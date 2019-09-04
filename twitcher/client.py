import os

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from twitcher.oauth2 import TOKEN_ENDPOINT, CLIENT_APP_ENDPOINT

import logging
LOGGER = logging.getLogger("TWITCHER")

KEYCLOAK_TOKEN_ENDPOINT = '/auth/realms/demo/protocol/openid-connect/token'


class TwitcherService(object):
    """TwitcherService is a twitcher client to talk to the twitcher service API."""
    def __init__(self, url, username=None, password=None, verify=True):
        self.base_url = url
        self.username = username
        self.password = password
        self.verify = verify

    def add_client_app(self, name=None, redirect_uri=None):
        """Add a client application to twitcher with optional name."""
        name = name or ''
        redirect_uri = redirect_uri or ''
        req_url = "{}{}?name={}&redirect_uri={}".format(
            self.base_url,
            CLIENT_APP_ENDPOINT,
            name,
            redirect_uri)
        resp = requests.get(req_url, auth=(self.username, self.password), verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not add client app.")
        else:
            return resp.json()

    def fetch_token(self, client_id, client_secret, scope=None, keycloak=False):
        """Get an access token with given scope."""
        scope = scope or 'compute'
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        if keycloak is True:
            endpoint = KEYCLOAK_TOKEN_ENDPOINT
        else:
            endpoint = TOKEN_ENDPOINT
        token_url = "{}{}".format(self.base_url, endpoint)
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        return oauth.fetch_token(token_url,
                                 scope=scope,
                                 client_id=client_id,
                                 client_secret=client_secret,
                                 include_client_id=True,
                                 verify=self.verify)

    def list_services(self):
        """List all registered OWS services."""
        req_url = "{}/services".format(self.base_url)
        resp = requests.get(req_url, auth=(self.username, self.password), verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not list services")
        else:
            return resp.json()

    def register_service(self, name, url, data=None):
        """Register a service."""
        data = data or {}
        data.update({"name": name, "url": url})
        req_url = "{}/services".format(self.base_url)
        import json
        resp = requests.post(req_url, data=json.dumps(data),
                             auth=(self.username, self.password),
                             headers={},
                             verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not add service")
        else:
            return resp.json()

    def clear_services(self):
        """Remove all OWS services."""
        req_url = "{}/services".format(self.base_url)
        resp = requests.delete(req_url,
                               auth=(self.username, self.password),
                               headers={},
                               verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not clear services")
        else:
            return resp.json()

    def get_service(self, name):
        """Get an OWS service with given name."""
        req_url = "{}/services/{}".format(self.base_url, name)
        resp = requests.get(req_url,
                            auth=(self.username, self.password),
                            verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not get service")
        else:
            return resp.json()

    def unregister_service(self, name):
        """Remove registered service with given name."""
        req_url = "{}/services/{}".format(self.base_url, name)
        resp = requests.delete(req_url,
                               auth=(self.username, self.password),
                               headers={},
                               verify=self.verify)
        if not resp.ok:
            LOGGER.error("Could not remove service")
        else:
            return resp.json()
