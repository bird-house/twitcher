from twitcher.interface import OWSSecurityInterface
from twitcher.owsrequest import OWSRequest


class OWSSecurity(OWSSecurityInterface):
    def verify_request(self, request):
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
            return request.headers.get('X-Ssl-Client-Verify', '') == 'SUCCESS'
        else:
            return request.verify_request(scopes=["compute"])


def includeme(config):
    from twitcher.adapter import get_adapter_factory

    def verify_ows_request(request):
        adapter = get_adapter_factory(request)
        return adapter.owssecurity_factory().verify_request(request)
    config.add_request_method(verify_ows_request, reify=True)
