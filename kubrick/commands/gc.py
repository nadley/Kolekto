import os

from kubrick.printer import printer
from kubrick.commands import Command
from kubrick.db import MoviesMetadata


class Gc(Command):

    """ Garbage collect orphan files stored in tree.
    """

    help = 'garbage collect orphan files'

    def run(self, args, config):
        mdb = MoviesMetadata(os.path.join(args.tree, '.kub', 'metadata.db'))
        db_files = set()
        for movie_hash, movie in mdb.itermovies():
            db_files.add(movie_hash)
            db_files.update(movie.get('_externals', []))
        printer.verbose('Found {nb} files in database', nb=len(db_files))
        fs_files = set(os.listdir(os.path.join(args.tree, '.kub', 'movies')))
        printer.verbose('Found {nb} files in filesystem', nb=len(fs_files))
        orphan_files = fs_files - db_files
        printer.p('Found {nb} orphan files to delete', nb=len(orphan_files))
        if orphan_files:
            printer.verbose('Files to delete: {files}', files=', '.join(orphan_files))
            if printer.ask('Would you like to delete orphans?'):
                for orphan_file in orphan_files:
                    try:
                        os.remove(os.path.join(args.tree, '.kub', 'movies', orphan_file))
                    except OSError as err:
                        printer.p('Unable to delete {file}: {err}', file=orphan_file, err=err)
                    else:
                        printer.verbose('Deleted {file}', file=orphan_file)