.. _tutorial:

********
Tutorial
********

.. contents::
    :local:
    :depth: 2

Using the OWSProxy with an external WPS application
===================================================


The ``OWSProxy`` is a proxy service for OWS services. Currently it only supports WPS.

First you need an external WPS. You can use `Emu WPS service <http://emu.readthedocs.io/en/latest/>`_ from Birdhouse.
Get it from GitHub and run the installation:

.. code-block:: console

    $ git clone https://github.com/bird-house/emu.git
    $ cd emu
    $ make install
    $ make start

The Emu WPS service is available by default at the URL:
http://localhost:5000/wps?service=WPS&version=1.0.0&request=GetCapabilities


Make sure Twitcher is installed and running:

.. code-block:: console

   $ cd ../twitcher  # cd into the twitcher installation folder
   $ pserve development.ini

Register a WPS service
----------------------

Register the Emu WPS service at the Twitcher ``OWSProxy``:

.. code-block:: console

   $ twitcherctl -k register --name emu http://localhost:5000/wps

If you don't provide a name with ``--name`` option then a nice name will be generated, for example ``sleepy_flamingo``.

Use the ``list`` command to see which WPS services are registered with OWSProxy:

.. code-block:: console

   $ twitcherctl -k list
   [{'url': 'http://localhost:5000/wps', 'proxy_url': 'https://localhost:8000/ows/proxy/emu', 'type': 'wps', 'name': 'emu'}]


Access a registered service
---------------------------

By default the registered service is available at the URL ``https://localhost:8000/ows/proxy/{service_name}``.
Replace the ``service_name`` with the registered name.

Run a ``GetCapabilities`` request for the registered Emu WPS service:

.. code-block:: console

    $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=getcapabilities"


Run a ``DescribeProcess`` request:

.. code-block:: console

    $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=describeprocess&identifier=hello&version=1.0.0"

Use tokens to run an execute request
------------------------------------

By default the WPS service is protected by the ``OWSSecurity`` wsgi middleware. You need to provide an access token to run an execute request.

Run an ``Exceute`` request:

.. code-block:: console

    $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=execute&identifier=hello&version=1.0.0&datainputs=name=tux"

Now you should get an XML error response with a message that you need to provide an access token (see section above).

We need to generate an access token with ``twitcherctl``:

.. code-block:: console

    $ twitcherctl -k gentoken -H 24
    def456

By default the token has a limited life time of one hour.
With the option ``-H`` you can extend the life time in hours (24 hours in this example).

You can provide the access token in three ways (see section above):

* as HTTP parameter,
* as part of the HTTP header
* or as part of the url path.

In the following example we provide the token as HTTP parameter:

.. code-block:: console

    $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=execute&identifier=hello&version=1.0.0&datainputs=name=tux&token=def456"

.. warning::

   If you have set enviroment variables with your access token then they will *not* be available in the external service.


Use x509 certificates to control client access
==================================================

.. warning::

  You need the Nginx web-service in front of the Twitcher WSGI service to use x509 certificates.

Since version 0.3.6 Twitcher is prepared to use x509 certificates to control client access.
By default it is configured to accept x509 proxy certificates from ESGF_.

Register the Emu WPS service at the Twitcher ``OWSProxy`` with ``auth`` option ``cert``:

.. code-block:: console

   $ twitcherctl -k register --name emu --auth cert http://localhost:5000/wps

The ``GetCapabilities``  and ``DescribeProcess`` requests are not blocked:

.. code-block:: console

  $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=getcapabilities"
  $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=describeprocess&identifier=hello&version=1.0.0"

When you run an ``Exceute`` request without a certificate you should get an exception report:

.. code-block:: console

  $ curl -k "http://localhost:8000/ows/proxy/emu?service=wps&request=execute&identifier=hello&version=1.0.0&datainputs=name=tux"

Now you should get an XML error response with a message that you need to provide a valid X509 certificate.

Get a valid proxy certificate from ESGF, you may use the `esgf-pyclient`_ to run a myproxy logon.
Let's say your proxy certificate is ``cert.pem``, then run the exceute request again using this certificate:

.. code-block:: console

  $ curl --cert cert.pem --key cert.pem -k "http://localhost:8000/ows/proxy/emu?service=wps&request=execute&identifier=hello&version=1.0.0&datainputs=name=tux"


.. _ESGF: https://esgf.llnl.gov/
.. _esgf-pyclient: https://github.com/ESGF/esgf-pyclient
