from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.registry import Registry
from datetime import datetime
from urllib import parse as urlparse
from lxml import etree
import json
import time
import pytz
import re
from typing import AnyStr, Optional

from twitcher.exceptions import ServiceNotFound
from twitcher.typedefs import AnySettingsContainer, SettingsType

import logging
LOGGER = logging.getLogger("TWITCHER")


def get_settings(container: AnySettingsContainer) -> Optional[SettingsType]:
    """
    Retrieves the application ``settings`` from various containers referencing to it.

    :raises TypeError: if the container type cannot be identified to retrieve settings.
    """
    if isinstance(container, (Configurator, Request)):
        container = container.registry
    if isinstance(container, Registry):
        container = container.settings
    if isinstance(container, dict):
        return container
    raise TypeError("Could not retrieve settings from container object of type [{}]".format(type(container)))


def get_twitcher_url(container: AnySettingsContainer) -> AnyStr:
    settings = get_settings(container)
    return settings.get('twitcher.url').rstrip('/').strip()


def sanitize(name, minlen=2, maxlen=25):
    """Lower-case name and replace all non-ascii chars by `_`."""
    if name is None or len(name.strip()) < minlen:
        raise ValueError("name must have at least {} chars.".format(minlen))
    return re.sub(r'\W|^(?=\d)', '_', name.strip().lower()[:maxlen])


def is_valid_url(url):
    try:
        parsed_url = urlparse.urlparse(url)
        return True if all([parsed_url.scheme, ]) else False
    except Exception:
        return False


def is_json_serializable(item):
    try:
        json.dumps(item)
        return True
    except (TypeError, OverflowError):
        return False


def parse_service_name(url: str, protected_path: str) -> Optional[str]:
    parsed_url = urlparse.urlparse(url)
    service_name = None
    if parsed_url.path.startswith(protected_path):
        parts_without_protected_path = parsed_url.path[len(protected_path)::].strip('/').split('/')
        # use ranges to avoid index error in case the path parts list is empty
        # the expected part must be exactly the first one after the protected path, then followed by the service name
        if any(part in parts_without_protected_path[:1] for part in ['proxy', 'verify']):
            parts_without_protected_path = parts_without_protected_path[1:]
        if len(parts_without_protected_path) > 0:
            service_name = parts_without_protected_path[0]
    if not service_name:
        raise ServiceNotFound
    return service_name


def now():
    return localize_datetime(datetime.utcnow())


def now_secs():
    """
    Return the current time in seconds since the Epoch.
    """
    return int(time.time())


def expires_at(hours=1):
    return now_secs() + hours * 3600


def localize_datetime(dt, tz_name='UTC'):
    """Provide a timezone-aware object for a given datetime and timezone name
    """
    tz_aware_dt = dt
    if dt.tzinfo is None:
        utc = pytz.timezone('UTC')
        aware = utc.localize(dt)
        timezone = pytz.timezone(tz_name)
        tz_aware_dt = aware.astimezone(timezone)
    else:
        LOGGER.warning('tzinfo already set')
    return tz_aware_dt


def baseurl(url):
    """
    return baseurl of given url
    """
    parsed_url = urlparse.urlparse(url)
    if not parsed_url.netloc or parsed_url.scheme not in ("http", "https"):
        raise ValueError('bad url')
    service_url = "%s://%s%s" % (parsed_url.scheme, parsed_url.netloc, parsed_url.path.strip())
    return service_url


def path_elements(path):
    elements = [el.strip() for el in path.split('/')]
    elements = [el for el in elements if len(el) > 0]
    return elements


def lxml_strip_ns(tree):
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith('{')
        except AttributeError:
            continue  # node.tag is not a string (node is a comment or similar)
        if has_namespace:
            node.tag = node.tag.split('}', 1)[1]


def replace_caps_url(xml, url, prev_url=None):
    ns = {
        'ows': 'http://www.opengis.net/ows/1.1',
        'xlink': 'http://www.w3.org/1999/xlink'}
    doc = etree.fromstring(xml)
    # wms 1.1.1 onlineResource
    if 'WMT_MS_Capabilities' in doc.tag:
        LOGGER.debug("replace proxy urls in wms 1.1.1")
        for element in doc.findall('.//OnlineResource[@xlink:href]', namespaces=ns):
            parsed_url = urlparse.urlparse(element.get('{http://www.w3.org/1999/xlink}href'))
            new_url = url
            if parsed_url.query:
                new_url += '?' + parsed_url.query
            element.set('{http://www.w3.org/1999/xlink}href', new_url)
        xml = etree.tostring(doc)
    # wms 1.3.0 onlineResource
    elif 'WMS_Capabilities' in doc.tag:
        LOGGER.debug("replace proxy urls in wms 1.3.0")
        for element in doc.findall('.//{http://www.opengis.net/wms}OnlineResource[@xlink:href]', namespaces=ns):
            parsed_url = urlparse.urlparse(element.get('{http://www.w3.org/1999/xlink}href'))
            new_url = url
            if parsed_url.query:
                new_url += '?' + parsed_url.query
            element.set('{http://www.w3.org/1999/xlink}href', new_url)
        xml = etree.tostring(doc)
    # wps operations
    elif 'Capabilities' in doc.tag:
        for element in doc.findall('ows:OperationsMetadata//*[@xlink:href]', namespaces=ns):
            element.set('{http://www.w3.org/1999/xlink}href', url)
        xml = etree.tostring(doc)
    elif prev_url:
        xml = xml.decode('utf-8', 'ignore')
        xml = xml.replace(prev_url, url)
    return xml
