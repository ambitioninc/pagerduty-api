import os
from unittest import TestCase

import requests

from mock import patch, Mock

from pagerduty_api.base import AuthorizedResource, Resource
from pagerduty_api.exceptions import ConfigurationException, PagerDutyAPIServerException


class ResourceTests(TestCase):
    """
    Tests for Resource
    """

    def setUp(self):
        self.TEST_URL = 'https://www.google.com'

    @patch.object(requests, 'post')
    def test_post_not_ok(self, mock_post):
        """
        Test ._post() handles a not ok response
        """
        mock_response = Mock(name='response', ok=False, status_code=500, text='Server Error')
        mock_post.return_value = mock_response

        resource = Resource()

        with self.assertRaises(PagerDutyAPIServerException):
            resource._post(url=self.TEST_URL)

        mock_post.assert_called_once_with(
            url=self.TEST_URL,
        )


class AuthorizedResourceTests(TestCase):

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_with_arg(self, os_environ_mock):
        """
        Test the api_key gets set by an argument
        """

        resource = AuthorizedResource(api_key='123')

        self.assertFalse(os_environ_mock.called)

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_from_os(self, os_environ_mock):
        """
        Test the api_key gets set by the OS
        """
        os_environ_mock.return_value = '123'

        resource = AuthorizedResource()

        os_environ_mock.assert_called_once_with('PAGERDUTY_API_KEY')

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_raises_error(self, os_environ_mock):
        """
        Test the api_key is not set
        """
        os_environ_mock.return_value = None

        with self.assertRaises(ConfigurationException):
            AuthorizedResource()

        os_environ_mock.assert_called_once_with('PAGERDUTY_API_KEY')
