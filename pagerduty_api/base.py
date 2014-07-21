import os

from pagerduty_api.exceptions import ConfigurationException


class Resource(object):
    """
    A base class for API resources
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
