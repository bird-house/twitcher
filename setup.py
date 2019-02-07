import os
from setuptools import setup, find_packages

version = __import__('twitcher').__version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

reqs = [line.strip() for line in open('requirements.txt')]
extra_reqs = [line.strip() for line in open('requirements_dev.txt')]

setup(name='pyramid_twitcher',
      version=version,
      description='Security Proxy for OGC Services like WPS.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Development Status :: 4 - Beta",
      ],
      author='Carsten Ehbrecht',
      author_email='ehbrecht@dkrz.de',
      url='https://github.com/bird-house/twitcher.git',
      license='Apache License 2.0',
      keywords='pyramid twitcher birdhouse wps security proxy ows ogc',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='twitcher',
      install_requires=reqs,
      extra_requires=extra_reqs,
      entry_points="""\
      [paste.app_factory]
      main = twitcher:main
      [console_scripts]
      twitcherctl=twitcher.twitcherctl:main
      """,
      )
