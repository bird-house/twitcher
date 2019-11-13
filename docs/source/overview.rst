.. _overview:

********
Overview
********

Twitcher Components
===================

Twitcher consists of the following main parts:

OWS Security
   A security layer to protect service access with :ref:`oauth2_api`.
OWS Registry
   :ref:`ows_registry_api` is a registration service with an :ref:`openapi_api` to register OWS services for the OWS proxy protected by basic authentication.
OWS Proxy
   :ref:`ows_proxy_api` a service which acts as a proxy for registered OWS services.

OAuth access tokens can be retrieved from a Keycloak authentication service using the `client credentials workflow`_.

.. image:: _images/twitcher-overview.png

.. _`client credentials workflow`: https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#refreshing-tokens
