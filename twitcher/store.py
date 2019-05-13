"""
Read or write data from database.
"""

from twitcher.exceptions import (
    AccessTokenNotFound,
    ServiceNotFound,
    DatabaseError
)
from twitcher import namesgenerator
from twitcher.utils import baseurl
from twitcher import datatype
from twitcher import models

from sqlalchemy.exc import DBAPIError


class AccessTokenStore(object):
    """
    Stores tokens in sql database.

    TODO: handle exceptions.
    """
    def __init__(self, request):
        self.request = request

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


class ServiceStore(object):
    """
    Stores a services. It inserts or updates the service with a given name.
    """
    def __init__(self, request):
        self.request = request

    def save_service(self, service):
        """
        Stores an OWS service in database.

        :param service: An instance of :class:`twitcher.datatype.Service`.
        """
        try:
            self.request.dbsession.merge(models.Service(
                name=service.name,
                url=baseurl(service.url),
                type=service.type,
                purl=service.purl,
                public=service.public,
                verify=service.verify,
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
