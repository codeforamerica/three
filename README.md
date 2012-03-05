Three
=====

An updated [Open311 API](http://wiki.open311.org/GeoReport_v2) Python wrapper
that was built to be as absolute **user-friendly** and **easy-to-use as
possible**. Many of the design decisions made will reflect these
qualities.


Installation
------------

This is still a work in progress, but you can `git clone` this repo and
run `python setup.py install` to check out the current progress.


Settings
--------

### API Key

If you have an Open311 API key that you always intend to use, rather
than initializing the `Three` class with it each time, you can set an
`OPEN311_API_KEY` environment variable on the command line.

    export OPEN311_API_KEY="MY_API_KEY"

Otherwise, you can initialize the class with your API key and endpoint.

    >>> from three import Three
    >>> t = Three('api.city.gov', api_key='my_api_key')


### HTTPS

By default, `Three` will configure a URL without a specified schema to
use `HTTPS`.

    >>> t = Three('api.city.gov')
    >>> t.endpoint == 'https://api.city.gov/'
    True


### Format

The default format for the `Three` wrapper is `JSON` -- although not all
[Open311 implementations support it](http://wiki.open311.org/GeoReport_v2#Format_Support).
This is done mainly for easy-of-use (remember, that's the over-arching
goal of the `Three` wrapper). You can, however, specifically request to
use `XML` as your format of choice.

    >>> t = Three('api.city.gov', format='xml')
    >>> t.format == 'xml'
    True


Usage
-----

### Configure

After you've initialized your `Three` class, you can readjust its
settings with the `configure` method. You can also switch back to the
orgininal settings with the `reset` method.

    >>> from three import Three
    >>> t = Three('api.city.gov', api_key='SECRET_KEY')
    >>> t.services()
    {'service': 'data'}

    >>> t.configure('open311.sfgov.org/dev/V2/', format='xml'
    ...             api_key='SF_OPEN311_API_KEY')
    >>> t.services()
    {'SF': {'service': 'data'}}

    >>> t.configure(api_key='ANOTHER_API_KEY')
    >>> # Switch back to original settings.
    ... t.reset()


### Discovery

In order to use the [Open311 service discovery](http://wiki.open311.org/Service_Discovery),
simply invoke the `discovery` method.

    >>> t = Three('api.city.gov')
    >>> t.discovery()
    {'service': {'discovery': 'data'}}

Sometimes, however, service discovery paths differ from service and
request URL paths -- in which case you can pass the specified URL to the
`discovery` method as an argument.

    >>> t.discovery('http://another.path.gov/discovery.json')


### Services

To see the available services provided by an Open311 implementation, use
the `services` method.

    >>> t = Three('api.city.gov')
    >>> t.services()
    {'all': {'service_code': 'info'}}

You can also specify a specific service code to get information about.

    >>> t.services('033')
    {'033': {'service_code': 'info'}}


### Requests

To see available request data, use the `requests` method.

    >>> t = Three('api.city.gov')
    >>> t.requests()
    {'all': {'requests': 'data'}}

[Most Open311
implementations](http://lists.open311.org/groups/discuss/messages/topic/2y4jI0eZulj9aZTVS3JgAj)
support `page_size` and `page` parameters.

    >>> t.requests(page_size=50)
    {'total': {'of': {'50': 'requests'}}}

    >>> t.requests(page=2, page_size=50)
    {'next': {'50': 'results'}}

You can also specify a specific service code.

    >>> t.requests('123')
    {'123': {'requests': 'data'}}

Other parameters can also be passed as keyword arguments.

    >>> t.requests('456', status='open')
    {'456': {'open': {'requests': 'data'}}}


### Request

If you're looking for information on a specific Open311 request (and you
have it's service code ID), you can use the `request` method.

    >>> t = Three('api.city.gov')
    >>> t.request('12345')
    {'request': {'service_code_id': {'12345': 'data'}}}


### Post

Sometimes you might need to programmatically create a new request, which
is what the `post` method can be used for. **NOTE**: the Open311 spec
states that all POST service requests [require a valid API
key](http://wiki.open311.org/GeoReport_v2#POST_Service_Request).

    >>> t = Three('api.city.gov', api_key='SECRET_KEY')
    >>> t.post('123', name='Zach Williams', address='85 2nd St',
    ...        description='New service code 123 request.')
    {'new': {'request': 'created'}}


### Token

Each service request ID can be tracked with a temporary token. If you
need to find the service request ID and have the request's token, you
can use the `token` method.

    >>> t = Three('api.city.gov')
    >>> t.token('12345')
    {'service_request_id': {'for': {'token': '12345'}}}
