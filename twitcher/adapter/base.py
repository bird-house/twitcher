from twitcher.utils import get_settings

from typing import TYPE_CHECKING
import six
if TYPE_CHECKING:
    from twitcher.typedefs import AnySettingsContainer, JSON
    from twitcher.store import AccessTokenStoreInterface, ServiceStoreInterface
    from twitcher.owssecurity import OWSSecurityInterface
    from pyramid.config import Configurator
    from pyramid.request import Request


class AdapterBase(type):
    @property
    def name(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)


class AdapterInterface(six.with_metaclass(AdapterBase)):
    """
    Common interface allowing functionality overriding using an adapter implementation.
    """
    def __init__(self, container):
        # type: (AnySettingsContainer) -> None
        self.settings = get_settings(container)

    @classmethod
    def name(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)

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

    def tokenstore_factory(self, request):
        # type: (Request) -> AccessTokenStoreInterface
        """
        Returns the 'tokenstore' implementation of the adapter.
        """
        raise NotImplementedError

    def servicestore_factory(self, request):
        # type: (Request) -> ServiceStoreInterface
        """
        Returns the 'servicestore' implementation of the adapter.
        """
        raise NotImplementedError

    def owssecurity_factory(self, request):
        # type: (Request) -> OWSSecurityInterface
        """
        Returns the 'owssecurity' implementation of the adapter.
        """
        raise NotImplementedError

    def owsproxy_config(self, container):
        # type: (AnySettingsContainer) -> None
        """
        Returns the 'owsproxy' implementation of the adapter.
        """
        raise NotImplementedError
