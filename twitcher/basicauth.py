"""
Basic Authentication.

Taken from:
https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/auth/basic.html
"""
from pyramid.settings import asbool
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Authenticated,
    forget)
from pyramid.view import forbidden_view_config

from twitcher.utils import get_settings


@forbidden_view_config()
def forbidden_view(request):
    if request.authenticated_userid is None:
        response = HTTPUnauthorized()
        response.headers.update(forget(request))

    # user is logged in but doesn't have permissions, reject wholesale
    else:
        response = HTTPForbidden()
    return response


def check_credentials(username, password, request):
    settings = request.registry.settings
    _username = settings['twitcher.username']
    _password = settings['twitcher.password']
    if username == _username and password == _password:
        # an empty list is enough to indicate logged-in
        return []


class Root:
    # dead simple, give everyone who is logged in any permission
    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )


def includeme(config):
    settings = get_settings(config)
    if asbool(settings.get('twitcher.basicauth', True)):
        authn_policy = BasicAuthAuthenticationPolicy(check=check_credentials, debug=True)
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
        config.set_authentication_policy(authn_policy)
        config.set_root_factory(lambda request: Root())
