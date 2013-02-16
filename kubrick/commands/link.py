import os
from string import Formatter
from itertools import product, izip

from kubrick.printer import printer
from kubrick.commands import Command
from kubrick.db import MoviesMetadata
from kubrick.datasources import MovieDatasource


def format_all(format_string, env):
    """
    """

    formatter = Formatter()
    fields = [x[1] for x in formatter.parse(format_string) if x[1] is not None]

    # Create a prepared environment with only used fields, all as list:
    prepared_env = []
    for field in fields:
        field_values = env.get(field, [])
        if not isinstance(field_values, list):
            field_values = [field_values]
        prepared_env.append(set(field_values))

    # Generate each possible combination, format the string with it and yield
    # the resulting string:
    for field_values in product(*prepared_env):
        format_env = dict(izip(fields, field_values))
        yield format_string.format(**format_env)


def walk_links(directory, prefix='', linkbase=None):
    """ Return all links contained in directory (or any sub directory).
    """
    links = {}
    try:
        for child in os.listdir(directory):
            fullname = os.path.join(directory, child)
            if os.path.islink(fullname):
                link_path = os.path.normpath(os.path.join(directory, os.readlink(fullname)))
                if linkbase:
                    link_path = os.path.relpath(link_path, linkbase)
                links[os.path.join(prefix, child)] = link_path
            elif os.path.isdir(fullname):
                links.update(walk_links(fullname,
                                        prefix=os.path.join(prefix, child),
                                        linkbase=linkbase))
    except OSError as err:
        if err.errno != 2:  # Ignore unknown directory error
            raise
    return links


class Link(Command):

    """ Create links in the kubrick tree.
    """

    help = 'create symlinks'

    def run(self, args, config):
        mdb = MoviesMetadata(os.path.join(args.tree, '.kub', 'metadata.db'))
        mds = MovieDatasource(config.subsections('datasource'), args.tree)

        # Create the list of links that must exists on the fs:
        db_links = {}
        for movie_hash, movie in mdb.itermovies():
            movie = mds.attach(movie_hash, movie)
            for view in config.subsections('view'):
                for result in format_all(view.get('pattern'), movie):
                    filename = os.path.join(view.args[0], result)
                    if filename in db_links:
                        printer.p('Warning: duplicate link {link}', link=filename)
                    else:
                        db_links[filename] = movie_hash

        # Create the list of links already existing on the fs:
        fs_links = {}
        for view in config.subsections('view'):
            view_links = walk_links(os.path.join(args.tree, view.args[0]),
                                    prefix=view.args[0],
                                    linkbase=os.path.join(args.tree, '.kub', 'movies'))
            fs_links.update(view_links)

        db_links = set(db_links.iteritems())
        fs_links = set(fs_links.iteritems())

        links_to_delete = fs_links - db_links
        links_to_create = db_links - fs_links

        printer.p('Found {rem} links to delete, {add} links to create',
                  rem=len(links_to_delete),
                  add=len(links_to_create))

        # Delete the old links:
        for filename, link in links_to_delete:
            printer.verbose('Deleting {file}', file=filename)
            os.remove(os.path.join(args.tree, filename))

        # Create the new links:
        for filename, link in links_to_create:
            fullname = os.path.join(args.tree, filename)
            dirname = os.path.dirname(fullname)
            movie_link = os.path.join(args.tree, '.kub', 'movies', link)
            try:
                os.makedirs(dirname)
            except OSError as err:
                if err.errno != 17:  # Ignore already existing directory error
                    raise
            printer.verbose('Creating link {file!r} to {link!r}', file=filename, link=link)
            os.symlink(os.path.relpath(movie_link, dirname), fullname)