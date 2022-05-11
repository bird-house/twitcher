"""
Testing the Twitcher Rest interface.
"""
import pytest

from .base import FunctionalTest


class APITest(FunctionalTest):

    def setUp(self):
        super(APITest, self).setUp()
        self.init_database()
        self.init_store()

        self.config.include('twitcher.api')
        self.app = self.get_test_app()

    @pytest.mark.skip(reason="not working")
    def test_register_service_and_unregister_it(self):
        # clear
        resp = self.app.get('/services/clear')
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        assert resp is True
