"""
Based on unitests in https://github.com/wndhydrnt/python-oauth2/tree/master/oauth2/test
"""

import pytest
from .common import BaseTest, dummy_request

from twitcher.utils import expires_at
from twitcher.store import AccessTokenStore, ServiceStore
from twitcher.datatype import AccessToken, Service


class AccessTokenStoreTestCase(BaseTest):
    def setUp(self):
        super(AccessTokenStoreTestCase, self).setUp()
        self.init_database()

        self.token_store = AccessTokenStore(
            dummy_request(dbsession=self.session))

    def test_token_store(self):
        self.token_store.save_token(
            AccessToken(token="abc", expires_at=expires_at(hours=1)))
        token = self.token_store.fetch_by_token(token='abc')
        assert token.token == 'abc'
        self.token_store.delete_token(token='abc')
        self.token_store.clear_tokens()


class ServiceStoreTestCase(BaseTest):
    def setUp(self):
        super(ServiceStoreTestCase, self).setUp()
        self.init_database()

        self.service_store = ServiceStore(
            dummy_request(dbsession=self.session))

    def test_service_store(self):
        self.service_store.save_service(
            Service(
                name="flamingo",
                url="http://somewhere.over.the/ocean",
                type="wps",
                public=False,
                auth='token',
                verify=True,
                purl="http://purl/wps")
        )
        service = self.service_store.fetch_by_name(name='flamingo')
        assert service.name == 'flamingo'
        service = self.service_store.fetch_by_url(url='http://somewhere.over.the/ocean')
        assert service.url == 'http://somewhere.over.the/ocean'
        services = self.service_store.list_services()
        assert len(services) == 1
        self.service_store.delete_service(name='flamingo')
        self.service_store.clear_services()

    def test_service_store_insert_or_update(self):
        self.service_store.save_service(
            Service(
                name="albatross",
                url="http://somewhere.over.the/ocean",
                type="wps",
                public=False,
                auth='token',
                verify=True,
                purl="http://purl/wps")
        )
        # update
        self.service_store.save_service(
            Service(
                name="albatross",
                url="http://somewhere.over.the/ocean",
                type="wps",
                public=True,
                auth='token',
                verify=True,
                purl="http://purl/wps")
        )
        services = self.service_store.list_services()
        assert len(services) == 1
        self.service_store.clear_services()
