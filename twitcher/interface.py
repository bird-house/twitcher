"""
Twitcher interfaces to allow alternative implementions in adapters.
"""
from typing import Dict, List


class OWSSecurityInterface(object):
    def verify_request(self, request) -> bool:
        """Verify that the service request is allowed."""
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
