import logging

import json
import unittest
from mock import patch
import requests

from pagerduty_api.alerts import Alert
from pagerduty_api.exceptions import IncidentKeyException

logging.disable(logging.FATAL)
DUMMY_API_KEY = 'wieZvi9AY3uCj6zaQPZX'


class PagerDutyAlertTests(unittest.TestCase):

    def setUp(self):
        super(PagerDutyAlertTests, self).setUp()

        self.service_key = '4baa5d20cfba466a5e075b02698f455c'
        self.client = 'Apple'

        self.incident_key = '/alert/110'

        self.alert = Alert(service_key=self.service_key, api_key=DUMMY_API_KEY)

    @patch.object(requests, 'post')
    def test_trigger_assigns_incident_key(self, mock_post):
        """
        Test triggering an alert without an incident_key sets one for the alert
        """
        alert = Alert(service_key=self.service_key, api_key=DUMMY_API_KEY)

        self.assertIsNone(alert.incident_key)

        # Call the method
        alert.trigger(description='No data')

        # Assert we made one
        self.assertIsNotNone(alert.incident_key)

    @patch.object(requests, 'post')
    def test_trigger_success(self, mock_post):
        """
        Test .trigger() calls the correct endpoint with correct parameters
        """
        # Call the method
        self.alert.trigger(
            description='No data received',
            incident_key=self.incident_key,
            client='apple_0033c42e190872c508666ab6acbbd2e7',
            client_url='https://apple.ambition.com',
            details={'some_key': 'some_value'}
        )

        # Assert we made one
        mock_post.assert_called_once_with(
            data=json.dumps({
                'service_key': self.service_key,
                'event_type': 'trigger',
                'incident_key': self.incident_key,
                'description': 'No data received',
                'client': 'apple_0033c42e190872c508666ab6acbbd2e7',
                'client_url': 'https://apple.ambition.com',
                'details': {'some_key': 'some_value'},
            }),
            headers=self.alert.headers,
            url=self.alert.URL,
        )

    @patch.object(requests, 'post')
    def test_acknowledge_success(self, mock_post):
        """
        Test .acknowledge() calls the correct endpoint with correct parameters
        """
        # Call the method
        self.alert.acknowledge(
            incident_key=self.incident_key,
            description='No data received',
            details={'some_key': 'some_value'}
        )

        # Assert we made one
        mock_post.assert_called_once_with(
            data=json.dumps({
                'service_key': self.service_key,
                'event_type': 'acknowledge',
                'incident_key': self.incident_key,
                'description': 'No data received',
                'details': {'some_key': 'some_value'},
            }),
            headers=self.alert.headers,
            url=self.alert.URL,
        )

    @patch.object(requests, 'post')
    def test_acknowledge_raises_error(self, mock_post):
        """
        Test .acknowledge() raises an IncidentKeyException
        """
        alert = Alert(service_key=self.service_key, api_key=DUMMY_API_KEY)

        # Call the method
        with self.assertRaises(IncidentKeyException):
            alert.acknowledge(
                description='No data received',
                details={'some_key': 'some_value'}
            )

    @patch.object(requests, 'post')
    def test_resolve_success(self, mock_post):
        """
        Test .resolve() calls the correct endpoint with correct parameters
        """
        # Call the method
        self.alert.resolve(
            incident_key=self.incident_key,
            description='No data received',
            details={'some_key': 'some_value'}
        )

        # Assert we made one
        mock_post.assert_called_once_with(
            data=json.dumps({
                'service_key': self.service_key,
                'event_type': 'resolve',
                'incident_key': self.incident_key,
                'description': 'No data received',
                'details': {'some_key': 'some_value'},
            }),
            headers=self.alert.headers,
            url=self.alert.URL,
        )

    @patch.object(requests, 'post')
    def test_resolve_raises_error(self, mock_post):
        """
        Test .resolve() raises an IncidentKeyException
        """
        alert = Alert(service_key=self.service_key, api_key=DUMMY_API_KEY)

        # Call the method
        with self.assertRaises(IncidentKeyException):
            alert.resolve(
                description='No data received',
                details={'some_key': 'some_value'}
            )
