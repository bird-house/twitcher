import unittest

from twitcher.datatype import AccessToken
from twitcher.store.memory import MemoryTokenStore

from twitcher.datatype import Service
from twitcher.store.memory import MemoryServiceStore


class MemoryTokenStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.access_token_data = {"token": "xyz",
                                  "data": {"name": "test"},
                                  }
        self.test_store = MemoryTokenStore()

    def test_save_token_and_fetch_by_token(self):
        access_token = AccessToken(**self.access_token_data)

        assert self.test_store.save_token(access_token)
        assert self.test_store.fetch_by_token(access_token.token) == access_token


class MemoryServiceStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.service_data = {'url': 'http://localhost:5000/wps',
                             'name': 'emu',
                             'purl': 'http://myservice/wps',
                             'public': False,
                             'auth': 'token',
                             'type': 'WPS',
                             'verify': True,
                             }
        self.test_store = MemoryServiceStore()

    def test_save_service_and_fetch_service(self):
        service = Service(**self.service_data)

        assert self.test_store.save_service(service)
        assert self.test_store.fetch_by_name(service.name) == service
        assert self.test_store.fetch_by_url(service.url) == service
