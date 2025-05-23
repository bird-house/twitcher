Changes
*******

Unreleased
====================================================================================================================

0.10.1 (2025-05-23)
====================================================================================================================

Changes:

* Pin ``waitress>=3.0.2`` for Python 3.9+. Pin ``waitress>=3.0.0`` for legacy Python 3.8.
* Pin ``setuptools>=78.1.1`` for Python 3.9+. Pin ``setuptools==75.3.2`` for legacy Python 3.8.


0.10.0 (2024-07-22)
====================================================================================================================

Changes:

* Drop Python 3.6, 3.7 support.
* Deprecate Python 3.8 (EOL 2024-10 planed, supported until then).
* Add Python 3.12 support.
* Update docker with latest ``python:3.11-alpine3.20`` base.

0.9.0 (2023-02-08)
====================================================================================================================

Changes:

* Add CI workflow tests for Python 3.9, 3.10 and 3.11, and use 3.11 by default for all linting and coverage tests.
* Use Python 3.11 in Dockerfile for latest performance improvements and security fixes.
* Convert comment typing definitions into typing annotations.

0.8.0 (2023-02-01)
====================================================================================================================

Changes:

* Add ``/ows/verify/{service_name}[/{extra_path}]`` endpoint analoguous to ``/ows/proxy/{service_name}[/{extra_path}]``
  to only verify if access is granted to this service, for that specific resource path, and for the authenticated user,
  without performing the proxied request. This can be employed by servers and external entities to validate that
  authorization will be granted for the user without executing potentially heavy computation or large data transfers
  from the targeted resource that would otherwise be performed by requesting the ``/ows/proxy`` equivalent location.
  One usage example of this feature is using |nginx-auth|_ to verify an alternate resource prior to proxying a service
  request that needs authenticated access to the first resource.
* Add the OWS proxy ``send_request`` operation under the ``twitcher.adapter`` interface to allow it applying relevant
  proxying adjustments when using derived implementation. The ``DefaultAdapater`` simply calls the original function
  that was previously called directly instead of using the adapter's method.
* Removed the ``extra_path`` and ``request_params`` arguments from OWS proxy ``send_request`` to better align them with
  arguments from other adapter methods. These parameters are directly retrieved from the ``request`` argument, which was
  also provided as input to ``send_request``.

.. _nginx-auth: https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
.. |nginx-auth| replace:: NGINX Authentication Based on Subrequest Result

0.7.0 (2022-05-11)
====================================================================================================================

Changes:

* Add request and response hooks operations to adapter allowing derived implementations to modify OWS proxied requests
  and returned responses from the service. The default adapter applies no modifications to the original definitions.

0.6.2 (2021-12-01)
====================================================================================================================

Changes:

* Enforce regeneration of the ``OWSRegistry`` object on each request to avoid incorrect handling by adapters that
  require the new transaction or refreshed database session state each time.

0.6.1 (2021-10-27)
====================================================================================================================

Changes:

* Integrate functionality changes of ``0.5.x`` branch back into ``0.6.x``.
* Align ``twitcher.adapter`` features of ``0.6.x`` branch to support ``0.5.x`` behaviour.
* Revert removal of ``ServiceStoreInterface`` to provide relevant implementation details to external adapters.
* Apply missing interface classes as bases to default implementations.
* Add ``owsproxy_uri`` in frontpage response.
* Use ``hybrid_property`` to provide direct ``twitcher.models.Service.verify`` setter instead of protected ``_verify``.
* Add more logging and handling of errors to catch cases where adapter doesn't return a valid ``Service`` instance.
* Add ``scoped_session`` to ``session_factory`` object to ensure distinct connections and transactions are created for
  concurrent requests.

0.6.0 (2020-04-01)
====================================================================================================================

Changes:

* Added Keycloak support (`#91 <https://github.com/bird-house/twitcher/issues/91>`_).
* Added Keycloak demo notebook (
  `#92 <https://github.com/bird-house/twitcher/issues/92>`_,
  `#93 <https://github.com/bird-house/twitcher/issues/93>`_,
  `#94 <https://github.com/bird-house/twitcher/issues/94>`_).
* Refactor models definitions (``Service``, ``Client``, ``Token``).
* Refactor ``twitcher.adapter`` instantiation.
* Drop ``rpcinterface`` feature and endpoint.
* Drop ``owsproxy_delegate`` endpoint.
* Drop ``owsproxy_secure`` endpoint.

0.5.6 (2021-09-10)
====================================================================================================================

Changes:

* Add Github Actions workflow to run local tests and Docker smoke tests for pre-validation of features and changes.
* Add Github issue, feature request and pull request templates.

Fixes:

* Pin packages ``pyramid<2``, ``zope.sqlalchemy>=1.5`` and ``sqlalchemy>=1.4,<2`` to avoid errors with conflicting
  and upcoming release and features employed in code.
* Fix failing ``cryptography`` package build step in Docker image due to missing ``g++`` and ``rust`` dependencies
  (``rust`` installed via ``cargo``).

0.5.5 (2021-01-27)
====================================================================================================================

Fixes:

* Update invalid reference to ``python3-dev`` in docker image.
  Travis-CI is also updated to run a smoke test build of this docker image prior to merge to help early detection
  of problems prior to deploy triggers from tags.

0.5.4 (2020-10-29)
====================================================================================================================

Changes:

* Replace ``waitress`` by ``gunicorn`` to resolve issue related to slow download of large files (#97).

0.5.3 (2020-02-20)
====================================================================================================================

Changes:

* Reduce log level of ``"failed security check"`` from ``exception`` to ``warning`` as it corresponds to the expected
  code behavior (unauthorised access) when ``OWSException`` is raised, instead of dumping an unhandled error traceback.

0.5.2 (2019-07-11)
====================================================================================================================

New Features:

* Adds route ``/info`` which returns contents of ``twitcher.__version__``.
* Adds route `/versions` which returns version details such as `Twitcher` app version and employed adapter version.

Changes:

* Updated ``README.rst`` to match recent development, reference and docker image link.
* Adds URI of ``/info`` and ``/versions`` routes in the frontpage response.
* Corresponding HTTP status codes are returned for raised ``OWSException``.

Fixes:

0.5.1 (2019-05-24)
====================================================================================================================

New Features:

* Add `postgres` extra requirements for when it is used as database driver with ``sqlalchemy``.

Changes:

* Use ``container`` instead of ``config`` for ``AdapterInterface.owsproxy_config`` to match real use cases.

Fixes:

* Improve the adapter import methodology to work with more
  use cases (`Ouranosinc/Magpie#182 <https://github.com/Ouranosinc/Magpie/issues/182>`_).
* Fix incorrect setup for bump version within ``Makefile``.
* Fix Twitcher ``main`` including ``twitcher.<module>`` instead of ``.<module>``.

0.5.0 (2019-05-22)
====================================================================================================================

Changes:

* Skipped Buildout (`#49 <https://github.com/bird-house/twitcher/issues/49>`_).
* Replaced mongodb by sqlalchemy (`#51 <https://github.com/bird-house/twitcher/issues/51>`_).
* Simplified ``Makefile`` and skipped conda
  targets (`#75 <https://github.com/bird-house/twitcher/issues/75>`_).
* Add ``Makefile`` targets for ``docker``, ``bumpversion`` and ``coverage`` analysis
  related tasks (`#67 <https://github.com/bird-house/twitcher/issues/67>`_).
* Removed unused ``config`` module (`#70 <https://github.com/bird-house/twitcher/issues/70>`_).

New Features:

* Provided a ``Dockerfile`` for building `Twitcher`
  (`#67 <https://github.com/bird-house/twitcher/issues/67>`_).
* Provide ``AdapterInterface`` to allow overriding store implementations with configuration
  setting ``twitcher.adapter`` (`#67 <https://github.com/bird-house/twitcher/issues/67>`_).
* Add version auto-update (number and date) of these 'changes' with ``bump2version``
  (`#67 <https://github.com/bird-house/twitcher/issues/67>`_).

Fixes:

* Update requirements with missing dependencies when building docker image.
* Various fixes (
  `#71 <https://github.com/bird-house/twitcher/issues/71>`_,
  `#72 <https://github.com/bird-house/twitcher/issues/72>`_,
  `#73 <https://github.com/bird-house/twitcher/issues/73>`_,
  `#74 <https://github.com/bird-house/twitcher/issues/74>`_)

0.4.0 (2019-05-02)
====================================================================================================================

Changes:

* Skipped Python 2.7 support (`#61 <https://github.com/bird-house/twitcher/issues/61>`_).
* Added public URL "purl" (`#58 <https://github.com/bird-house/twitcher/issues/58>`_).
* Added SSL verify option (`#55 <https://github.com/bird-house/twitcher/issues/55>`_).
* Skipped internal WPS (`#52 <https://github.com/bird-house/twitcher/issues/52>`_).
* Moved tests to top-level folder (`#47 <https://github.com/bird-house/twitcher/issues/47>`_).

0.3.8 (2018-09-11)
====================================================================================================================

Fixes:

* Fixed the wps DataInputs params encoding (`#42 <https://github.com/bird-house/twitcher/issues/42>`_).
* Fixed error 400 Contradictory scheme headers (`#40 <https://github.com/bird-house/twitcher/issues/40>`_).

New Features:

* make protected path configurable (`#36 <https://github.com/bird-house/twitcher/issues/36>`_).

0.3.7 (2018-03-13)
====================================================================================================================

Fixes:

* Fixed exclude filter in ``MANIFEST.in``.

New Features:

* Feature `#28 <https://github.com/bird-house/twitcher/issues/28>`_: use request upstream when not using WPS
  (e.g download file through ``thredds``).

0.3.6 (2018-03-08)
====================================================================================================================

* Fix PEP8
* Removed unused ``c4i`` option.
* Added ``auth`` option to set authentication method.
* Updated docs for usage of x509 certificates.

New Features:

* Feature `#25 <https://github.com/bird-house/twitcher/issues/25>`_: using x509 certificates for service authentication.

0.3.5 (2018-03-01)
====================================================================================================================

* Fix PEP8.
* Updated makefile.
* Updated buildout recipes.
* Fixed nginx dependency.
* Updated mongodb 3.4.
* Configured csrf in ``xmlrpc``.
* Fixed tutorial example.
* Added readthedocs, licence and chat badges.

0.3.4 (2017-05-05)
====================================================================================================================

* Updated logging.
* Fixed: creates workdir if it does not exist.

0.3.3 (2017-04-27)
====================================================================================================================

* Fixed fetching of access token when service is public.

0.3.2 (2017-01-31)
====================================================================================================================

* Set header ``X-X509-User-Proxy``.

0.3.1 (2017-01-26)
====================================================================================================================

* Fix PEP8.
* Set permission of ``certfile``.
* Added option ``ows-proxy-delegate``.

0.3.0 (2017-01-11)
====================================================================================================================

* Fix PEP8.
* Changed rpc interface.
* Added twitcher.client module.
* Using esgf scls service to get credentials.
* Updated internal pywps to version 4.0.0.
* Using default port 5000.
* Added ipython notebook examples.
* Moved ``namesgenerator`` to top-level.
* Added ``_compat`` module for Python 3.x/2.x compatibility.
* Added ``twitcher.api`` and cleaned up rpcinterface.
* Added ``twitcher.store`` with mongodb and memory implementation.
* Added ``twitcher.datatype`` with ``AccessToken`` and ``Service``.
* Using https port only.
* Using ``OWSExceptions`` on errors in owsproxy.

0.2.4 (2016-12-23)
====================================================================================================================

* Fix PEP8.
* Using ``replace_caps_url`` in ``owsproxy``.
* Pinned ``mongodb=2.6*|3.3.9``.
* Replaced ``service_url`` by ``proxy_url``.
* Added ``wms_130`` and renamed ``wms_111``.

0.2.3 (2016-11-18)
====================================================================================================================

* Fix PEP8.
* Using ``doc2dict``, renamed ``get_service_by_name()``.
* Added support for c4i tokens.
* Updated deps: ``pytest``, ``mongodb``.
* Updated buildout recipes.
* Fixed functional tests.

0.2.2 (2016-08-18)
====================================================================================================================

* Fix PEP8.
* Don't allow duplicate service names.

0.2.1 (2016-08-05)
====================================================================================================================

* Register service with public access.
* WMS services can be registered.

0.2.0 (2016-07-18)
====================================================================================================================

* Updated to new buildout with separated conda environment.
* Replaced nose by pytest.
* Updated installation docs.

0.1.7 (2016-06-09)
====================================================================================================================

Fixes:

* Update of service failed (`#17 <https://github.com/bird-house/twitcher/issues/17>`_).

0.1.6 (2016-06-01)
====================================================================================================================

* Updated docs.
* Renamed Python package to ``pyramid_twitcher``.
* Conda ``environment.yml`` added.
* Using ``get_sane_name()``.
* Replaced ``httplib2`` by ``requests``.

Fixes:

* Don't check token for allowed requests (`#14 <https://github.com/bird-house/twitcher/issues/14>`_).
* Ignore decoding errors of response content (`#13 <https://github.com/bird-house/twitcher/issues/13>`_).
* Fixed twitcher app config: wrong egg name.

0.1.5 (2016-04-22)
====================================================================================================================

* Fixed docs links

0.1.4 (2016-04-19)
====================================================================================================================

* Fixed ``MANIFEST.in``
* Fixed service database index.
* Updated ``Makefile``.
* Added more links to appendix.

0.1.0 (2015-12-07)
====================================================================================================================

Initial Release.
