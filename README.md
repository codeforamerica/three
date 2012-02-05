Three
=====

An updated [Open311 API](http://wiki.open311.org/GeoReport_v2) Python wrapper
that was built to be as absolute user-friendly and easy-to-use as
possible.


Installation
------------

This is still a work in progress, but you can `git clone` this repo and
run `python setup.py install` to check out the current progress.


Usage
-----

### API Key

If you have an Open311 API key that you always intend to use, rather
than initializing the `Three` class with it each time, you can set an
`OPEN311_API_KEY` environment variable on the command line.

    export OPEN311_API_KEY="MY_API_KEY"

Otherwise, you can initialize the class with your API key and endpoint.

    >>> from three import Three
    >>> t = Three('api.city.gov', api_key='my_api_key')


### Format

The default format for the `Three` wrapper is `JSON` -- although not all
[Open311 implementation support it](http://wiki.open311.org/GeoReport_v2#Format_Support).
This is done mainly for easy-of-use (remember, that's the over-arching
goal of the `Three` wrapper). You can, however, specifically request to
use `XML` as your format of choice.

    >>> t = Three('api.city.gov', format='xml')
    >>> t.format == 'xml'
    True


### Discovery

In order to use the [Open311 service discovery](http://wiki.open311.org/Service_Discovery),
simply envoke the `discovery` method.

    >>> from three import Three
    >>> t = Three('api.city.gov')
    >>> t.discovery()
    {'service': {'discovery': 'data'}}


### Services

To see the available services provided by an Open311 implementation, use
the `services` method.

    >>> t = Three('api.city.gov')
    >>> t.services()
    {'all': {'service_code': 'info'}}

You can also specify a specific service code to get information about.

    >>> t.services('033')
    {'033': {'service_code': 'info'}}
