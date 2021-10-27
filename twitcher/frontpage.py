from twitcher.adapter import get_adapter_factory
from twitcher.utils import get_settings, get_twitcher_url, is_json_serializable
from twitcher.oauth2 import CLIENT_APP_ENDPOINT, TOKEN_ENDPOINT
from twitcher.owsproxy import owsproxy_base_url
from twitcher import __version__
from pyramid.settings import asbool
from pyramid.view import view_config

VERSIONS_PATH = '/versions'
INFORMATION_PATH = '/info'


@view_config(route_name='frontpage', renderer='json')
def frontpage(request):
    url = get_twitcher_url(request)
    body = {
        'message': 'Twitcher Frontpage',
        'information_uri': url + INFORMATION_PATH,
        'versions_uri': url + VERSIONS_PATH,
        'services_uri': "{}/services".format(url),
        'client_uri': "{}{}".format(url, CLIENT_APP_ENDPOINT),
        'token_uri': "{}{}".format(url, TOKEN_ENDPOINT),
        'openapi_uri': "{}/__api__".format(url),
    }
    settings = get_settings(request)
    if asbool(settings.get('twitcher.ows_proxy', True)):
        body["owsproxy_uri"] = owsproxy_base_url(request) + "/proxy"
    else:
        body["owsproxy_uri"] = None
    return body


@view_config(route_name='information', renderer='json')
def information(request):
    """List API information."""
    return dict(
        (i.replace('__', ''), getattr(__version__, i))
        for i in dir(__version__)
        if i not in ['__file__', '__name__', '__cached__'] and is_json_serializable(getattr(__version__, i))
    )


@view_config(route_name='versions', renderer='json')
def versions(request):
    """List version details of components used by the API."""
    adapter_version = get_adapter_factory(request).describe_adapter()
    adapter_version['type'] = 'adapter'
    twitcher_version = {
        'name': 'Twitcher',
        'version': __version__.__version__,
        'type': 'application',
    }
    return [twitcher_version, adapter_version]


def includeme(config):
    config.add_route('frontpage', '/')
    config.add_route('information', INFORMATION_PATH)
    config.add_route('versions', VERSIONS_PATH)
