"""
Testing the Twitcher API.
"""

from .common import BaseTest, dummy_request

from twitcher.store import AccessTokenStore, ServiceStore
from twitcher.api import TokenManager, Registry
from twitcher.tokengenerator import UuidTokenGenerator


class TokenManagerTest(BaseTest):

    def setUp(self):
        super(TokenManagerTest, self).setUp()
        self.init_database()

        token_store = AccessTokenStore(
            dummy_request(dbsession=self.session))
        self.tokenmgr = TokenManager(
            tokengenerator=UuidTokenGenerator(),
            tokenstore=token_store
        )

    def test_generate_token_and_revoke_it(self):
        # gentoken
        resp = self.tokenmgr.generate_token()
        assert 'access_token' in resp
        assert 'expires_at' in resp
        # revoke
        resp = self.tokenmgr.revoke_token(resp['access_token'])
        assert resp is True
        # revoke all
        resp = self.tokenmgr.revoke_all_tokens()
        assert resp is True


class RegistryTest(BaseTest):

    def setUp(self):
        super(RegistryTest, self).setUp()
        self.init_database()

        service_store = ServiceStore(
            dummy_request(dbsession=self.session))

        self.reg = Registry(servicestore=service_store)

    def test_register_service_and_unregister_it(self):
        service = {'url': 'http://localhost/wps', 'name': 'test_emu',
                   'type': 'wps', 'public': False, 'auth': 'token', 'verify': True,
                   'purl': 'http://myservice/wps'}
        # register
        resp = self.reg.register_service(
            service['name'],
            service['url'],
            service)
        assert resp == service

        # get by name
        resp = self.reg.get_service_by_name(service['name'])
        assert resp == service

        # list
        resp = self.reg.list_services()
        assert resp == [service]

        # unregister
        resp = self.reg.unregister_service(service['name'])
        assert resp is True

        # clear
        resp = self.reg.clear_services()
        assert resp is True
