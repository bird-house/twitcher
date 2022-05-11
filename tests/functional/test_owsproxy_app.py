"""
Run tests OWSProxy tests with external WPS.

Please start `Emu WPS <https://emu.readthedocs.io/en/latest/>`_ on port 5000:

http://localhost:5000/wps
"""

import pytest

from .base import FunctionalTest


class OWSProxyAppTest(FunctionalTest):

    def setUp(self):
        super(OWSProxyAppTest, self).setUp()
        self.init_database()
        self.init_store()

        self.config.include('twitcher.owsproxy')
        self.app = self.get_test_app()

    @pytest.mark.online
    def test_getcaps(self):
        resp = self.app.get('/ows/proxy/wps?service=wps&request=getcapabilities')
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:Capabilities>')

    @pytest.mark.online
    def test_describeprocess(self):
        resp = self.app.get(
            '/ows/proxy/wps?service=wps&request=describeprocess&version=1.0.0&identifier=dummyprocess')
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        resp.mustcontain('</wps:ProcessDescriptions>')

    @pytest.mark.online
    def test_execute_allowed(self):
        access_token = self.create_token()
        url = "/ows/proxy/wps_secured?service=wps&request=execute&version=1.0.0&identifier=hello&DataInputs=name=tux&access_token={}".format(access_token)  # noqa
        resp = self.app.get(url)
        assert resp.status_code == 200
        assert resp.content_type == 'text/xml'
        print(resp.body)
        resp.mustcontain(
            '<wps:ProcessSucceeded>PyWPS Process Say Hello finished</wps:ProcessSucceeded>')
