from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # include twitcher components
        config.include('twitcher.models')
        config.include('twitcher.frontpage')
        config.include('twitcher.rpcinterface')
        config.include('twitcher.owsproxy')
        # tweens/middleware
        # TODO: maybe add tween for exception handling or use unknown_failure view
        config.include('twitcher.tweens')
        config.scan()
    return config.make_wsgi_app()
