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
    'sf': {
        'endpoint': 'https://open311.sfgov.org/dev/V2/',
        'format': 'xml',
        'jurisdiction': 'sfgov.org'
    },
}
