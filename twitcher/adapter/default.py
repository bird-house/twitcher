"""
Factories to create storage backends.
"""

from twitcher.adapter.base import AdapterInterface
from twitcher.models.service import ServiceConfig
from twitcher.owsproxy import send_request
from twitcher.owssecurity import OWSSecurity
from twitcher.owsregistry import OWSRegistry
from twitcher.store import ServiceStore
from twitcher.utils import get_settings
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response

TWITCHER_ADAPTER_DEFAULT = 'default'


class DefaultAdapter(AdapterInterface):
    @property
    def name(self):
        return TWITCHER_ADAPTER_DEFAULT

    def describe_adapter(self):
        from twitcher.__version__ import __version__
        return {"name": self.name, "version": str(__version__)}

    def configurator_factory(self, container):
        settings = get_settings(container)
        return Configurator(settings=settings)

    def owssecurity_factory(self):
        return OWSSecurity()

    def owsregistry_factory(self, request):
        return OWSRegistry(ServiceStore(request))

    def owsproxy_config(self, container):
        from twitcher.owsproxy import owsproxy_defaultconfig
        # update provided config or generate it otherwise
        if not isinstance(container, Configurator):
            container = self.configurator_factory(container)
        owsproxy_defaultconfig(container)

    def request_hook(self, request, service):
        return request

    def response_hook(self, response, service):
        return response

    def send_request(self, request: Request, service: ServiceConfig) -> Response:
        return send_request(request, service)
