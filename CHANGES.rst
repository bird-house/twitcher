Changes
*******

Unreleased
==========

0.5.2 (2019-07-11)
==================

New Features:

* Adds route `/info` which returns contents of `twitcher.__version__`.
* Adds route `/versions` which returns version details such as `Twitcher` app version and employed adapter version.

Changes:

* Updated `README.rst` to match recent development, reference and docker image link.
* Adds URI of `/info` and `/versions` routes in the frontpage response.
* Corresponding HTTP status codes are returned for raised ``OWSException``.

Fixes:

0.5.1 (2019-05-24)
==================

New Features:

* Add `postgres` extra requirements for when it is used as database driver with `sqlalchemy`.

Changes:

* Use ``container`` instead of ``config`` for ``AdapterInterface.owsproxy_config`` to match real use cases.

Fixes:

* Improve the adapter import methodology to work with more use cases (https://github.com/Ouranosinc/Magpie/issues/182).
* Fix incorrect setup for bump version within `Makefile`.
* Fix Twitcher `main` including ``twitcher.<module>`` instead of ``.<module>``.

0.5.0 (2019-05-22)
==================

Changes:

* Skipped Buildout (#49).
* Replaced mongodb by sqlalchemy (#51).
* Simplified `Makefile` and skipped conda targets (#75).
* Add `Makefile` targets for `docker`, `bumpversion` and `coverage` analysis related tasks (#67).
* Removed unused `config` module (#70).

New Features:

* Provided a `Dockerfile` for building `Twitcher` (#67).
* Provide ``AdapterInterface`` to allow overriding store implementations with configuration setting ``twitcher.adapter`` (#67).
* Add version auto-update (number and date) of these 'changes' with ``bump2version`` (#67).

Fixes:

* Update requirements with missing dependencies when building docker image.
* Various fixes (#74, #73, #72, #71)

0.4.0 (2019-05-02)
==================

Changes:

* Skipped Python 2.7 support (#61).
* Added public URL "purl" (#58).
* Added SSL verify option (#55).
* Skipped internal WPS (#52).
* Moved tests to top-level folder (#47).

0.3.8 (2018-09-11)
==================

Fixes:

* Fixed the wps DataInputs params encoding (#42).
* Fixed error 400 Contradictory scheme headers (#40).

New Features:

* make protected path configurable (#36).

0.3.7 (2018-03-13)
==================

Fixes:

* fixed exclude filter in MANIFEST.in.

New Features:

* Feature #28: use request upstream when not using wps (e.g download file through thredds).

0.3.6 (2018-03-08)
==================

* pep8
* removed unused ``c4i`` option.
* added ``auth`` option to set authentication method.
* updated docs for usage of x509 certificates.

New Features:

* Feature #25: using x509 certificates for service authentication.

0.3.5 (2018-03-01)
==================

* pep8
* updated makefile
* updated buildout recipes
* fixed nginx dependency
* updated mongodb 3.4
* configured csrf in xmlrpc
* fixed tutorial example
* added readthedocs, licence and chat badges

0.3.4 (2017-05-05)
==================

* updated logging.
* fixed: creates workdir if it does not exist.

0.3.3 (2017-04-27)
==================

* fixed fetching of access token when service is public.

0.3.2 (2017-01-31)
==================

* set header X-X509-User-Proxy.


0.3.1 (2017-01-26)
==================

* pep8.
* set permission of certfile.
* added option ows-proxy-delegate.

0.3.0 (2017-01-11)
==================

* pep8.
* changed rpc interface.
* added twitcher.client module.
* using esgf scls service to get credentials.
* updated internal pywps to version 4.0.0.
* using default port 5000.
* added ipython notebook examples.
* moved namesgenerator to top-level.
* added _compat module for python 3.x/2.x compatibility.
* added twitcher.api and cleaned up rpcinterface.
* added twitcher.store with mongodb and memory implementation.
* added twitcher.datatype with AccessToken and Service.
* using https port only.
* using OWSExceptions on errors in owsproxy.

0.2.4 (2016-12-23)
==================

* pep8.
* using replace_caps_url in owsproxy.
* pinned mongodb=2.6*|3.3.9.
* replaced service_url by proxy_url.
* added wms_130 and renamed wms_111.

0.2.3 (2016-11-18)
==================

* pep8
* using doc2dict, renamed get_service_by_name().
* added support for c4i tokens.
* updated deps: pytest, mongodb.
* updated buildout recipes.
* fixed functional tests.

0.2.2 (2016-08-18)
==================

* pep8
* don't allow dupliate service names.

0.2.1 (2016-08-05)
==================

* register service with public access.
* WMS services can be registered.

0.2.0 (2016-07-18)
==================

* updated to new buildout with seperated conda environment.
* replaced nose by pytest.
* updated installation docs.

0.1.7 (2016-06-09)
==================

Bugfixes:

* update of service failed (#17).

0.1.6 (2016-06-01)
==================

* updated docs.
* renamed python package to pyramid_twitcher.
* conda envionment.yml added.
* using get_sane_name().
* replaced httplib2 by requests.

Bugfixes:

* don't check token for allowed requests (#14).
* ignore decoding errors of response content (#13).
* fixed twitcher app config: wrong egg name.

0.1.5 (2016-04-22)
==================

* fixed docs links

0.1.4 (2016-04-19)
==================

* Fixed MANIFEST.in
* Fixed service database index.
* Updated makefile.
* Added more links to appendix.

0.1.0 (2015-12-07)
==================

Initial Release.
