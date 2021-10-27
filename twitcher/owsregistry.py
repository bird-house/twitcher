from twitcher.interface import OWSRegistryInterface
from twitcher.utils import sanitize

import logging
LOGGER = logging.getLogger("TWITCHER")


class OWSRegistry(OWSRegistryInterface):
    """
    OWS Service Registry is a service to register OWS services for the OWS proxy.
    """
    def __init__(self, servicestore):
        self.store = servicestore

    def register_service(self, name, url, *args, **kwargs):
        """
        Adds an OWS service with the given ``name`` and ``url`` to the service store.
        """
        data = dict(kwargs)
        data['name'] = sanitize(name)
        data['url'] = url
        try:
            service = self.store.save_service(**data)
        except Exception:
            LOGGER.exception('register service failed')
            return {}
        return service.json()

    def unregister_service(self, name):
        """
        Removes OWS service with the given ``name`` from the service store.
        """
        try:
            self.store.delete_service(name=name)
        except Exception:
            LOGGER.exception('unregister service failed')
            return False
        else:
            return True

    def get_service_by_name(self, name):
        """
        Gets service with given ``name`` from service store.
        """
        try:
            service = self.store.fetch_by_name(name=name)
        except Exception as exc:
            msg = 'Could not get service with name {}'.format(name)
            LOGGER.debug(msg, exc_info=exc)
            LOGGER.error(msg)
            return {}
        else:
            return service.json()

    def get_service_by_url(self, url):
        """
        Gets service with given ``url`` from service store.
        """
        try:
            service = self.store.fetch_by_url(url=url)
        except Exception:
            LOGGER.error('Could not get service with url {}'.format(url))
            return {}
        else:
            return service.json()

    def list_services(self):
        """
        Lists all registered OWS services.
        """
        try:
            services = [service.json() for service in self.store.list_services()]
        except Exception:
            LOGGER.error('List services failed.')
            return []
        else:
            return services

    def clear_services(self):
        """
        Removes all services from the service store.
        """
        try:
            self.store.clear_services()
        except Exception:
            LOGGER.error('Clear services failed.')
            return False
        else:
            return True


def includeme(config):
    from twitcher.adapter import get_adapter_factory

    def owsregistry(request):
        adapter = get_adapter_factory(request)
        return adapter.owsregistry_factory(request)
    config.add_request_method(owsregistry, reify=True)
