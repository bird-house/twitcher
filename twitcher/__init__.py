from pyramid.config import Configurator

from .__version__ import __author__, __email__, __version__


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # include twitcher components
        config.include('.models')
        config.include('.config')
        config.include('.frontpage')
        config.include('.rpcinterface')
        config.include('.owsproxy')
        # tweens/middleware
        # TODO: maybe add tween for exception handling or use unknown_failure view
        config.include('twitcher.tweens')
        config.scan()
    return config.make_wsgi_app()
