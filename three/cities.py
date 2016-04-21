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
    'bainbridge': {
        'endpoint': 'https://seeclickfix.com/open311/v2/38/'
    },
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
    'chicago': {
        'endpoint': 'http://311api.cityofchicago.org/open311/v2/',
        'discovery': 'http://311api.cityofchicago.org/open311/discovery.json'
    },
    'corona': {
        'endpoint': 'https://seeclickfix.com/open311/v2/70/'
    },
    'darwin': {
        'endpoint': 'https://seeclickfix.com/open311/v2/111/'
    },
    'dc': {
        'endpoint': 'http://app.311.dc.gov/CWI/Open311/v2/',
        'format': 'xml',
        'jurisdiction': 'dc.gov'
    },
    'district of columbia': {
        'endpoint': 'http://app.311.dc.gov/CWI/Open311/v2/',
        'format': 'xml',
        'jurisdiction': 'dc.gov'
    },
     'dunwoody': {
        'endpoint': 'https://seeclickfix.com/open311/v2/112/'
    },
    'fontana': {
        'endpoint': 'https://seeclickfix.com/open311/v2/159/'
    },
    'grand rapids': {
        'endpoint': 'http://grcity.spotreporters.com/open311/v2/'
    },
    'hillsborough': {
        'endpoint': 'https://seeclickfix.com/open311/v2/45/'
    },
    'howard county': {
        'endpoint': 'https://seeclickfix.com/open311/v2/520/'
    },
    'huntsville': {
        'endpoint': 'https://seeclickfix.com/open311/v2/145/'
    },
    'manor': {
        'endpoint': 'https://seeclickfix.com/open311/v2/33/'
    },
    'new haven': {
        'endpoint': 'https://seeclickfix.com/open311/v2/29/'
    },
    'newark': {
        'endpoint': 'https://seeclickfix.com/open311/v2/809/'
    },
    'newberg': {
        'endpoint': 'https://seeclickfix.com/open311/v2/122/'
    },
    'newnan': {
        'endpoint': 'https://seeclickfix.com/open311/v2/161/'
    },
    'olathe': {
        'endpoint': 'https://seeclickfix.com/open311/v2/106/'
    },
    'raleigh': {
        'endpoint': 'https://seeclickfix.com/open311/v2/149/'
    },
    'richmond': {
        'endpoint': 'https://seeclickfix.com/open311/v2/102/'
    },
    'roosevelt island': {
        'endpoint': 'https://seeclickfix.com/open311/v2/115/'
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
    }
}
