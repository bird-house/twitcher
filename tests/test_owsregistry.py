"""
Testing the OWS Registry.
"""

from .common import BaseTest, dummy_request

from twitcher.store import ServiceStore
from twitcher.owsregistry import OWSRegistry


class OWSRegistryTest(BaseTest):

    def setUp(self):
        super(OWSRegistryTest, self).setUp()
        self.init_database()

        service_store = ServiceStore(
            dummy_request(dbsession=self.session))

        self.reg = OWSRegistry(servicestore=service_store)

    def test_register_service_and_unregister_it(self):
        service = {
            'url': 'http://localhost/wps',
            'name': 'test_emu',
            'type': 'wps',
            'auth': 'token',
            'public': False,
            'verify': True,
            'purl': 'http://myservice/wps'}
        # register
        resp = self.reg.register_service(**service)
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
