from twitcher import datatype
from twitcher.utils import sanitize

import logging
LOGGER = logging.getLogger("TWITCHER")


class ITokenManager(object):
    def generate_token(self, valid_in_hours):
        """
        Generates an access token which is valid for ``valid_in_hours``.

        Arguments:

        * :param valid_in_hours: an int with number of hours the token is valid.
        """
        raise NotImplementedError

    def revoke_token(self, token):
        """
        Remove token from tokenstore.
        """
        raise NotImplementedError

    def revoke_all_tokens(self):
        """
        Removes all tokens from tokenstore.
        """
        raise NotImplementedError


class IRegistry(object):
    def register_service(self, name, url, data):
        """
        Adds an OWS service with the given ``name`` and ``url`` to the service store.

        :param data: a dict with additional information like ``purl``.
        """
        raise NotImplementedError

    def unregister_service(self, name):
        """
        Removes OWS service with the given ``name`` from the service store.
        """
        raise NotImplementedError

    def get_service_by_name(self, name):
        """
        Gets service with given ``name`` from service store.
        """
        raise NotImplementedError

    def get_service_by_url(self, url):
        """
        Gets service with given ``url`` from service store.
        """
        raise NotImplementedError

    def list_services(self):
        """
        Lists all registred OWS services.
        """
        raise NotImplementedError

    def clear_services(self):
        """
        Removes all services from the service store.
        """
        raise NotImplementedError


class TokenManager(ITokenManager):
    """
    Implementation of :class:`twitcher.api.ITokenManager`.
    """

    def __init__(self, tokengenerator, tokenstore):
        self.tokengenerator = tokengenerator
        self.store = tokenstore

    def generate_token(self, valid_in_hours=1):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.generate_token`.
        """
        access_token = self.tokengenerator.create_access_token(
            valid_in_hours=valid_in_hours
        )
        try:
            self.store.save_token(access_token)
        except Exception:
            LOGGER.exception('Failed to save token.')
            return {}
        else:
            return access_token.params

    def revoke_token(self, token):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.revoke_token`.
        """
        try:
            self.store.delete_token(token)
        except Exception:
            LOGGER.exception('Failed to remove token.')
            return False
        else:
            return True

    def revoke_all_tokens(self):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.revoke_all_tokens`.
        """
        try:
            self.store.clear_tokens()
        except Exception:
            LOGGER.exception('Failed to remove tokens.')
            return False
        else:
            return True


class Registry(IRegistry):
    """
    Implementation of :class:`twitcher.api.IRegistry`.
    """
    def __init__(self, servicestore):
        self.store = servicestore

    def register_service(self, name, url, data=None):
        """
        Implementation of :meth:`twitcher.api.IRegistry.register_service`.
        """
        data = data or {}

        args = dict(data)
        args['name'] = sanitize(name)
        args['url'] = url
        service = datatype.Service(**args)
        try:
            self.store.save_service(service)
        except Exception:
            LOGGER.exception('register service failed')
            return {}
        return service.params

    def unregister_service(self, name):
        """
        Implementation of :meth:`twitcher.api.IRegistry.unregister_service`.
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
        Implementation of :meth:`twitcher.api.IRegistry.get_service_by_name`.
        """
        try:
            service = self.store.fetch_by_name(name=name)
        except Exception:
            LOGGER.error('Could not get service with name {}'.format(name))
            return {}
        else:
            return service.params

    def get_service_by_url(self, url):
        """
        Implementation of :meth:`twitcher.api.IRegistry.get_service_by_url`.
        """
        try:
            service = self.store.fetch_by_url(url=url)
        except Exception:
            LOGGER.error('Could not get service with url {}'.format(url))
            return {}
        else:
            return service.params

    def list_services(self):
        """
        Implementation of :meth:`twitcher.api.IRegistry.list_services`.
        """
        try:
            services = [service.params for service in self.store.list_services()]
        except Exception:
            LOGGER.error('List services failed.')
            return []
        else:
            return services

    def clear_services(self):
        """
        Implementation of :meth:`twitcher.api.IRegistry.clear_services`.
        """
        try:
            self.store.clear_services()
        except Exception:
            LOGGER.error('Clear services failed.')
            return False
        else:
            return True
