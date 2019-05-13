.. _installation:

************
Installation
************

From GitHub Sources
===================

Install twitcher from GitHub sources:

.. code-block:: console

   $ git clone https://github.com/bird-house/twitcher.git
   $ cd twitcher
   $ conda env update -f environment.yml
   $ conda activate twitcher
   $ python setup.py install

The installation process setups a Conda_ environment named *twitcher*
with all dependent packages.

... or do it the lazy way
+++++++++++++++++++++++++

We provide also a ``Makefile`` to run this installation:

.. code-block:: console

   $ git clone https://github.com/bird-house/twitcher.git
   $ cd twitcher
   $ make clean    # cleans up a previous Conda environment
   $ make install  # runs the above installation steps

Initialize Database
===================

Initialize and upgrade the database using Alembic_.

Generate your first revision:

.. code-block:: console

  $ conda activate twitcher
  $ alembic -c development.ini revision --autogenerate -m "init"

Upgrade to that revision:

.. code-block:: console

  $ alembic -c development.ini upgrade head

Load default data into the database using a script.

.. code-block:: console

  $ initialize_twitcher_db development.ini


.. note::

  You can use `make db` as a shortcut to upgrade or init the twitcher database (last two steps).

Starting Twitcher Service
=========================

For development twitcher is using the the waitress_ WSGI server.

Start the twitcher service using the `development.ini` configuration:

.. code-block:: console

   $ pserve development.ini --reload

.. _waitress: https://docs.pylonsproject.org/projects/waitress/en/latest/
.. _Conda: https://conda.io/en/latest/
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
