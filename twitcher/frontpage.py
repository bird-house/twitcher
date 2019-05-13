from pyramid.view import view_config


@view_config(route_name='frontpage', renderer='json')
def frontpage(request):
    return {'message': 'hello'}


def includeme(config):
    config.add_route('frontpage', '/')
