from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('twitcher.models')
        config.include('twitcher.frontpage')
        config.include('twitcher.oauth2')
        config.include('twitcher.api')
        config.include('twitcher.owsproxy')
        config.scan()
    return config.make_wsgi_app()
