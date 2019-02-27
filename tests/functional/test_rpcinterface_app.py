"""
Testing the Twithcer XML-RPC interface.
"""
import pytest
import unittest
import webtest
import pyramid.testing

from .common import call_FUT
from .common import setup_with_mongodb
from .common import setup_mongodb_tokenstore
from .common import setup_mongodb_servicestore
from .common import WPS_TEST_SERVICE


class XMLRPCInterfaceAppTest(unittest.TestCase):

    def setUp(self):
        config = setup_with_mongodb()
        self.token = setup_mongodb_tokenstore(config)
        setup_mongodb_servicestore(config)
        config.include('twitcher.rpcinterface')
        self.app = webtest.TestApp(config.make_wsgi_app())

    def tearDown(self):
        pyramid.testing.tearDown()

    @pytest.mark.online
    def test_generate_token_and_revoke_it(self):
        # gentoken
        resp = call_FUT(self.app, 'generate_token', (1, {}))
        assert 'access_token' in resp
        assert 'expires_at' in resp
        # revoke
        resp = call_FUT(self.app, 'revoke_token', (resp['access_token'],))
        assert resp is True
        # revoke all
        resp = call_FUT(self.app, 'revoke_all_tokens', ())
        assert resp is True

    @pytest.mark.online
    def test_register_service_and_unregister_it(self):
        service = {'url': WPS_TEST_SERVICE, 'name': 'test_emu',
                   'type': 'wps', 'public': False, 'auth': 'token',
                   'verify': True, 'purl': 'http://purl/wps'}
        # register
        resp = call_FUT(self.app, 'register_service', (
            service['url'],
            service,
            False))
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

        # clear
        resp = call_FUT(self.app, 'clear_services', ())
        assert resp is True
