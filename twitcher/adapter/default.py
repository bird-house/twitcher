"""
Factories to create storage backends.
"""

from twitcher.adapter.base import AdapterInterface
from twitcher.store import AccessTokenStore, ServiceStore
from twitcher.owssecurity import OWSSecurity
from twitcher.utils import get_settings

from pyramid.config import Configurator


class DefaultAdapter(AdapterInterface):
    def describe_adapter(self):
        __doc__ = super(DefaultAdapter, self).__doc__
        from twitcher.__version__ import __version__
        return {"name": "default", "version": str(__version__)}

    def configurator_factory(self, request):
        __doc__ = super(DefaultAdapter, self).__doc__
        settings = get_settings(request)
        return Configurator(settings=settings)

    def tokenstore_factory(self, request):
        __doc__ = super(DefaultAdapter, self).__doc__
        return AccessTokenStore(request)

    def servicestore_factory(self, request):
        __doc__ = super(DefaultAdapter, self).__doc__
        return ServiceStore(request)

    def owssecurity_factory(self, request):
        __doc__ = super(DefaultAdapter, self).__doc__
        token_store = self.tokenstore_factory(request)
        service_store = self.servicestore_factory(request)
        return OWSSecurity(token_store, service_store)

    def owsproxy_config(self, request):
        __doc__ = super(DefaultAdapter, self).__doc__
        from twitcher.owsproxy import owsproxy_defaultconfig
        config = self.configurator_factory(request)
        owsproxy_defaultconfig(config)
