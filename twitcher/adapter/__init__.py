from twitcher.adapter.default import DefaultAdapter, AdapterInterface
from twitcher.warning import UnsupportedOperationWarning
from twitcher.utils import get_settings
from inspect import isclass
from typing import TYPE_CHECKING
import warnings
import logging
if TYPE_CHECKING:
    from twitcher.store.base import AccessTokenStore, ServiceStore
    from twitcher.owssecurity import OWSSecurityInterface
    from twitcher.typedefs import AnySettingsContainer
    from typing import AnyStr, Type, Union
LOGGER = logging.getLogger("TWITCHER")

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
            return adapter_class()
        except Exception as e:
            LOGGER.error("Adapter '{!s}' raised an exception during instantiation : '{!r}'".format(adapter_type, e))
            raise
    return DefaultAdapter()


def get_adapter_store_factory(
        adapter,        # type: AdapterInterface
        store_name,     # type: AnyStr
        container,      # type: AnySettingsContainer
):                      # type: (...) -> Union[AccessTokenStore, ServiceStore, OWSSecurityInterface]
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
        return store(container)
    except NotImplementedError:
        if isinstance(adapter, DefaultAdapter):
            LOGGER.exception("Adapter 'DefaultAdapter' doesn't implement '{1!r}', no way to recover."
                             .format(adapter, store_name))
            raise
        warnings.warn("Adapter '{0!r}' doesn't implement '{1!r}', falling back to 'DefaultAdapter' implementation."
                      .format(adapter, store_name), UnsupportedOperationWarning)
        return get_adapter_store_factory(DefaultAdapter(), store_name, container)
    except Exception as e:
        LOGGER.error("Adapter '{0!r}' raised an exception while instantiating '{1!r}' : '{2!r}'"
                     .format(adapter, store_name, e))
        raise


def tokenstore_factory(container):
    # type: (AnySettingsContainer) -> AccessTokenStore
    """Shortcut method to retrieve the AccessTokenStore from the selected AdapterInterface from settings."""
    adapter = get_adapter_factory(container)
    return get_adapter_store_factory(adapter, 'tokenstore_factory', container)


def servicestore_factory(container):
    # type: (AnySettingsContainer) -> ServiceStore
    """Shortcut method to retrieve the ServiceStore from the selected AdapterInterface from settings."""
    adapter = get_adapter_factory(container)
    return get_adapter_store_factory(adapter, 'servicestore_factory', container)


def owssecurity_factory(container):
    # type: (AnySettingsContainer) -> OWSSecurityInterface
    """Shortcut method to retrieve the OWSSecurityInterface from the selected AdapterInterface from settings."""
    adapter = get_adapter_factory(container)
    return get_adapter_store_factory(adapter, 'owssecurity_factory', container)
