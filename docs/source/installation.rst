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

.. code-block:: sh

   $ git clone https://github.com/bird-house/twitcher.git
   $ cd twitcher
   $ make clean    # cleans up a previous Conda environment
   $ make install  # runs the above installation steps

Starting Database
=================

Twitcher is using a MongoDB_ database.
The default configuration is using the MongoDB standard port 27017 on localhost.

You can install MongoDB with Conda_ for testing:

.. code-block:: console

  $ conda install mongodb=4
  # start DB for testing
  $ mongod --config etc/mongod.conf

Starting Twitcher Service
=========================

For development twitcher is using the the waitress_ WSGI server.

Start the twitcher service using the `development.ini` configuration:

.. code-block:: console

   $ pserve development.ini --reload

.. _waitress: https://docs.pylonsproject.org/projects/waitress/en/latest/
.. _Conda: https://conda.io/en/latest/
.. _MongoDB: https://www.mongodb.com/
