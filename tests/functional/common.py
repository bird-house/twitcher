from pyramid import testing

from twitcher.tokengenerator import tokengenerator_factory
from twitcher.store import tokenstore_factory
from twitcher.store import servicestore_factory

import six
if six.PY2:
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib


WPS_TEST_SERVICE = 'http://localhost:5000/wps'


def setup_with_mongodb():
    settings = {'mongodb.host': '127.0.0.1', 'mongodb.port': '27027', 'mongodb.db_name': 'twitcher_test'}
    config = testing.setUp(settings=settings)
    return config


def setup_mongodb_tokenstore(config):
    store = tokenstore_factory(config.registry)
    generator = tokengenerator_factory(config.registry)
    store.clear_tokens()
    access_token = generator.create_access_token()
    store.save_token(access_token)
    return access_token.token


def setup_mongodb_servicestore(config):
    store = servicestore_factory(config.registry)
    store.clear_services()


def call_FUT(app, method, params):
    if six.PY2:
        xml = xmlrpclib.dumps(params, methodname=method)
    else:
        xml = xmlrpclib.dumps(params, methodname=method).encode('utf-8')
    print(xml)
    resp = app.post('/RPC2', content_type='text/xml', params=xml)
    assert resp.status_int == 200
    assert resp.content_type == 'text/xml'
    print(resp.body)
    return xmlrpclib.loads(resp.body)[0][0]
