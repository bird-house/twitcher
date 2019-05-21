.. _installation:

************
Installation
************

Quick Installation
==================

Quick steps to install and start Twitcher:

.. code-block:: console

  $ git clone https://github.com/bird-house/twitcher.git
  $ cd twitcher
  $ conda env create
  $ conda activate twitcher
  $ make install
  $ make migrate
  $ make start

From GitHub Sources
===================

Get Twitcher source from GitHub:

.. code-block:: console

   $ git clone https://github.com/bird-house/twitcher.git
   $ cd twitcher

Create Conda_ environment named *twitcher*:

.. code-block:: console

   $ conda env update -f environment.yml
   $ conda activate twitcher

Install the Twitcher app:

.. code-block:: console

   $ pip install -e .
   OR
   make install

For development you can use this command:

.. code-block:: console

  $ pip install -e .[dev]
  OR
  $ make develop

Initialize Database
===================

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

Starting Twitcher Service
=========================

For development twitcher is using the the waitress_ WSGI server.

Start the twitcher service using the `development.ini` configuration:

.. code-block:: console

   $ pserve development.ini --reload

.. _waitress: https://docs.pylonsproject.org/projects/waitress/en/latest/
.. _Conda: https://conda.io/en/latest/
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
