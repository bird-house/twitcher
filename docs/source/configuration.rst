.. _configuration:

Configuration
=============

Twitcher has a configuration file `development.ini` for local development.
Copy and edit this configuration to adapt to your settings.

Service
-------

Edit the configuration to change the service parameters.

The URL of the Twitcher service endpoint:

.. code-block:: ini

  twitcher.url = http://localhost:8000


Basic Authentication
--------------------

Twitcher uses basic authentication for client application registration.
Edit username in password in the configuration:

.. code-block:: ini

  twitcher.username = demo
  twitcher.password = demo


OAuth2 Token Generator
----------------------

Twitcher uses `OAuth2 tokens`_ to control access to the service registration and the OWS service access.
You can use three types of tokens.

Random Token
++++++++++++

Tokens with UUID strings stored in the local twitcher database.

Edit the configuration file:

.. code-block:: ini

  twitcher.token.type = random_token


Signed Token
++++++++++++

`JWT tokens`_ signed with a certificate. You can generate a self-signed certificate
for testing with the Makefile:

.. code-block:: console

  $ make gencert

Edit the configuration file:

.. code-block:: ini

  twitcher.token.type = signed_token
  twitcher.token.keyfile = key.pem # private key
  twitcher.token.certfile = pubkey.pem # public key

Custom Token
++++++++++++

JWT tokens using a shared secret. You can generate a UUID secret with:

.. code-block:: console

  $ make gensecret

Edit the configuration file:

.. code-block:: ini

  twitcher.token.type = custom_token
  twitcher.token.secret = secret

.. _OAuth2 tokens: https://oauthlib.readthedocs.io/en/latest/oauth2/tokens/bearer.html
.. _JWT tokens: https://pyjwt.readthedocs.io/en/latest/usage.html
