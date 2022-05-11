import os
import unittest
import json

from pyramid import testing

import transaction

RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))

WPS_CAPS_EMU_XML = os.path.join(RESOURCES_PATH, 'wps_caps_emu.xml')
WMS_CAPS_NCWMS2_111_XML = os.path.join(RESOURCES_PATH, 'wms_caps_ncwms2_111.xml')
WMS_CAPS_NCWMS2_130_XML = os.path.join(RESOURCES_PATH, 'wms_caps_ncwms2_130.xml')

WPS_TEST_SERVICE = os.getenv("TWITCHER_TEST_WPS", "http://localhost:5000/wps")


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
        'twitcher.username': 'testuser',
        'twitcher.password': 'testpassword',
        'twitcher.token.type': 'custom_token',
        'twitcher.token.secret': 'testsecret',
    }

    def setUp(self):
        self.config = testing.setUp(settings=self.settings)
        self.config.include('twitcher.models')
        settings = self.config.get_settings()

        from twitcher.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from twitcher.models.meta import Base
        Base.metadata.create_all(self.engine)
        # add test client
        from twitcher import models
        self.session.add(models.Client(client_id='dev', client_secret='dev'))

    def create_token(self):
        resp = self.app.get('/oauth/token?grant_type={}&client_id={}&client_secret={}'.format(
            'client_credentials',
            'dev',
            'dev'))
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        resp.mustcontain('access_token')
        return json.loads(resp.text)['access_token']

    def tearDown(self):
        from twitcher.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)
