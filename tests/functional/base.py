import webtest

from .. common import BaseTest, WPS_TEST_SERVICE, dummy_request

from twitcher.store import ServiceStore


class FunctionalTest(BaseTest):
    def get_test_app(self):
        app = webtest.TestApp(
            self.config.make_wsgi_app(),
            extra_environ={'db.session': self.session, 'tm.active': True})
        return app

    def init_store(self):
        # add public wps service
        service_store = ServiceStore(
            dummy_request(dbsession=self.session))
        service_store.save_service(
            name="wps",
            url=WPS_TEST_SERVICE,
            type="wps",
            auth='token',
            verify=False,
            purl="http://purl/wps")
        # add secured wps service
        service_store.save_service(
            name="wps_secured",
            url=WPS_TEST_SERVICE,
            type="wps",
            auth='token',
            verify=False,
            purl="http://purl/wps_secured")
