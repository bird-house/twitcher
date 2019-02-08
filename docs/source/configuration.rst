.. _configuration:

******************
Configuration File
******************

.. contents::
    :local:
    :depth: 2

After you have installed twitcher you can customize the default twitcher configuration by editing the ``custom.cfg`` configuration file. This configuration file overwrites the default settings in the ``buildout.cfg``:

.. code-block:: cfg

   $ vim custom.cfg
   $ cat custom.cfg
   [buildout]
   extends = buildout.cfg

   [settings]
   hostname = localhost
   https-port = 8000
   log-level = WARN
   username =
   password =
   workdir =
   ows-security = true
   ows-proxy = true
   rpcinterface = true

After your have made a change in ``custom.cfg`` you *need to update* the installation and restart the twitcher service:

.. code-block:: sh

   $ make update
   $ make restart
   $ make status

Set hostname and port
=====================

Edit the options ``hostname`` and ``https-port``.


Activate basic-auth for XML-RPC control interface
=================================================

Set ``username`` and ``password``.

Deactivate twitcher components
==============================

Twitcher has four components which by default are activated:

ows-security
   The OWS security wsgi middleware
ows-proxy
   A proxy wsgi application for OWS services
rpcinterface
   An XML-RPC interface to control token generation and service registration

By setting a component option to ``false`` you can deactivate it:

.. code-block:: sh

   [settings]
   ows-proxy = false
