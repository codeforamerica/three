"""
A dict of information needed to query city Open311 servers.
"""


class CityNotFound(Exception):
    pass


def find_info(name=None):
    """Find the needed city server information."""
    if not name:
        return servers.keys()
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
    'bloomington': {
        'endpoint': 'https://bloomington.in.gov/crm/open311/v2/'
    },
    'boston': {
        'endpoint': 'https://mayors24.cityofboston.gov/open311/v2/'
    },
    'brookline': {
        'endpoint': 'http://spot.brooklinema.gov/open311/v2/'
    },
    'grand rapids': {
        'endpoint': 'http://grcity.spotreporters.com/open311/v2/'
    },
    'macon': {
        'endpoint': 'http://seeclickfix.com/macon/open311/'
    },
    'new haven': {
        'endpoint': 'http://seeclickfix.com/new-haven/open311/'
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
    'toronto': {
        'endpoint': 'https://secure.toronto.ca/webwizard/ws/',
        'jurisdiction': 'toronto.ca'
    },
}
