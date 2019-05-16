"""
Read or write data from database.

Stores should not be accessed directly, but instead should use the adapter interface.

See also:
    - :class:`twitcher.adapter.base.AdapterInterface`
    - :func:`twitcher.adapter.get_adapter_factory`
"""

from twitcher.exceptions import (
    AccessTokenNotFound,
    ServiceNotFound,
    DatabaseError
)
from twitcher.utils import baseurl
from twitcher import datatype
from twitcher import models

from typing import TYPE_CHECKING
from sqlalchemy.exc import DBAPIError

if TYPE_CHECKING:
    from twitcher.models.token import AccessToken
    from twitcher.models.service import Service
    from pyramid.request import Request
    from typing import AnyStr, List


class AccessTokenStoreInterface(object):
    def __init__(self, request):            # type: (Request) -> None
        self.request = request

    def save_token(self, access_token):     # type: (AccessToken) -> None
        raise NotImplementedError

    def delete_token(self, token):          # type: (AccessToken) -> None
        raise NotImplementedError

    def fetch_by_token(self, token):        # type: (AnyStr) -> None
        raise NotImplementedError

    def clear_tokens(self):                 # type: () -> None
        raise NotImplementedError


class AccessTokenStore(AccessTokenStoreInterface):
    """
    Stores tokens in sql database.

    TODO: handle exceptions.
    """
    def __init__(self, request):
        super(AccessTokenStore, self).__init__(request)

    def save_token(self, access_token):
        """
        Stores an access token.
        """
        try:
            self.request.dbsession.add(models.AccessToken(
                token=access_token.token,
                expires_at=access_token.expires_at))
        except DBAPIError:
            raise DatabaseError

    def delete_token(self, token):
        """
        Deletes an access token from the store using its token string to identify it.

        :param token: A token string.
        """
        try:
            query = self.request.dbsession.query(models.AccessToken)
            one = query.filter(models.AccessToken.token == token).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise AccessTokenNotFound
        self.request.dbsession.delete(one)

    def fetch_by_token(self, token):
        """
        Fetches an access token from the store using its token string to
        identify it.

        :param token: A token string.
        :return: An instance of :class:`twitcher.datatype.AccessToken`.
        """
        try:
            query = self.request.dbsession.query(models.AccessToken)
            one = query.filter(models.AccessToken.token == token).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise AccessTokenNotFound
        return datatype.AccessToken.from_model(one)

    def clear_tokens(self):
        """
        Removes all tokens.
        """
        try:
            self.request.dbsession.query(models.AccessToken).delete()
        except DBAPIError:
            raise DatabaseError


class ServiceStoreInterface(object):
    def __init__(self, request):        # type: (Request) -> None
        self.request = request

    def save_service(self, service):    # type: (Service) -> None
        raise NotImplementedError

    def delete_service(self, name):     # type: (AnyStr) -> None
        raise NotImplementedError

    def list_services(self):            # type: () -> List[Service]
        raise NotImplementedError

    def fetch_by_name(self, name):      # type: (AnyStr) -> Service
        raise NotImplementedError

    def fetch_by_url(self, url):        # type: (AnyStr) -> Service
        raise NotImplementedError

    def clear_services(self):           # type: () -> None
        raise NotImplementedError


class ServiceStore(ServiceStoreInterface):
    """
    Stores a services. It inserts or updates the service with a given name.
    """
    def __init__(self, request):
        super(ServiceStore, self).__init__(request)

    def save_service(self, service):
        """
        Stores an OWS service in database (insert or update).

        :param service: An instance of :class:`twitcher.datatype.Service`.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.name == service.name).first()
            if one:
                # update
                one.url = baseurl(service.url)
                one.type = service.type
                one.purl = service.purl
                one.public = int(service.public)
                one.verify = int(service.verify)
                one.auth = service.auth
                self.request.dbsession.merge(one)
            else:
                # insert
                self.request.dbsession.add(models.Service(
                    name=service.name,
                    url=baseurl(service.url),
                    type=service.type,
                    purl=service.purl,
                    public=int(service.public),
                    verify=int(service.verify),
                    auth=service.auth))
        except DBAPIError:
            raise DatabaseError

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

        :return: A list with instances of :class:`twitcher.datatype.Service`.
        """
        try:
            services = self.request.dbsession.query(models.Service).all()
        except DBAPIError:
            raise DatabaseError
        return [datatype.Service.from_model(service) for service in services]

    def fetch_by_name(self, name):
        """
        Get service for given service ``name``.

        :param name: A service name string.
        :return: An instance of :class:`twitcher.datatype.Service`.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.name == name).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        return datatype.Service.from_model(one)

    def fetch_by_url(self, url):
        """
        Get a service for given ``url``.

        :param url: A URL string.
        :return: An instance of :class:`twitcher.datatype.Service`.
        """
        try:
            query = self.request.dbsession.query(models.Service)
            one = query.filter(models.Service.url == url).first()
        except DBAPIError:
            raise DatabaseError
        if not one:
            raise ServiceNotFound
        return datatype.Service.from_model(one)

    def clear_services(self):
        """
        Removes all services.
        """
        try:
            self.request.dbsession.query(models.Service).delete()
        except DBAPIError:
            raise DatabaseError
