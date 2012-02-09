"""
Unit tests for the Three Open311 API wrapper.
"""

import os
import unittest
from mock import Mock

from three import three
from three import Three
from three.three import requests as req


class ThreeInit(unittest.TestCase):

    def test_uninitialized_api_key(self):
        self.assertEqual(Three().api_key, '')

    def test_global_api_key(self):
        os.environ['OPEN311_API_KEY'] = 'OHAI'
        self.assertEqual(Three().api_key, 'OHAI')

    def test_default_format_is_json(self):
        self.assertEqual(Three().format, 'json')

    def test_format_can_be_set_to_xml(self):
        t = Three(format='xml')
        self.assertEqual(t.format, 'xml')

    def test_first_argument_is_endpoint(self):
        t = Three('api.city.gov')
        self.assertEqual(t.endpoint, 'https://api.city.gov/')

    def test_reset_method_reconfigures_defaults(self):
        t = Three('foo.bar')
        self.assertEqual(t.endpoint, 'https://foo.bar/')
        t.configure(endpoint='bar.bar')
        self.assertEqual(t.endpoint, 'https://bar.bar/')
        t.configure(endpoint='http://baz.bar')
        self.assertEqual(t.endpoint, 'http://baz.bar/')
        t.reset()
        self.assertEqual(t.endpoint, 'https://foo.bar/')

    def tearDown(self):
        os.environ['OPEN311_API_KEY'] = ''


class ThreeDiscovery(unittest.TestCase):

    def setUp(self):
        req.get = Mock()
        three.json = Mock()

    def test_default_discovery_method(self):
        t = Three('api.city.gov')
        t.discovery()
        expected = 'https://api.city.gov/discovery.json'
        req.get.assert_called_with(expected, params={})

    def test_discovery_url_argument(self):
        t = Three('api.city.gov')
        t.discovery('http://testing.gov/discovery.json')
        req.get.assert_called_with('http://testing.gov/discovery.json')


class ThreeServices(unittest.TestCase):

    def setUp(self):
        req.get = Mock()
        three.json = Mock()

    def test_empty_services_call(self):
        t = Three('api.city.gov')
        t.services()
        expected = 'https://api.city.gov/services.json'
        req.get.assert_called_with(expected, params={})

    def test_specific_service_code(self):
        t = Three('api.city.gov')
        t.services('123')
        expected = 'https://api.city.gov/services/123.json'
        req.get.assert_called_with(expected, params={})

    def test_keyword_arguments_become_parameters(self):
        t = Three('api.city.gov')
        t.services('123', foo='bar')
        params = {'foo': 'bar'}
        expected = 'https://api.city.gov/services/123.json'
        req.get.assert_called_with(expected, params=params)


class ThreeRequests(unittest.TestCase):

    def setUp(self):
        req.get = Mock()
        three.json = Mock()

    def test_empty_requests_call(self):
        t = Three('api.city.gov')
        t.requests()
        expected = 'https://api.city.gov/requests.json'
        req.get.assert_called_with(expected, params={})

    def test_requests_call_with_service_code(self):
        t = Three('api.city.gov')
        t.requests('123')
        params = {'service_code': '123'}
        expected = 'https://api.city.gov/requests.json'
        req.get.assert_called_with(expected, params=params)

    def test_requests_with_additional_keyword_arguments(self):
        t = Three('api.city.gov')
        t.requests('123', status='open')
        params = {'service_code': '123', 'status': 'open'}
        expected = 'https://api.city.gov/requests.json'
        req.get.assert_called_with(expected, params=params)


class ThreeRequest(unittest.TestCase):

    def setUp(self):
        req.get = Mock()
        three.json = Mock()

    def test_getting_a_specific_request(self):
        t = Three('api.city.gov')
        t.request('12345')
        expected = 'https://api.city.gov/requests/12345.json'
        req.get.assert_called_with(expected, params={})


class ThreePost(unittest.TestCase):

    def setUp(self):
        req.post = Mock()
        three.json = Mock()

    def test_a_default_post(self):
        t = Three('api.city.gov', api_key='my_api_key')
        t.post('123', name='Zach Williams', address='85 2nd Street')
        params = {'first_name': 'Zach', 'last_name': 'Williams',
                  'service_code': '123', 'address_string': '85 2nd Street',
                  'api_key': 'my_api_key'}
        expected = 'https://api.city.gov/requests.json'
        req.post.assert_called_with(expected, params=params)


class ThreeToken(unittest.TestCase):

    def setUp(self):
        req.get = Mock()
        three.json = Mock()

    def test_a_default_token_call(self):
        t = Three('api.city.gov')
        t.token('12345')
        expected = 'https://api.city.gov/tokens/12345.json'
        req.get.assert_called_with(expected, params={})


if __name__ == '__main__':
    unittest.main()
