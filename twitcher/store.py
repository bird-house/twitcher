"""
Read or write data from database.

Stores should not be accessed directly, but instead should use the adapter interface.

See also:
    - :class:`twitcher.adapter.base.AdapterInterface`
    - :func:`twitcher.adapter.get_adapter_factory`
"""
from twitcher.exceptions import (
    ServiceNotFound,
    DatabaseError
)
from twitcher.interface import ServiceStoreInterface
from twitcher.utils import baseurl
from twitcher import models

from sqlalchemy.exc import DBAPIError


class ServiceStore(ServiceStoreInterface):
    """
    Stores a services. It inserts or updates the service with a given name.
    """
    def save_service(self, name, url, *args, **kwargs):
        """
        Stores an OWS service in database (insert or update).

        :param name: A service name string.
        :param url: A URL string.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.name == name).first()
            if one:
                # update
                one.url = baseurl(url)
                one.type = kwargs.get('type', 'WPS')
                one.purl = kwargs.get('purl', '')
                one._verify = int(kwargs.get('verify', 1))
                one.auth = kwargs.get('auth', 'token')
                self.request.dbsession.merge(one)
            else:
                # insert
                one = models.Service(
                    name=name,
                    url=baseurl(url),
                    type=kwargs.get('type', 'WPS'),
                    purl=kwargs.get('purl', ''),
                    _verify=int(kwargs.get('verify', 1)),
                    auth=kwargs.get('auth', 'token'))
                self.request.dbsession.add(one)
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        return one

    def delete_service(self, name):
        """
        Removes service identified by name.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.name == name).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        self.request.dbsession.delete(one)

    def list_services(self):
        """
        Lists all services.

        :return: A list with instances of :class:`twitcher.models.Service`.
        """
        try:
            services = self.request.dbsession.query(models.Service).all()
        except DBAPIError:
            raise DatabaseError
        return services

    def fetch_by_name(self, name):
        """
        Get service for given service ``name``.

        :param name: A service name string.
        :return: An instance of :class:`twitcher.models.Service`.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.name == name).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        return one

    def fetch_by_url(self, url):
        """
        Get a service for given ``url``.

        :param url: A URL string.
        :return: An instance of :class:`twitcher.models.Service`.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.url == url).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        return one

    def clear_services(self):
        """
        Removes all services.
        """
        try:
            self.request.dbsession.query(models.Service).delete()
        except DBAPIError:
            raise DatabaseError
