"""
Based on unitests in https://github.com/wndhydrnt/python-oauth2/tree/master/oauth2/test
"""

import pytest
import unittest

from twitcher.datatype import AccessToken, Service
from twitcher import models
from twitcher.utils import expires_at


class AccessTokenTestCase(unittest.TestCase):

    def test_access_token(self):
        access_token = AccessToken(token='abcdef', expires_at=expires_at(hours=1))
        assert access_token.token == 'abcdef'
        assert access_token.expires_in > 0
        assert access_token.expires_in <= 3600
        assert access_token.is_expired() is False
        assert access_token.params['access_token'] == 'abcdef'
        assert 'expires_at' in access_token.params

    def test_missing_token(self):
        with pytest.raises(TypeError):
            AccessToken()

    def test_invalid_access_token(self):
        access_token = AccessToken(token='abcdef', expires_at=expires_at(hours=-1))
        assert access_token.expires_in == 0
        assert access_token.is_expired() is True

    def test_access_token_from_model(self):
        access_token = AccessToken.from_model(
            models.AccessToken(token='abc', expires_at=expires_at(hours=2)))
        assert access_token.token == 'abc'
        assert access_token.expires_at > 0


class ServiceTestCase(unittest.TestCase):
    def test_service_with_url_only(self):
        service = Service(name="test_wps", url='http://nowhere/wps')
        assert service.url == 'http://nowhere/wps'
        assert service.name == 'test_wps'
        assert service.has_purl() is False

    def test_missing_url_or_name(self):
        with pytest.raises(TypeError):
            Service(name="test")
        with pytest.raises(TypeError):
            Service(url='http://nowhere/wps')

    def test_service_with_name(self):
        service = Service(url='http://nowhere/wps', name="test_wps")
        assert service.url == 'http://nowhere/wps'
        assert service.name == 'test_wps'
        assert service.has_purl() is False

    def test_service_params(self):
        service = Service(url='http://nowhere/wps', name="test_wps", purl='http://myservice/wps')
        assert service.params == {'name': 'test_wps',
                                  'public': False,
                                  'auth': 'token',
                                  'type': 'WPS',
                                  'url': 'http://nowhere/wps',
                                  'verify': True,
                                  'purl': 'http://myservice/wps'}
        assert service.has_purl() is True

    def test_service_from_model(self):
        service = Service.from_model(
            models.Service(name='test_wps', url='http://nowhere/wps'))
        assert service.name == 'test_wps'
        assert service.url == 'http://nowhere/wps'
        assert service.type == 'WPS'
        assert service.auth == 'token'
        assert service.public is False
        assert service.verify is True
        assert service.purl == ''
