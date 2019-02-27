"""
Based on tests from:

* https://github.com/geopython/pywps/tree/master/tests
* https://github.com/mmerickel/pyramid_services/tree/master/pyramid_services/tests
* http://webtest.pythonpaste.org/en/latest/
* http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html
"""
import pytest
import unittest
import webtest
import pyramid.testing

from .common import call_FUT
from .common import setup_with_mongodb, setup_mongodb_tokenstore
from .common import WPS_TEST_SERVICE


class WpsAppTest(unittest.TestCase):

    def setUp(self):
        config = setup_with_mongodb()
        self.token = setup_mongodb_tokenstore(config)
        config.include('twitcher.rpcinterface')
        config.include('twitcher.owsproxy')
        config.include('twitcher.tweens')
        self.app = webtest.TestApp(config.make_wsgi_app())
        self.wps_path = '/ows/proxy/test_emu'
        # register
        service = {'url': WPS_TEST_SERVICE, 'name': 'test_emu',
                   'type': 'wps', 'public': True, 'purl': 'http://purl/wps'}
        try:
            call_FUT(self.app, 'register_service', (
                service['url'],
                service,
                False))
        except Exception:
            pass

    def tearDown(self):
        pyramid.testing.tearDown()

    @pytest.mark.online
    def test_getcaps(self):
        url = '{}?service=wps&request=getcapabilities'
        resp = self.app.get(url.format(self.wps_path))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:Capabilities>')

    @pytest.mark.online
    def test_getcaps_with_invalid_token(self):
        url = '{}?service=wps&request=getcapabilities&access_token=invalid'
        resp = self.app.get(url.format(self.wps_path))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:Capabilities>')

    @pytest.mark.online
    def test_describeprocess(self):
        url = '{}?service=wps&request=describeprocess&version=1.0.0&identifier=hello'
        resp = self.app.get(url.format(self.wps_path))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:ProcessDescriptions>')

    @pytest.mark.online
    def test_describeprocess_with_invalid_token(self):
        url = '{}?service=wps&request=describeprocess&version=1.0.0&identifier=hello&access_token=invalid'
        resp = self.app.get(url.format(self.wps_path))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:ProcessDescriptions>')

    @pytest.mark.online
    @pytest.mark.skip(reason="not configured")
    def test_execute_not_allowed(self):
        url = '{}?service=wps&request=execute&version=1.0.0&identifier=hello&datainputs=name=tux'
        resp = self.app.get(url.format(self.wps_path))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        print(resp.body)
        resp.mustcontain('<Exception exceptionCode="NoApplicableCode" locator="AccessForbidden">')

    @pytest.mark.online
    def test_execute_allowed(self):
        url = "{}?service=wps&request=execute&version=1.0.0&identifier=hello&datainputs=name=tux&access_token={}"
        resp = self.app.get(url.format(self.wps_path, self.token))
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        print(resp.body)
        resp.mustcontain(
            '<wps:ProcessSucceeded>PyWPS Process Say Hello finished</wps:ProcessSucceeded>')
