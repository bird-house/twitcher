"""
Twitcher interfaces to allow alternative implementations in adapters.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AnyStr, Dict, List

    from pyramid.request import Request

    from twitcher.models import Service


class OWSSecurityInterface(object):
    def verify_request(self, request) -> bool:
        """Verify that the service request is allowed."""
        raise NotImplementedError


class ServiceStoreInterface(object):
    def __init__(self, request):
        # type: (Request) -> None
        self.request = request

    def save_service(self, name, url, *args, **kwargs):
        # type: (AnyStr, AnyStr, Any, Any) -> None
        raise NotImplementedError

    def delete_service(self, name):
        # type: (AnyStr) -> None
        raise NotImplementedError

    def list_services(self):
        # type: () -> List[Service]
        raise NotImplementedError

    def fetch_by_name(self, name):
        # type: (AnyStr) -> Service
        raise NotImplementedError

    def fetch_by_url(self, url):
        # type: (AnyStr) -> Service
        raise NotImplementedError

    def clear_services(self):
        # type: () -> None
        raise NotImplementedError


class OWSRegistryInterface(object):
    def register_service(self, name: str, url: str, *args, **kwargs) -> Dict:
        """Register an OWS service with given ``name`` and ``url``."""
        raise NotImplementedError

    def unregister_service(self, name: str) -> bool:
        """Unregister an OWS service with given ``name``."""
        raise NotImplementedError

    def get_service_by_name(self, name: str) -> Dict:
        """Lookup OWS service with given ``name``."""
        raise NotImplementedError

    def get_service_by_url(self, url: str) -> Dict:
        """Lookup OWS service with given ``url``."""
        raise NotImplementedError

    def list_services(self) -> List:
        """List all registered OWS services."""
        raise NotImplementedError

    def clear_services(self) -> bool:
        """Remove all registered OWS services."""
        raise NotImplementedError
