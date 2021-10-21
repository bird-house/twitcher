"""
Based on unitests in https://github.com/wndhydrnt/python-oauth2/tree/master/oauth2/test
"""

from .common import BaseTest, dummy_request

from twitcher.store import ServiceStore


class ServiceStoreTestCase(BaseTest):
    def setUp(self):
        super(ServiceStoreTestCase, self).setUp()
        self.init_database()

        self.service_store = ServiceStore(
            dummy_request(dbsession=self.session))

    def test_service_store(self):
        self.service_store.save_service(
            name="flamingo",
            url="http://somewhere.over.the/ocean",
            type="wps",
            auth='token',
            verify=True,
            purl="http://purl/wps"
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
            name="albatross",
            url="http://somewhere.over.the/ocean",
            type="wps",
            auth='token',
            verify=True,
            purl="http://purl/wps"
        )
        # update
        self.service_store.save_service(
            name="albatross",
            url="http://somewhere.over.the/ocean",
            type="wps",
            auth='token',
            verify=True,
            purl="http://purl/wps"
        )
        services = self.service_store.list_services()
        assert len(services) == 1
        self.service_store.clear_services()
