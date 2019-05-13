import webtest

import xmlrpc.client as xmlrpclib

from .. common import BaseTest, WPS_TEST_SERVICE, dummy_request

from twitcher.utils import expires_at
from twitcher.datatype import AccessToken, Service
from twitcher.store import AccessTokenStore, ServiceStore

TEST_TOKEN = 'test_token_123'


def call_FUT(app, method, params):
    xml = xmlrpclib.dumps(params, methodname=method).encode('utf-8')
    print(xml)
    resp = app.post('/RPC2', content_type='text/xml', params=xml)
    assert resp.status_int == 200
    assert resp.content_type == 'text/xml'
    print(resp.body)
    return xmlrpclib.loads(resp.body)[0][0]


class FunctionalTest(BaseTest):
    def test_app(self):
        app = webtest.TestApp(
            self.config.make_wsgi_app(),
            extra_environ={'db.session': self.session, 'tm.active': True})
        return app

    def init_store(self):
        # add public wps service
        service_store = ServiceStore(
            dummy_request(dbsession=self.session))
        service_store.save_service(
            Service(
                name="wps",
                url=WPS_TEST_SERVICE,
                type="wps",
                public=True,
                auth='token',
                verify=False,
                purl="http://purl/wps"))
        # add secured wps service
        service_store.save_service(
            Service(
                name="wps_secured",
                url=WPS_TEST_SERVICE,
                type="wps",
                public=False,
                auth='token',
                verify=False,
                purl="http://purl/wps_secured"))
        # generate token
        token_store = AccessTokenStore(
            dummy_request(dbsession=self.session))
        token_store.save_token(
            AccessToken(token=TEST_TOKEN, expires_at=expires_at(hours=1)))
