from pyramid.settings import asbool

from twitcher.interface import OWSSecurityInterface
from twitcher.owsrequest import OWSRequest
from twitcher.utils import get_settings


class OWSSecurity(OWSSecurityInterface):
    def verify_request(self, request):
        """Verify that the service request is allowed.

        This method verifies that the provided credentials are valid.
        Depending on the authentication configuration this could be
        a client X509 certificate or an OAuth2 token.
        """
        ows_request = OWSRequest(request)
        if ows_request.service_allowed() is False:
            return False
        try:
            service_name = request.matchdict.get('service_name')
            service = request.owsregistry.get_service_by_name(service_name)
        except Exception:
            return False
        if service.get('public', False) is True:
            return True
        if ows_request.public_access() is True:
            return True
        if service.get('auth', '') == 'cert':
            # Check the verification result of the client certificate.
            # Verification is done by nginx.
            return request.headers.get('X-Ssl-Client-Verify', '') == 'SUCCESS'
        else:
            # verify the oauth token for compute scope.
            return request.verify_request(scopes=["compute"])


def includeme(config):
    from twitcher.adapter import get_adapter_factory
    settings = get_settings(config)
    security_enabled = asbool(settings.get('twitcher.ows_security', True))

    def is_verified(request):
        if not security_enabled:
            return True
        adapter = get_adapter_factory(request)
        return adapter.owssecurity_factory().verify_request(request)
    config.add_request_method(is_verified, reify=True)
