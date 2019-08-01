# coding: utf-8
"""
twitcher.models.oauth
---------------------

The model is inspired by the flask-oauthlib example:
https://flask-oauthlib.readthedocs.io/en/latest/oauth2.html
"""

from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base


class Client(Base):
    __tablename__ = 'client'
    # human readable name, not required
    name = Column(String(40))
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True, index=True, nullable=False)
    _redirect_uris = Column(Text)
    default_scope = Column(Text, default='compute')

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        if self.redirect_uris:
            return self.redirect_uris[0]
        return ''

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['client_credentials']


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    client_id = Column(
        String(40), ForeignKey('client.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    client = relationship('Client')
    token_type = Column(String(40))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    expires = Column(DateTime)
    scope = Column(Text)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in', None)
        if expires_in is not None:
            self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []
