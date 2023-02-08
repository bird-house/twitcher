import typing
from typing import AnyStr, Dict, List, Tuple, Union
from requests.structures import CaseInsensitiveDict
from pyramid.config import Configurator
from pyramid.registry import Registry
from pyramid.request import Request as PyramidRequest
from pyramid.response import Response as PyramidResponse
from webob.response import Response as WebobResponse
from webob.headers import ResponseHeaders, EnvironHeaders

if hasattr(typing, "TypedDict"):
    from typing import TypedDict  # pylint: disable=E0611,no-name-in-module
else:
    from typing_extensions import TypedDict  # noqa

Number = Union[int, float]
AnyValue = Union[AnyStr, Number, bool, None]
AnyKey = Union[AnyStr, int]
JSON = Dict[AnyKey, Union[AnyValue, Dict[AnyKey, 'JSON'], List['JSON']]]

AnyContainer = Union[Configurator, Registry, PyramidRequest]
SettingValue = Union[AnyStr, Number, bool, None]
SettingsType = Dict[AnyStr, SettingValue]
AnySettingsContainer = Union[AnyContainer, SettingsType]

CookiesType = Dict[AnyStr, AnyStr]
HeadersType = Dict[AnyStr, AnyStr]
CookiesTupleType = List[Tuple[AnyStr, AnyStr]]
HeadersTupleType = List[Tuple[AnyStr, AnyStr]]
CookiesBaseType = Union[CookiesType, CookiesTupleType]
HeadersBaseType = Union[HeadersType, HeadersTupleType]
OptionalHeaderCookiesType = Union[Tuple[None, None], Tuple[HeadersBaseType, CookiesBaseType]]
AnyHeadersContainer = Union[HeadersBaseType, ResponseHeaders, EnvironHeaders, CaseInsensitiveDict]
AnyCookiesContainer = Union[CookiesBaseType, PyramidRequest, AnyHeadersContainer]
AnyResponseType = Union[WebobResponse, PyramidResponse]
