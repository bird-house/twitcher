"""
OWSExceptions are based on pyramid.httpexceptions.

See also: https://github.com/geopython/pywps/blob/master/pywps/exceptions.py
"""


from string import Template

from zope.interface import implementer

from webob import html_escape as _html_escape

from pyramid.interfaces import IExceptionResponse
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPException,
    HTTPUnauthorized,
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotImplemented,
    status_map,
)

import inspect


@implementer(IExceptionResponse)
class OWSException(Response, Exception):
    status_base = HTTPNotImplemented
    code = 'NoApplicableCode'
    value = None
    locator = 'NoApplicableCode'
    explanation = 'Unknown Error'

    page_template = Template('''\
<?xml version="1.0" encoding="utf-8"?>
<ExceptionReport version="1.0.0"
    xmlns="http://www.opengis.net/ows/1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.opengis.net/ows/1.1 http://schemas.opengis.net/ows/1.1.0/owsExceptionReport.xsd">
    <Exception exceptionCode="${code}" locator="${locator}">
        <ExceptionText>${message}</ExceptionText>
    </Exception>
</ExceptionReport>''')

    def __init__(self, detail=None, value=None, status_base=None, **kw):
        if status_base is not None:
            self.status_base = status_base
        Response.__init__(self, status=self._get_status_string(), **kw)
        Exception.__init__(self, detail)
        self.message = detail or self.explanation
        if value:
            self.locator = value

    def __str__(self, skip_body=False):
        return self.message

    def _get_status_string(self):
        if inspect.isclass(self.status_base) and issubclass(self.status_base, HTTPException):
            status = self.status_base().status
        elif isinstance(self.status_base, HTTPException):
            status = self.status_base.status
        elif isinstance(self.status_base, int):
            status = status_map[self.status_base]().status
        else:
            raise ValueError("Invalid status base configuration.")
        return status

    def prepare(self, environ):
        if not self.body:
            self.content_type = 'text/xml'
            args = {
                'code': _html_escape(self.code),
                'locator': _html_escape(self.locator),
                'message': _html_escape(self.message or ''),
            }
            page = self.page_template.substitute(args)
            page = page.encode(self.charset)
            self.app_iter = [page]
            self.body = page

    @property
    def wsgi_response(self):
        # bw compat only
        return self

    exception = wsgi_response  # bw compat only

    def __call__(self, environ, start_response):
        # differences from webob.exc.WSGIHTTPException
        #
        # - does not try to deal with HEAD requests
        #
        # - does not manufacture a new response object when generating
        #   the default response
        #
        self.prepare(environ)
        return Response.__call__(self, environ, start_response)


class OWSAccessForbidden(OWSException):
    status_base = HTTPUnauthorized
    locator = "AccessForbidden"
    explanation = "Access to this service is forbidden"


class OWSAccessFailed(OWSException):
    status_base = HTTPBadRequest
    locator = "NotAcceptable"
    explanation = "Access to this service failed"


class OWSNoApplicableCode(OWSException):
    status_base = HTTPInternalServerError


class OWSMissingParameterValue(OWSException):
    """MissingParameterValue WPS Exception"""
    status_base = HTTPBadRequest
    code = "MissingParameterValue"
    locator = ""
    explanation = "Parameter value is missing"


class OWSInvalidParameterValue(OWSException):
    """InvalidParameterValue WPS Exception"""
    status_base = HTTPBadRequest
    code = "InvalidParameterValue"
    locator = ""
    explanation = "Parameter value is invalid"
