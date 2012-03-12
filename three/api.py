"""
Simple, top-level functions for working with the Open311 API.
"""

import os
from .cities import find_info
from .three import Three
from simplejson import dumps


def api_key(key=None):
    """
    Save your API key to the global environment.

    >>> three.api_key('my_api_key')
    """
    if key:
        os.environ['OPEN311_API_KEY'] = key
    return os.environ['OPEN311_API_KEY']


def city(name):
    """
    Store the city that will be queried against.

    >>> three.city('sf')
    """
    info = find_info(name)
    endpoint = info.pop('endpoint')
    os.environ['OPEN311_ENDPOINT'] = endpoint
    os.environ['OPEN311_CITY_INFO'] = dumps(info)
    return Three(endpoint, **info)


def discovery(path=None, **kwargs):
    """
    Check a city's Open311 discovery endpoint.

    >>> three.city('sf')
    >>> three.discovery()
    """
    return Three().discovery(path, **kwargs)


def request(code, **kwargs):
    """
    Find a specific request in a city.

    >>> three.city('sf')
    >>> three.request('12345')
    """
    return Three().request(code, **kwargs)


def requests(code=None, **kwargs):
    """
    Find service requests for a city.

    >>> three.city('sf')
    >>> three.requests()
    """
    return Three().requests(code, **kwargs)


def services(code=None, **kwargs):
    """
    Find services for a given city.

    >>> three.city('sf')
    >>> three.services()
    """
    return Three().services(code, **kwargs)


def token(code, **kwargs):
    """
    Find service request information for a specific token.

    >>> three.city('sf')
    >>> three.token('123abc')
    """
    return Three().token(code, **kwargs)