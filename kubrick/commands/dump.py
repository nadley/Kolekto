import os
import json

from kubrick.printer import printer
from kubrick.commands import Command
from kubrick.db import MoviesMetadata


class Dump(Command):

    """ Dump the whole database into json.
    """

    help = 'dump database into json'

    def run(self, args, config):
        mdb = MoviesMetadata(os.path.join(args.tree, '.kub', 'metadata.db'))
        dump = [{'hash': x, 'movie': y} for x, y in mdb.itermovies()]
        json.dump(dump, printer.output)