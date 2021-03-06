from setuptools import setup, find_packages
import os

version = '1.2~dev'

base = os.path.dirname(__file__)

readme = open(os.path.join(base, 'README.rst')).read()
changelog = open(os.path.join(base, 'CHANGELOG.rst')).read()
todo = open(os.path.join(base, 'TODO.rst')).read()


setup(name='kolekto',
      version=version,
      description='A really KISS movie catalog software',
      long_description=readme + '\n' + changelog + '\n' + todo,
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent'],
      keywords='kolekto movies',
      author='Antoine Millet',
      author_email='antoine@inaps.org',
      url='https://github.com/NaPs/Kolekto',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      scripts=['bin/kolekto'],
      entry_points={'kolekto.commands': ['gc = kolekto.commands.gc:Gc',
                                         'link = kolekto.commands.link:Link',
                                         'show = kolekto.commands.show:Show',
                                         'rm = kolekto.commands.rm:Rm',
                                         'refresh = kolekto.commands.refresh:Refresh',
                                         'dump = kolekto.commands.dump:Dump',
                                         'restore = kolekto.commands.restore:Restore',
                                         'config = kolekto.commands.config:Config',
                                         'watch = kolekto.commands.flags:Watch',
                                         'fav = kolekto.commands.flags:Favorite',
                                         'crap = kolekto.commands.flags:Crap',
                                         'edit = kolekto.commands.edit:Edit'],
                    'kolekto.commands.no_profile': ['init = kolekto.commands.init:Init'],
                    'kolekto.commands.movies': ['list = kolekto.commands.list:List',
                                                'import = kolekto.commands.importer:ImportMovies',
                                                'stats = kolekto.commands.stats:Stats',
                                                'find-duplicates = kolekto.commands.find_duplicates:FindDuplicates'],
                    'kolekto.datasources': ['tmdb = kolekto.datasources.tmdb:TmdbDatasource',
                                            'tmdb_proxy = kolekto.datasources.tmdb:TmdbProxyDatasource',
                                            'mediainfos = kolekto.datasources.mediainfos:MediainfosDatasource'],
                    'kolekto.profiles': ['movies = kolekto.profiles.movies:Movies']},
      install_requires=['dotconf', 'kaa-metadata', 'progressbar', 'requests'])
