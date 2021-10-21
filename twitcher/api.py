import colander
from cornice import Service
from cornice.validators import colander_body_validator

from twitcher.__version__ import __version__


import logging
LOGGER = logging.getLogger("TWITCHER")

# Rest API Services
services = Service(name='services',
                   path='/services',
                   permission='view',
                   description="List, add or clear services")

service = Service(name='service',
                  path='/services/{name}',
                  permission='view',
                  description="Get or remove a service item")


# Register service request schema
class ServicesPostBodySchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(),
                               description='Service name')
    url = colander.SchemaNode(colander.String(),
                              description='Service URL')
    type = colander.SchemaNode(colander.String(),
                               missing=colander.drop, default='WPS',
                               description='Service Type')
    purl = colander.SchemaNode(colander.String(),
                               missing=colander.drop, default='',
                               description='Service public URL')
    verify = colander.SchemaNode(colander.Boolean(),
                                 missing=colander.drop, default=True,
                                 description='Verify HTTPS connection')
    auth = colander.SchemaNode(colander.String(),
                               missing=colander.drop, default='token',
                               description='Authentication method')


# Create our cornice service views
class TwitcherAPI(object):
    """Twitcher API defined with OpenAPI."""

    @staticmethod
    @services.get(tags=['services', 'list'])
    def list_services(request):
        """Returns a list of registered services."""
        return request.owsregistry.list_services()

    @staticmethod
    @services.delete(tags=['services', 'clear'])
    def clear_services(request):
        """Clear all services."""
        return request.owsregistry.clear_services()

    @staticmethod
    @services.post(tags=['services', 'register'],
                   validators=(colander_body_validator, ),
                   schema=ServicesPostBodySchema())
    def register_service(request):
        """Register a service."""
        LOGGER.debug("request validated={}".format(request.validated))
        return request.owsregistry.register_service(**request.validated)

    @staticmethod
    @service.get(tags=['service', 'get'])
    def get_service(request):
        """Get registered service."""
        return request.owsregistry.get_service_by_name(name=request.matchdict['name'])

    @staticmethod
    @service.delete(tags=['service', 'unregister'])
    def unregister_service(request):
        """Remove registered service."""
        return request.owsregistry.unregister_service(name=request.matchdict['name'])


def includeme(config):
    config.include('twitcher.basicauth')
    config.include('cornice')
    config.include('cornice_swagger')
    config.include('twitcher.oauth2')
    config.include('twitcher.owsregistry')
    # Create views to serve our OpenAPI spec
    config.cornice_enable_openapi_view(
        api_path='/__api__',
        # permission='view',
        title='Twitcher API',
        description="OpenAPI documentation",
        version=__version__
    )
    # Create views to serve OpenAPI spec UI explorer
    config.cornice_enable_openapi_explorer(
        api_explorer_path='/api-explorer',
        # permission='view'
    )
