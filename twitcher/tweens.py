from pyramid.settings import asbool
from pyramid.tweens import EXCVIEW

from twitcher.adapter import get_adapter_factory
from twitcher.owsexceptions import OWSException, OWSNoApplicableCode

import logging
LOGGER = logging.getLogger("TWITCHER")


def includeme(config):
    settings = config.registry.settings

    if asbool(settings.get('twitcher.ows_security', True)):
        LOGGER.info('Add OWS security tween')
        config.add_tween(OWS_SECURITY, under=EXCVIEW)


def ows_security_tween_factory(handler, registry):
    """A tween factory which produces a tween which raises an exception
    if access to OWS service is not allowed."""

    def ows_security_tween(request):
        try:
            adapter = get_adapter_factory(request)
            security = adapter.owssecurity_factory(request)
            security.check_request(request)
            return handler(request)
        except OWSException as err:
            LOGGER.warning("security check failed.")
            return err
        except Exception as err:
            LOGGER.exception("unknown error")
            return OWSNoApplicableCode("{}".format(err))

    return ows_security_tween


OWS_SECURITY = 'twitcher.tweens.ows_security_tween_factory'
