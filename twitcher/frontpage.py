from twitcher.adapter import get_adapter_factory
from twitcher.utils import get_twitcher_url, is_json_serializable
from twitcher import __version__
from pyramid.view import view_config

VERSIONS_PATH = '/versions'
INFORMATION_PATH = '/info'


@view_config(route_name='frontpage', renderer='json')
def frontpage(request):
    return {
        'message': 'Twitcher Frontpage',
        'information_uri': get_twitcher_url(request) + INFORMATION_PATH,
        'versions_uri': get_twitcher_url(request) + VERSIONS_PATH,
    }


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
