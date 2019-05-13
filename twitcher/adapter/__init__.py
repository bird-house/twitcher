from twitcher.adapter.default import DefaultAdapter, AdapterInterface
from twitcher.utils import get_settings

from inspect import isclass
from typing import TYPE_CHECKING

import logging
LOGGER = logging.getLogger("TWITCHER")

if TYPE_CHECKING:
    from twitcher.store import AccessTokenStoreInterface, ServiceStoreInterface
    from twitcher.owssecurity import OWSSecurityInterface
    from twitcher.typedefs import AnySettingsContainer
    from pyramid.request import Request
    from typing import AnyStr, Type, Union


TWITCHER_ADAPTER_DEFAULT = 'default'


def import_adapter(name):
    # type: (AnyStr) -> Type[AdapterInterface]
    """Attempts import of the class specified by python string ``package.module.class``."""
    components = name.split('.')
    mod_name = components[0]
    mod = __import__(mod_name)
    for comp in components[1:]:
        if not hasattr(mod, comp):
            mod_name = '{mod}.{sub}'.format(mod=mod_name, sub=comp)
            mod = __import__(mod_name, fromlist=[mod_name])
            continue
        mod = getattr(mod, comp)
    if not isclass(mod) or not issubclass(mod, AdapterInterface):
        raise TypeError("Invalid reference is not of type '{}.{}'."
                        .format(AdapterInterface.__module__, AdapterInterface.__name__))
    return mod


def get_adapter_type(container):
    # type: (AnySettingsContainer) -> AnyStr
    """Finds the specified adapter from configuration settings."""
    settings = get_settings(container)
    return str(settings.get('twitcher.adapter', TWITCHER_ADAPTER_DEFAULT.lower()))


def get_adapter_factory(container):
    # type: (AnySettingsContainer) -> AdapterInterface
    """
    Creates an adapter interface according to `twitcher.adapter` setting.
    By default the :class:`twitcher.adapter.default.DefaultAdapter` implementation will be used.
    """
    adapter_type = get_adapter_type(container)
    if adapter_type != TWITCHER_ADAPTER_DEFAULT:
        try:
            adapter_class = import_adapter(adapter_type)
        except Exception as e:
            LOGGER.error("Adapter '{!s}' raised an exception during import : '{!r}'".format(adapter_type, e))
            raise
        try:
            LOGGER.info("Using adapter: '{!r}'".format(adapter_class))
            return adapter_class(container)
        except Exception as e:
            LOGGER.error("Adapter '{!s}' raised an exception during instantiation : '{!r}'".format(adapter_type, e))
            raise
    return DefaultAdapter(container)


def get_adapter_store_factory(
        adapter,        # type: AdapterInterface
        store_name,     # type: AnyStr
        request,        # type: Request
):                      # type: (...) -> Union[AccessTokenStoreInterface, ServiceStoreInterface, OWSSecurityInterface]
    """
    Retrieves the adapter store by name if it is defined.

    If another adapter than :class:`twitcher.adapter.default.DefaultAdapter` is provided, and that the store
    cannot be found with it, `DefaultAdapter` is used as fallback to find the "default" store implementation.

    :returns: found store.
    :raises NotImplementedError: when the store is not available from the adapter.
    :raises Exception: when store instance was found but generated an error on creation.
    """
    try:
        store = getattr(adapter, store_name)
        return store(request)
    except NotImplementedError:
        if isinstance(adapter, DefaultAdapter):
            LOGGER.exception("Adapter 'DefaultAdapter' doesn't implement '{1!r}', no way to recover."
                             .format(adapter, store_name))
            raise
        LOGGER.warning("Adapter '{0!r}' doesn't implement '{1!r}', falling back to 'DefaultAdapter' implementation."
                       .format(adapter, store_name))
        return get_adapter_store_factory(DefaultAdapter(request), store_name, request)
    except Exception as e:
        LOGGER.error("Adapter '{0!r}' raised an exception while instantiating '{1!r}' : '{2!r}'"
                     .format(adapter, store_name, e))
        raise
