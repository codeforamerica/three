"""
Unit tests for the Three Open311 API wrapper.
"""

import os
import unittest
from mock import Mock

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

    def test_first_argument_is_endpoint(self):
        t = Three('api.city.gov')
        self.assertEqual(t.endpoint, 'api.city.gov')

    def test_json_is_default_format(self):
        t = Three()
        self.assertEqual(t.format, 'json')

    def tearDown(self):
        os.environ['OPEN311_API_KEY'] = ''


class ThreeServices(unittest.TestCase):

    def setUp(self):
        req.get = Mock()

    def test_empty_services_call(self):
        t = Three('api.city.gov')
        t.services()
        req.get.assert_called_with('api.city.gov/services.json', params={})

    def test_specific_service_code(self):
        t = Three('api.city.gov')
        t.services('123')
        req.get.assert_called_with('api.city.gov/services/123.json', params={})

    def test_keyword_arguments_become_parameters(self):
        t = Three('api.city.gov')
        t.services('123', foo='bar')
        kw = {'foo': 'bar'}
        req.get.assert_called_with('api.city.gov/services/123.json', params=kw)


class ThreeRequests(unittest.TestCase):

    def setUp(self):
        req.get = Mock()

    def test_empty_requests_call(self):
        t = Three('api.city.gov')
        t.requests()
        req.get.assert_called_with('api.city.gov/requests.json', params={})


if __name__ == '__main__':
    unittest.main()
