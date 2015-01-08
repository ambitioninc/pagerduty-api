import json
import os

import requests

from pagerduty_api.exceptions import ConfigurationException, PagerDutyAPIServerException


class Resource(object):
    """
    A base class for API resources
    """
    @property
    def headers(self):
        return {
            'Content-type': 'application/json',
        }

    def _post(self, *args, **kwargs):
        """
        A wrapper for posting things. It will also json encode your 'data' parameter

        :returns: The response of your post
        :rtype: dict

        :raises: This will raise a
            :class:`PagerDutyAPIServerException<pagerduty_api.exceptions.PagerDutyAPIServerException>`
            if there is an error from Pager Duty
        """
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'], sort_keys=True)
        response = requests.post(*args, **kwargs)
        if not response.ok:
            raise PagerDutyAPIServerException('{}: {}'.format(response.status_code, response.text))
        return response.json()


class AuthorizedResource(object):
    """
    A base class for authorized API resources
    """
    def __init__(self, api_key=None, *args, **kwargs):
        """
        :type api_key: str
        :param api_key: The API key. If no key is passed, the environment
            variable PAGERDUTY_API_KEY is used.
        :raises: If the api_key parameter is not present, and no environment
            variable is present, a :class:`ConfigurationException <pagerduty_api.exceptions.ConfigurationException>`
            is raised.
        """
        self.api_key = api_key or os.environ.get('PAGERDUTY_API_KEY')

        if not self.api_key:
            raise ConfigurationException('PAGERDUTY_API_KEY not present in environment!')

        self.headers = {
            'Content-type': 'application/json',
            'Authorization': 'Token token={}'.format(api_key)
        }
