from twitcher.utils import get_settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyramid.config import Configurator
    from pyramid.request import Request
    from pyramid.response import Response

    from twitcher.interface import OWSSecurityInterface, OWSRegistryInterface
    from twitcher.models.service import ServiceConfig
    from twitcher.typedefs import AnySettingsContainer, JSON


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

    def request_hook(self, request, service):
        # type: (Request, ServiceConfig) -> Request
        """
        Apply modifications onto the request before sending it.

        .. versionadded:: 0.7.0

        Request members employed after this hook is called include:
        - :meth:`Request.headers`
        - :meth:`Request.method`
        - :meth:`Request.body`

        This method can modified those members to adapt the request for specific service logic.
        """
        raise NotImplementedError

    def response_hook(self, response, service):
        # type: (Response, ServiceConfig) -> Response
        """
        Apply modifications onto the response from sent request.

        .. versionadded:: 0.7.0

        The received response from the proxied service is normally returned directly.
        This method can modify the response to adapt it for specific service logic.
        """
        raise NotImplementedError

    def send_request(self, request, service):
        # type: (Request, ServiceConfig) -> Response
        """
        Performs the provided request in order to obtain a proxied response.

        .. versionadded:: 0.8.0

        The operation should consider the service definition to resolve where the
        request redirection should be proxied to, and handle any relevant response
        errors, such as an unauthorized access or an unreachable service.
        """
        raise NotImplementedError
