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

Before you can start the service you need to initialize or upgrade the database:

.. code-block:: console

  $ make migrate

Starting Twitcher Service
=========================

For development twitcher is using the the waitress_ WSGI server.

Start the twitcher service using the `development.ini` configuration:

.. code-block:: console

   $ pserve development.ini --reload
   OR
   $ make start

.. _waitress: https://docs.pylonsproject.org/projects/waitress/en/latest/
.. _Conda: https://conda.io/en/latest/
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
