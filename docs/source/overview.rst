.. _overview:

********
Overview
********

.. contents::
    :local:
    :depth: 2


The Big Picture
===============

The following image gives an overview of the Twitcher components.

.. image:: _images/twitcher-overview.png

The Aim
=======

The aim is to have a simple to use security filter for OGC/OWS services (especially for Web Processing Services)
which can be integrated in existing processing infrastructures.

The design aims are:

* Existing Web Processing Services and Clients should be able to use this security filter without modifications.
* Simple: to use, to deploy, to maintain, to understand, ...
* Token based security.
* Tokens are only valid for a short period of time.
* Able to be used in a distributed infrastructure (maybe using `Macaroons <https://github.com/rescrv/libmacaroons>`_?).
* Python .. *ehm* not a requirement ... but more and more used.

Twitcher Components
===================

Twitcher consists of the following main parts:

OWS Security
   A wsgi middleware (actually currently it is a `Pyramid tween <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-tween>`_) which puts a simple token based security layer on top of a wsgi application. The access tokens are stored in a MongoDB.
OWS Proxy
   A wsgi middleware which acts as a proxy for registred OWS services.
   Currently it only supports WPS services.
XML-RPC Interface
   An XML-RPC service which is used to control the token generation and OWS service registration.
   The interface is accessed using Basic Authentication. It should be used by an administrator and administrative web portals.

How to Use
==========

The OWS security middleware protects OWS services with a simple string based token mechanism.
A WPS client needs to provide a string token to access the internal WPS or a registered OWS service.
A token is generated via the XML-RPC interface. This interface is supposed to be used by
an external administration client which has user authentication and generates an access token on behalf of the user.

The OWS security middleware works currently only with WPS services.
It allows by default to use ``GetCapabilities`` and ``DescribeProcess`` requests without a token.
The ``Execute`` request (and anything else) can be accessed only with a valid token.

Access tokens have a life time limit. By default only for one hour but the admin
can set a longer life time when generating a token.

Twitcher is meant to be integrated in existing processing infrastructures with OGC/OWS services.
