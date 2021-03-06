.. _devguide:

Developer Guide
===============

.. contents::
    :local:
    :depth: 1

.. _testing:

Running tests
-------------

Run tests using `pytest`_.

First activate the ``twitcher`` Conda environment and install ``pytest``.

.. code-block:: console

   $ source activate twitcher
   $ pip install -r requirements_dev.txt  # if not already installed
   OR
   $ make develop

Run quick tests (skip slow and online):

.. code-block:: console

    $ pytest -m 'not slow and not online'"

Run all tests:

.. code-block:: console

    $ pytest

Check pep8:

.. code-block:: console

    $ flake8

Run tests the lazy way
----------------------

Do the same as above using the ``Makefile``.

.. code-block:: console

    $ make test
    $ make test-all
    $ make lint
    $ make coverage

Upgrade Database
----------------

Initialize and upgrade the database using Alembic_.

Generate your first revision:

.. code-block:: console

  $ conda activate twitcher
  $ alembic -c development.ini revision --autogenerate -m "init"

.. warning::

    This first step is only needed in development to generate a new database schema version.

Upgrade to that revision:

.. code-block:: console

  $ alembic -c development.ini upgrade head

Load default data into the database using a script.

.. code-block:: console

  $ initialize_twitcher_db development.ini

.. note::

  You can use `make migrate` as a shortcut to upgrade or init the twitcher database (last two steps).


Building the docs
-----------------

First install dependencies for the documentation:

.. code-block:: console

  $ make docs

Prepare a release
-----------------

Update `CHANGES.rst`.

Bump a new version
------------------

Make a new version of twitcher in the following steps:

* Make sure everything is commit to GitHub.
* Update ``CHANGES.rst`` with the next version.
* Dry Run: ``bumpversion --dry-run --verbose --new-version 0.5.1 patch``
* Do it: ``bumpversion --new-version 0.5.1 patch``
* ... or: ``bumpversion --new-version 0.6.0 minor``
* Push it: ``git push``
* Push tag: ``git push --tags``

See the bumpversion_ documentation for details.

.. _bumpversion: https://pypi.org/project/bumpversion/
.. _pytest: https://docs.pytest.org/en/latest/
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
