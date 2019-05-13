"""
Testing the Twitcher XML-RPC interface.
"""
import pytest

from .. common import WPS_TEST_SERVICE
from .base import FunctionalTest, call_FUT


class XMLRPCInterfaceAppTest(FunctionalTest):

    def setUp(self):
        super(XMLRPCInterfaceAppTest, self).setUp()
        self.init_database()
        self.init_store()

        self.config.include('twitcher.rpcinterface')
        self.app = self.test_app()

    def test_generate_token_and_revoke_it(self):
        # gentoken
        resp = call_FUT(self.app, 'generate_token', (1, ))
        assert 'access_token' in resp
        assert 'expires_at' in resp
        # revoke
        resp = call_FUT(self.app, 'revoke_token', (resp['access_token'],))
        assert resp is True
        # revoke all
        resp = call_FUT(self.app, 'revoke_all_tokens', ())
        assert resp is True

    def test_register_service_and_unregister_it(self):
        service = {'url': WPS_TEST_SERVICE, 'name': 'test_wps',
                   'type': 'wps', 'public': False, 'auth': 'token',
                   'verify': True, 'purl': 'http://purl/wps'}

        # clear
        resp = call_FUT(self.app, 'clear_services', ())
        assert resp is True

        # register
        resp = call_FUT(self.app, 'register_service', (
            service['name'],
            service['url'],
            service))
        assert resp == service

        # get by name
        resp = call_FUT(self.app, 'get_service_by_name', (service['name'],))
        assert resp == service

        # get by url
        resp = call_FUT(self.app, 'get_service_by_url', (service['url'],))
        assert resp == service

        # list
        resp = call_FUT(self.app, 'list_services', ())
        assert resp == [service]

        # unregister
        resp = call_FUT(self.app, 'unregister_service', (service['name'],))
        assert resp is True
