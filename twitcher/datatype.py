"""
Definition of service and token types.
"""

import time

from pyramid.settings import asbool

from twitcher.utils import now_secs, is_valid_url
from twitcher.exceptions import AccessTokenNotFound


class Service(dict):
    """
    Dictionary that contains OWS services.
    It always has the ``'url'`` and ``'name'`` key.

    TODO: Should this be part of the model?
    TODO: If the field is accessed with service['public'] instead of service.public,
    we get different values. We could override `__getattr__`.
    """
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        if 'name' not in self:
            raise TypeError("'name' is required")
        if 'url' not in self:
            raise TypeError("'url' is required")
        if self.get('public') is None:
            self['public'] = False
        if self.get('verify') is None:
            self['verify'] = True

    @property
    def url(self):
        """Service URL."""
        return self['url']

    @property
    def name(self):
        """Service name."""
        return self['name']

    @property
    def type(self):
        """Service type."""
        return self.get('type') or 'WPS'

    @property
    def purl(self):
        """Service optional public URL (purl)."""
        return self.get('purl') or ''

    def has_purl(self):
        """Return true if we have a valid public URL (purl)."""
        return is_valid_url(self.purl)

    @property
    def public(self):
        """Flag if service has public access."""
        # TODO: public access can be set via auth parameter.
        return asbool(self.get('public', False))

    @property
    def auth(self):
        """Authentication method: public, token, cert."""
        return self.get('auth') or 'token'

    @property
    def verify(self):
        """Verify ssl service certificate."""
        return asbool(self.get('verify', True))

    @property
    def params(self):
        return {
            'url': self.url,
            'name': self.name,
            'type': self.type,
            'purl': self.purl,
            'public': self.public,
            'auth': self.auth,
            'verify': self.verify}

    @classmethod
    def from_model(cls, model):
        instance = cls(
            url=model.url,
            name=model.name,
            type=model.type,
            purl=model.purl,
            public=model.public,
            auth=model.auth,
            verify=model.verify)
        return instance

    def __str__(self):
        return self.name

    def __repr__(self):
        cls = type(self)
        repr_ = dict.__repr__(self)
        return '{0}.{1}({2})'.format(cls.__module__, cls.__name__, repr_)


class AccessToken(dict):
    """
    Dictionary that contains access token. It always has ``'token'`` key.

    TODO: Should this be part of the model?
    """

    def __init__(self, *args, **kwargs):
        super(AccessToken, self).__init__(*args, **kwargs)
        if 'token' not in self:
            raise TypeError("'token' is required")

    @property
    def token(self):
        """Access token string."""
        return self['token']

    @property
    def expires_at(self):
        return int(self.get("expires_at") or 0)

    @property
    def expires_in(self):
        """
        Returns the time until the token expires.
        :return: The remaining time until expiration in seconds or 0 if the
                 token has expired.
        """
        time_left = self.expires_at - now_secs()

        if time_left > 0:
            return time_left
        return 0

    def is_expired(self):
        """
        Determines if the token has expired.
        :return: `True` if the token has expired. Otherwise `False`.
        """
        if self.expires_at is None:
            return True

        if self.expires_in > 0:
            return False

        return True

    @property
    def data(self):
        return self.get('data') or {}

    @property
    def params(self):
        return {'access_token': self.token, 'expires_at': self.expires_at}

    @classmethod
    def from_model(cls, model):
        instance = cls(
            token=model.token,
            expires_at=model.expires_at)
        return instance

    def __str__(self):
        return self.token

    def __repr__(self):
        cls = type(self)
        repr_ = dict.__repr__(self)
        return '{0}.{1}({2})'.format(cls.__module__, cls.__name__, repr_)
