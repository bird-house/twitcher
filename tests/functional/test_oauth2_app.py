from .base import FunctionalTest


def compute_view(request):
    if request.verify_request(scopes=["compute"]) is True:
        result = {'status': 'success'}
    else:
        result = {'status': 'not allowed'}
    return result


class OAuth2AppTests(FunctionalTest):

    def setUp(self):
        super(OAuth2AppTests, self).setUp()
        self.init_database()

        self.config.include('twitcher.oauth2')
        self.config.add_route('compute', '/api/compute')
        self.config.add_view(compute_view, route_name='compute', renderer='json')
        self.app = self.get_test_app()

    def test_compute_with_param(self):
        access_token = self.create_token()
        resp = self.app.get('/api/compute?access_token={}'.format(access_token))
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        resp.mustcontain('success')

    def test_compute_with_header(self):
        access_token = self.create_token()
        resp = self.app.get('/api/compute',
                            headers={'Authorization': 'Bearer {}'.format(access_token)})
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        resp.mustcontain('success')
