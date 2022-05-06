import json
import mock

from twitcher.adapter.default import DefaultAdapter
from twitcher.owssecurity import OWSSecurityInterface
from twitcher.owsregistry import OWSRegistry
from twitcher.store import ServiceStore

from ..common import dummy_request
from .base import FunctionalTest


class AdapterWithHooks(DefaultAdapter):
    def owssecurity_factory(self):
        class DummyOWSSecurity(OWSSecurityInterface):
            def verify_request(self, request): return True   # noqa: E704
        return DummyOWSSecurity()

    def request_hook(self, request, service):
        request.headers["X-Hook-Test-Service"] = service["name"]
        return request

    def response_hook(self, response, service):
        # must edit body using text content,
        # json property re-generates from it, cannot set value direct on dict returned by it
        data = json.loads(response.text)
        data["Hook-Test-Service"] = service["name"]
        response.body = json.dumps(data).encode("UTF-8")
        return response


class TestAdapterWithHooks(FunctionalTest):
    @property
    def settings(self):
        adapter_name = '{}.{}'.format(AdapterWithHooks.__module__, AdapterWithHooks.__name__)
        settings = super(TestAdapterWithHooks, self).settings.copy()
        settings.update({
            'twitcher.adapter': adapter_name
        })
        return settings

    def setUp(self):
        super(TestAdapterWithHooks, self).setUp()
        self.init_database()
        service_store = ServiceStore(dummy_request(dbsession=self.session))
        self.reg = OWSRegistry(servicestore=service_store)

        self.test_service_name = "test_adapter_svc"
        self.test_service = {
            'url': 'http://localhost/wps',
            'name': self.test_service_name,
            'type': 'wps',
            'auth': 'token',
            'public': False,
            'verify': True,
            'purl': 'http://myservice/wps'}
        resp = self.reg.register_service(**self.test_service)
        assert resp == self.test_service

        self.config.include('twitcher.owsproxy')
        self.app = self.get_test_app()

    def test_request_response_hooks(self):
        test_request_handle = []

        def mocked_request(method, url, data, headers, **_):
            _req = dummy_request(self.session)
            _req.method = method
            _req.url = url
            _req.headers = headers
            _req.body = data
            test_request_handle.append(_req)
            _resp = _req.response
            _resp.content_type = "application/json"
            _resp.status_code = 200
            _resp.body = json.dumps({"response": "ok"}).encode("UTF-8")
            _resp.content = _resp.body
            _resp.ok = True
            return _resp

        with mock.patch("requests.request", side_effect=mocked_request):
            resp = self.app.get(f'/ows/proxy/{self.test_service_name}?service=wps&request=getcapabilities')
            assert resp.status_code == 200
            assert resp.content_type == "application/json"

        # check added header by request hook
        assert test_request_handle
        assert test_request_handle[0].headers.get("X-Hook-Test-Service") == self.test_service_name

        # check added body content by response hook
        assert resp.json == {"response": "ok", "Hook-Test-Service": self.test_service_name}
