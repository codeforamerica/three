"""
Unit tests for the Three Open311 API wrapper.
"""

import os
import unittest
from mock import Mock

from three import three
from three import Three


class ThreeInit(unittest.TestCase):

    def test_uninitialized_api_key(self):
        self.assertEqual(Three().api_key, '')

    def test_global_api_key(self):
        os.environ['OPEN311_API_KEY'] = 'OHAI'
        self.assertEqual(Three().api_key, 'OHAI')

    def test_default_format_is_json(self):
        self.assertEqual(Three().format, 'json')

    def test_first_argument_is_endpoint(self):
        t = Three('api.sf311.gov')
        self.assertEqual(t.endpoint, 'api.sf311.gov')

    def tearDown(self):
        os.environ['OPEN311_API_KEY'] = ''


class ThreeServices(unittest.TestCase):

    def test_empty_services_call(self):
        t = Three('api.sf311.gov')
        t.get = Mock()
        t.services()
        t.get.assert_called_with('api.sf311.gov/services.json')


if __name__ == '__main__':
    unittest.main()
