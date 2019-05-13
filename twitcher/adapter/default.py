"""
Factories to create storage backends.
"""

from twitcher.adapter.base import AdapterInterface
from twitcher.store import AccessTokenStore, ServiceStore
from twitcher.owssecurity import OWSSecurity
from pyramid.config import Configurator


class DefaultAdapter(AdapterInterface):
    def describe_adapter(self):
        __doc__ = super(DefaultAdapter, self).__doc__
        from twitcher.__version__ import __version__
        return {"name": "default", "version": str(__version__)}

    def tokenstore_factory(self, container):
        __doc__ = super(DefaultAdapter, self).__doc__
        return tokenstore_factory(container)

    def servicestore_factory(self, container):
        __doc__ = super(DefaultAdapter, self).__doc__
        return servicestore_factory(container)

    def owssecurity_factory(self, container):
        __doc__ = super(DefaultAdapter, self).__doc__
        token_store = self.tokenstore_factory(container)
        service_store = self.servicestore_factory(container)
        return OWSSecurity(token_store, service_store)

    def configurator_factory(self, container):
        __doc__ = super(DefaultAdapter, self).__doc__
        from twitcher.utils import get_settings
        if isinstance(container, Configurator):
            return container
        settings = get_settings(container)
        return Configurator(settings=settings)

    def owsproxy_config(self, container):
        __doc__ = super(DefaultAdapter, self).__doc__
        from twitcher.owsproxy import owsproxy_defaultconfig
        config = self.configurator_factory(container)
        owsproxy_defaultconfig(config)
