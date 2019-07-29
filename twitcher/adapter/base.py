from twitcher.utils import get_settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitcher.typedefs import AnySettingsContainer, JSON
    from twitcher.interface import OWSSecurityInterface, OWSRegistryInterface
    from pyramid.config import Configurator
    from pyramid.request import Request


class AdapterInterface(object):
    """
    Common interface allowing functionality overriding using an adapter implementation.
    """
    def __init__(self, container):
        # type: (AnySettingsContainer) -> None
        self.settings = get_settings(container)

    @property
    def name(self):
        return '{}.{}'.format(self.__module__, type(self).__name__)

    def describe_adapter(self):
        # type: () -> JSON
        """
        Returns a JSON serializable dictionary describing the adapter implementation.
        """
        raise NotImplementedError

    def configurator_factory(self, container):
        # type: (AnySettingsContainer) -> Configurator
        """
        Returns the 'configurator' implementation of the adapter.
        """
        raise NotImplementedError

    def owssecurity_factory(self):
        # type: () -> OWSSecurityInterface
        """
        Returns the 'owssecurity' implementation of the adapter.
        """
        raise NotImplementedError

    def owsregistry_factory(self, request):
        # type: (Request) -> OWSRegistryInterface
        """
        Returns the 'owsregistry' implementation of the adapter.
        """
        raise NotImplementedError

    def owsproxy_config(self, container):
        # type: (AnySettingsContainer) -> None
        """
        Returns the 'owsproxy' implementation of the adapter.
        """
        raise NotImplementedError
