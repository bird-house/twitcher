import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

about = {}
with open(os.path.join(here, 'twitcher', '__version__.py'), 'r') as f:
    exec(f.read(), about)

reqs = [line.strip() for line in open('requirements.txt')]
dev_reqs = [line.strip() for line in open('requirements_dev.txt')]

setup(name='pyramid_twitcher',
      version=about['__version__'],
      description=about['__doc__'],
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Development Status :: 4 - Beta",
      ],
      author=about['__author__'],
      author_email=about['__email__'],
      url='https://github.com/bird-house/twitcher.git',
      license='Apache License 2.0',
      keywords='web pyramid twitcher birdhouse wps security proxy ows ogc',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='twitcher',
      install_requires=reqs,
      extras_require={
          "dev": dev_reqs,              # pip install ".[dev]"
          "postgres": ["psycopg2"],     # when using postgres database driver with sqlalchemy
      },
      entry_points="""\
      [paste.app_factory]
      main = twitcher:main
      [console_scripts]
      twitcherctl=twitcher.scripts.twitcherctl:main
      initialize_twitcher_db=twitcher.scripts.initialize_db:main
      """,
      )
