"""
Simple, top-level functions for working with the Open311 API.
"""

import os
from .cities import find_info
from .core import Three
from simplejson import dumps


def key(key=None):
    """
    Save your API key to the global environment.

    >>> three.api_key('my_api_key')
    """
    if key:
        os.environ['OPEN311_API_KEY'] = key
    return os.environ['OPEN311_API_KEY']


def city(name=None):
    """
    Store the city that will be queried against.

    >>> three.city('sf')
    """
    info = find_info(name)
    os.environ['OPEN311_CITY_INFO'] = dumps(info)
    return Three(**info)


def cities():
    """Return a list of available cities."""
    info = find_info()
    return info


def discovery(path=None, **kwargs):
    """
    Check a city's Open311 discovery endpoint.

    >>> three.city('sf')
    >>> three.discovery()
    """
    return Three().discovery(path, **kwargs)


def post(code=None, **kwargs):
    """
    Send a POST service request to a city's Open311 endpoint.

    >>> three.city('sf')
    >>> three.post('123', address='155 9th St', name='Zach Williams',
    ...            phone='555-5555', description='My issue description'.)
    {'successful': {'request': 'post'}}
    """
    return Three().post(code, **kwargs)


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
