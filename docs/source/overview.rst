.. _overview:

********
Overview
********

Twitcher Components
===================

Twitcher consists of the following main parts:

OWS Security
   A security layer to protect service access with x509 certificates and :ref:`oauth2_api`.
OWS Registry
   :ref:`ows_registry_api` is a registration service with an :ref:`openapi_api` to register OWS services for the OWS proxy.
OWS Proxy
   :ref:`ows_proxy_api` a service which acts as a proxy for registered OWS services.

.. image:: _images/twitcher-overview.png
