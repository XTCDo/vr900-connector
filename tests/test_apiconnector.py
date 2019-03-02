import json
import unittest

import responses

from tests.testutil import TestUtil
from vr900connector.api import urls, ApiError, ApiConnector


class ApiConnectorTest(unittest.TestCase):

    def setUp(self):
        self.connector = ApiConnector('user', 'pass', 'vr900-connector', TestUtil.temp_path())

    @responses.activate
    def tearDown(self):
        if self.connector:
            TestUtil.mock_logout()
            self.connector.logout()

    @responses.activate
    def test_login(self):
        with open(TestUtil.path('files/responses/facilities'), 'r') as file:
            facilities_data = json.loads(file.read())

        with open(TestUtil.path('files/responses/token'), 'r') as file:
            token_data = json.loads(file.read())

        responses.add(responses.POST, urls.new_token(), json=token_data, status=200)
        responses.add(responses.POST, urls.authenticate(), status=200)
        responses.add(responses.GET, urls.facilities_list(), json=facilities_data, status=200)

        data = self.connector.get(urls.facilities_list())
        self.assertEqual(facilities_data, data)
        self.assertEqual(4, len(responses.calls))
        self.assertEqual(urls.new_token(), responses.calls[0].request.url)
        self.assertEqual(urls.authenticate(), responses.calls[1].request.url)
        self.assertEqual(urls.facilities_list(), responses.calls[2].request.url)
        self.assertEqual(urls.facilities_list(), responses.calls[3].request.url)

    @responses.activate
    def test_re_login(self):
        serial_number = TestUtil.mock_full_auth_success()

        repeaters_url = urls.repeaters().format(serial_number=serial_number)
        responses.add(responses.GET, repeaters_url, status=401)

        try:
            self.connector.get(urls.repeaters())
            self.fail('Error expected')
        except ApiError as e:
            self.assertEqual(8, len(responses.calls))
            self.assertEqual(401, e.response.status_code)
            self.assertEqual(repeaters_url, e.response.url)
            self.assertEqual(repeaters_url, responses.calls[3].request.url)
            self.assertEqual(repeaters_url, responses.calls[7].request.url)

    @responses.activate
    def test_cookie_failed(self):
        with open(TestUtil.path('files/responses/token'), 'r') as file:
            token_data = json.loads(file.read())

        responses.add(responses.POST, urls.new_token(), json=token_data, status=200)
        responses.add(responses.POST, urls.authenticate(), status=401)

        try:
            self.connector.get(urls.facilities_list())
            self.fail("Error expected")
        except ApiError as e:
            self.assertEqual("Cannot get cookies", e.message)

    @responses.activate
    def test_login_wrong_authentication(self):
        with open(TestUtil.path('files/responses/wrong_token'), 'r') as file:
            token_data = json.loads(file.read())

        responses.add(responses.POST, urls.new_token(), json=token_data, status=401)

        try:
            self.connector.get(urls.facilities_list())
            self.fail("Error expected")
        except ApiError as e:
            self.assertEqual("Authentication failed", e.message)

    @responses.activate
    def test_put(self):
        serial = TestUtil.mock_full_auth_success()

        responses.add(responses.PUT, urls.rooms().format(serial_number=serial), json='', status=200)
        self.connector.put(urls.rooms())

        self.assertEqual(4, len(responses.calls))
        self.assertEqual('PUT', responses.calls[3].request.method)


    @responses.activate
    def test_post(self):
        serial = TestUtil.mock_full_auth_success()

        responses.add(responses.POST, urls.rooms().format(serial_number=serial), json='', status=200)
        self.connector.post(urls.rooms())

        self.assertEqual(4, len(responses.calls))
        self.assertEqual('POST', responses.calls[3].request.method)

    @responses.activate
    def test_delete(self):
        serial = TestUtil.mock_full_auth_success()

        responses.add(responses.DELETE, urls.rooms().format(serial_number=serial), json='', status=200)
        self.connector.delete(urls.rooms())

        self.assertEqual(4, len(responses.calls))
        self.assertEqual('DELETE', responses.calls[3].request.method)

    @responses.activate
    def test_cannot_get_serial(self):
        TestUtil.mock_authentication_success()
        TestUtil.mock_token_success()

        try:
            self.connector.get('')
        except ApiError as e:
            self.assertEqual("Cannot get serial number", e.message)


    # @responses.activate
    # def test_login_once(self):
    #     TestUtil.mock_auth_success()
    #
    #     self.connector.get(urls.facilities_list())
    #     self.connector.get(urls.facilities_list())
    #     self.assertEqual(len(responses.calls), 5)


if __name__ == '__main__':
    unittest.main()
