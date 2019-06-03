from .common import BaseTest

from twitcher import main, __version__
from twitcher.adapter.default import TWITCHER_ADAPTER_DEFAULT
from twitcher.frontpage import INFORMATION_PATH, VERSIONS_PATH

from pyramid import testing
from webtest import TestApp
import unittest


class TestFrontpageAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.settings = {
            'twitcher.url': 'localhost',
            'sqlalchemy.url': 'sqlite:///:memory:'
        }
        cls.config = testing.setUp(settings=cls.settings)
        cls.app = TestApp(main({}, **cls.config.registry.settings))

    def test_get_frontpage(self):
        resp = self.app.get('/')
        assert resp.status_code == 200
        assert resp.json['message'] == 'Twitcher Frontpage'
        assert resp.json['information_uri'] == self.settings['twitcher.url'] + INFORMATION_PATH
        assert resp.json['versions_uri'] == self.settings['twitcher.url'] + VERSIONS_PATH

    def test_get_info(self):
        resp = self.app.get(INFORMATION_PATH)
        assert resp.status_code == 200
        assert resp.json['author'] == __version__.__author__
        assert resp.json['doc'] == __version__.__doc__
        assert resp.json['email'] == __version__.__email__
        assert resp.json['package'] == 'twitcher'
        assert resp.json['version'] == __version__.__version__

    def test_get_versions(self):
        resp = self.app.get(VERSIONS_PATH)
        assert resp.status_code == 200
        assert isinstance(resp.json, list)
        assert resp.json[0]['name'] == 'Twitcher'
        assert resp.json[0]['type'] == 'application'
        assert resp.json[0]['version'] == __version__.__version__
        assert resp.json[1]['name'] == TWITCHER_ADAPTER_DEFAULT
        assert resp.json[1]['type'] == 'adapter'
        assert resp.json[1]['version'] == __version__.__version__
