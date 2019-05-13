from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitcher.typedefs import AnySettingsContainer, JSON
    from twitcher.store import AccessTokenStoreInterface, ServiceStoreInterface
    from twitcher.owssecurity import OWSSecurityInterface
    from pyramid.config import Configurator


class AdapterInterface(object):
    """
    Common interface allowing some functionality overriding using an adapter
    """

    def describe_adapter(self):
        # type: () -> JSON
        """
        Returns a JSON serializable dictionary describing the adapter implementation.
        """
        raise NotImplementedError

    def tokenstore_factory(self, container):
        # type: (AnySettingsContainer) -> AccessTokenStoreInterface
        """
        Returns the 'tokenstore' implementation of the adapter.
        """
        raise NotImplementedError

    def servicestore_factory(self, container):
        # type: (AnySettingsContainer) -> ServiceStoreInterface
        """
        Returns the 'servicestore' implementation of the adapter.
        """
        raise NotImplementedError

    def owssecurity_factory(self, container):
        # type: (AnySettingsContainer) -> OWSSecurityInterface
        """
        Returns the 'owssecurity' implementation of the adapter.
        """
        raise NotImplementedError

    def configurator_factory(self, container):
        # type: (AnySettingsContainer) -> Configurator
        """
        Returns the 'configurator' implementation of the adapter.
        """
        raise NotImplementedError

    def owsproxy_config(self, container):
        # type: (AnySettingsContainer) -> None
        """
        Returns the 'owsproxy' implementation of the adapter.
        """
        raise NotImplementedError
