"""
Unit tests for the Three Open311 API wrapper.
"""

import os
import json
import unittest
from datetime import date
from mock import Mock, MagicMock, patch

import three
import responses
from three import core, Three, CityNotFound
from three.core import requests as req


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

    def test_ssl_version(self):
        import ssl
        t = Three('foo.bar', ssl_version=ssl.PROTOCOL_TLSv1)
        poolmanager = t.session.adapters['https://'].poolmanager
        self.assertEqual(poolmanager.connection_pool_kw['ssl_version'],
                         ssl.PROTOCOL_TLSv1)

    def tearDown(self):
        os.environ['OPEN311_API_KEY'] = ''


@patch.object(req, 'Session', Mock())
class ThreeDiscovery(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_default_discovery_method(self):
        t = Three('api.city.gov')
        t.discovery()
        expected = 'https://api.city.gov/discovery.json'
        t.session.get.assert_called_with(expected, params={})

    def test_discovery_url_argument(self):
        t = Three('api.city.gov')
        t.discovery('http://testing.gov/discovery.json')
        t.session.get.assert_called_with('http://testing.gov/discovery.json')

    def test_city_discovery_keyword(self):
        t = Three('api.chicago.city', discovery='http://chi.api.gov')
        self.assertEqual(t.discovery_url, 'http://chi.api.gov')


@patch.object(req, 'Session', Mock())
class ThreeServices(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_empty_services_call(self):
        t = Three('api.city.gov')
        t.services()
        expected = 'https://api.city.gov/services.json'
        t.session.get.assert_called_with(expected, params={})

    def test_specific_service_code(self):
        t = Three('api.city.gov')
        t.services('123')
        expected = 'https://api.city.gov/services/123.json'
        t.session.get.assert_called_with(expected, params={})

    def test_keyword_arguments_become_parameters(self):
        t = Three('api.city.gov')
        t.services('123', foo='bar')
        params = {'foo': 'bar'}
        expected = 'https://api.city.gov/services/123.json'
        t.session.get.assert_called_with(expected, params=params)


@patch.object(req, 'Session', Mock())
class ThreeRequests(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_empty_requests_call(self):
        t = Three('api.city.gov')
        t.requests()
        expected = 'https://api.city.gov/requests.json'
        t.session.get.assert_called_with(expected, params={})

    def test_requests_call_with_service_code(self):
        t = Three('api.city.gov')
        t.requests('123')
        params = {'service_code': '123'}
        expected = 'https://api.city.gov/requests.json'
        t.session.get.assert_called_with(expected, params=params)

    def test_requests_with_additional_keyword_arguments(self):
        t = Three('api.city.gov')
        t.requests('123', status='open')
        params = {'service_code': '123', 'status': 'open'}
        expected = 'https://api.city.gov/requests.json'
        t.session.get.assert_called_with(expected, params=params)


@patch.object(req, 'Session', Mock())
class ThreeRequest(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_getting_a_specific_request(self):
        t = Three('api.city.gov')
        t.request('123')
        expected = 'https://api.city.gov/requests/123.json'
        t.session.get.assert_called_with(expected, params={})

    def test_start_and_end_keyword_arguments(self):
        t = Three('api.city.gov')
        t.request('456', start='03-01-2010', end='03-05-2010')
        expected = 'https://api.city.gov/requests/456.json'
        params = {
            'start_date': '2010-03-01T00:00:00Z',
            'end_date': '2010-03-05T00:00:00Z'
        }
        t.session.get.assert_called_with(expected, params=params)

    def test_only_start_keyword_arguments(self):
        t = Three('api.city.gov')
        t.request('456', start='03-01-2010')
        end_date = date.today().strftime('%Y-%m-%dT00:00:00Z')
        expected = 'https://api.city.gov/requests/456.json'
        params = {
            'start_date': '2010-03-01T00:00:00Z',
            'end_date': end_date
        }
        t.session.get.assert_called_with(expected, params=params)

    def test_between_keyword_argument(self):
        t = Three('api.city.gov')
        t.request('789', between=['03-01-2010', '03-05-2010'])
        expected = 'https://api.city.gov/requests/789.json'
        params = {
            'start_date': '2010-03-01T00:00:00Z',
            'end_date': '2010-03-05T00:00:00Z'
        }
        t.session.get.assert_called_with(expected, params=params)

    def test_shortened_between_keyword(self):
        t = Three('api.city.gov')
        dates = ('03-01-10', '03-05-10')
        t.request('123', between=dates)
        expected = 'https://api.city.gov/requests/123.json'
        params = {
            'start_date': '2010-03-01T00:00:00Z',
            'end_date': '2010-03-05T00:00:00Z'
        }
        t.session.get.assert_called_with(expected, params=params)

    def test_between_can_handle_datetimes(self):
        t = Three('api.city.gov')
        dates = (date(2010, 3, 10), date(2010, 3, 15))
        t.request('123', between=dates)
        expected = 'https://api.city.gov/requests/123.json'
        params = {
            'start_date': '2010-03-10T00:00:00Z',
            'end_date': '2010-03-15T00:00:00Z'
        }
        t.session.get.assert_called_with(expected, params=params)

@responses.activate
@patch.object(req, 'Session', Mock())
class ThreePost(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_a_default_post(self):
        responses.add(responses.POST, 'https://api.city.gov/requests.json',
                  body="""[
                  {
                    "service_request_id":293944,
                    "service_notice":"The City will inspect and require the responsible party to correct within 24 hours and/or issue a Correction Notice or Notice of Violation of the Public Works Code",
                    "account_id":null
                    }
                  ]""",
                  status=201,
                  content_type='application/json')

        t = Three('api.city.gov', api_key='my_api_key')
        resp = t.post('123', name='Zach Williams', address='85 2nd Street')
        params = {'first_name': 'Zach', 'last_name': 'Williams',
                  'service_code': '123', 'address_string': '85 2nd Street',
                  'api_key': 'my_api_key'}

        assert resp.status_code == 201

    def test_post_request_with_api_key_argument(self):
        t = Three('http://seeclicktest.com/open311/v2')
        t.post('1627', name='Zach Williams', address='120 Spring St',
               description='Just a test post.', phone='555-5555',
               api_key='my_api_key')
        params = {
            'first_name': 'Zach', 'last_name': 'Williams',
            'description': 'Just a test post.', 'service_code': '1627',
            'address_string': '120 Spring St', 'phone': '555-5555',
            'api_key': 'my_api_key'
        }
        expected = 'http://seeclicktest.com/open311/v2/requests.json'
        t.session.post.assert_called_with(expected, data=params, files=None)


@patch.object(req, 'Session', Mock())
class ThreeToken(unittest.TestCase):

    def setUp(self):
        core.json = Mock()

    def test_a_default_token_call(self):
        t = Three('api.city.gov')
        t.token('12345')
        expected = 'https://api.city.gov/tokens/12345.json'
        t.session.get.assert_called_with(expected, params={})


class TopLevelFunctions(unittest.TestCase):

    def setUp(self):
        self.session = Mock()
        self.patch = patch.object(req, 'Session',
                                  Mock(return_value=self.session))
        self.patch.start()
        core.json = MagicMock()

    def tearDown(self):
        self.patch.stop()

    def test_three_api(self):
        three.key('my_api_key')
        key = os.environ['OPEN311_API_KEY']
        self.assertEqual(key, 'my_api_key')

    def test_cities_function_returns_a_list(self):
        cities = three.cities()
        self.assertTrue(isinstance(cities, list))

    def test_three_city_info(self):
        three.city('sf')
        info = os.environ['OPEN311_CITY_INFO']
        self.assertTrue(info)

    def test_three_city_error(self):
        self.assertRaises(CityNotFound, three.city, 'this is made up')

    def test_three_discovery(self):
        three.city('new haven')
        three.discovery()
        self.assertTrue(self.session.get.called)

    def test_three_requests(self):
        three.city('macon')
        three.requests()
        self.assertTrue(self.session.get.called)

    def test_three_request_specific_report(self):
        three.city('macon')
        three.request('123abc')
        self.assertTrue(self.session.get.called)

    def test_three_services(self):
        three.city('sf')
        three.services()
        self.assertTrue(self.session.get.called)

    def test_three_token(self):
        three.token('123abc')
        three.services()
        self.assertTrue(self.session.get.called)

    def test_three_dev_functionality(self):
        three.dev('http://api.city.gov')
        environ = os.environ['OPEN311_CITY_INFO']
        expected = '{"endpoint": "http://api.city.gov"}'
        self.assertEqual(environ, expected)

    def test_three_dev_keyword_arguments(self):
        three.dev('http://api.city.gov', format='xml')
        environ = json.loads(os.environ['OPEN311_CITY_INFO'])
        expected = {"endpoint": "http://api.city.gov", "format": "xml"}
        self.assertEqual(environ, expected)

    def tearDown(self):
        os.environ['OPEN311_API_KEY'] = ''
        os.environ['OPEN311_CITY_INFO'] = ''


if __name__ == '__main__':
    unittest.main()
