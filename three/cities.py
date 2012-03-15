"""
A dict of information needed to query city Open311 servers.
"""


class CityNotFound(Exception):
    pass


def find_info(name):
    """Find the needed city server information."""
    name = name.lower()
    if name in servers:
        info = servers[name]
    else:
        raise CityNotFound("Could not find the specified city: %s" % name)
    return info


servers = {
    'baltimore': {
        'endpoint': 'http://311.baltimorecity.gov/open311/v2/'
    },
    'boston': {
        'endpoint': 'https://mayors24.cityofboston.gov/open311/v2/'
    },
    'grand rapids': {
        'endpoint': 'http://grcity.spotreporters.com/open311/v2/'
    },
    'san francisco': {
        'endpoint': 'https://open311.sfgov.org/V2/',
        'format': 'xml',
        'jurisdiction': 'sfgov.org'
    },
    'sf': {
        'endpoint': 'https://open311.sfgov.org/V2/',
        'format': 'xml',
        'jurisdiction': 'sfgov.org'
    },
}
