import hashlib
import logging

from .base import Resource
from .exceptions import IncidentKeyException

LOG = logging.getLogger(__name__)


class AlertTypes(object):
    TRIGGER = 'trigger'
    RESOLVE = 'resolve'
    ACKNOWLEDGE = 'acknowledge'


class Alert(Resource):
    """
    An interface for interacting with PagerDuty alerts.

    Instantiate with a service API key (A unique id for the service you want to
    trigger an alert for)

    """
    URL = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'

    def __init__(self, service_key, *args, **kwargs):
        """
        :type service_key: str
        :param service_key: Service API Key is a unique ID generated in
                PagerDuty for a Generic API Service
        """
        self.service_key = service_key
        self.incident_key = None

    def trigger(self, description, incident_key=None, client=None, client_url=None, details=None):
        """
        Triggers a PagerDuty Alert. See the `PagerDuty API trigger docs`_ for more details.

        .. _PagerDuty API trigger docs: http://developer.pagerduty.com/documentation/integration/events/trigger/

        :type description: str
        :param description: A Description of the alert. 1024 character max

        :type incident_key: str
        :param incident_key: A unique ID to de-duplicate incident reports. If
                no key is present, an MD5 hash of the description is used.

        :type client: str
        :param client: The name of the monitoring client that is triggering
                this event. Optional

        :type client_url: str
        :param client_url: The URL of the monitoring client that is triggering
                this event. Optional

        :type details: dict
        :param details: An arbitrary JSON object containing any data you'd like
                included in the incident log. Optional

        :rtype: dict
        :return: The JSON response of the API

            ::

                {
                    "status": "success",
                    "message": "Event processed",
                    "incident_key": "srv01/HTTP"
                }

        """

        if not incident_key:
            m = hashlib.md5()
            m.update(description.encode())
            incident_key = m.hexdigest()

        # The incident key is set for future operations
        self.incident_key = incident_key

        data = {
            'service_key': self.service_key,
            'event_type': AlertTypes.TRIGGER,
            'description': description,
            'incident_key': self.incident_key,
            'client': client,
            'client_url': client_url,
            'details': details
        }
        LOG.info('Triggering PagerDuty incident {0}'.format(incident_key))

        return self._post(
            url=self.URL,
            data=data,
            headers=self.headers
        )

    def acknowledge(self, incident_key=None, description=None, details=None):
        """
        Acknowledges a PagerDuty Alert. See the `PagerDuty API ack docs`_ for more details.

        .. _PagerDuty API ack docs: http://developer.pagerduty.com/documentation/integration/events/acknowledge/

        :type incident_key: str
        :param incident_key: The key for the incident to acknowledge. If None,
                it will use the incident key assigned when you triggered the alert.

        :type description: str
        :param description: Text that will appear in the incident's log
                associated with this event. Optional

        :type details: dict
        :param details: An arbitrary JSON object containing any data you'd like
                included in the incident log. Optional

        :raises: An :class:`IncidentKeyException <pagerduty_api.exceptions.IncidentKeyException>` if the Alert
                doesn't have an incident key and one is not passed to the method

        :rtype: dict
        :return: The JSON response of the API

            ::

                {
                    "status": "success",
                    "message": "Event processed",
                    "incident_key": "srv01/HTTP"
                }

        """
        incident_key = incident_key or self.incident_key

        if incident_key is None:
            raise IncidentKeyException()

        data = {
            'service_key': self.service_key,
            'event_type': AlertTypes.ACKNOWLEDGE,
            'description': description,
            'incident_key': incident_key,
            'details': details
        }
        LOG.info('Acknowledging PagerDuty incident {0}'.format(incident_key))

        return self._post(
            url=self.URL,
            data=data,
            headers=self.headers
        )

    def resolve(self, incident_key=None, description=None, details=None):
        """
        Resolves a PagerDuty Alert. See the `PagerDuty API resolve docs`_ for more details.

        .. _PagerDuty API resolve docs: http://developer.pagerduty.com/documentation/integration/events/resolve/

        :type incident_key: str
        :param incident_key: The key for the incident to resolve. If None, it
                will use the incident key assigned when you triggered the alert.

        :type description: str
        :param description: Text that will appear in the incident's log
                associated with this event. Optional

        :type details: dict
        :param details: An arbitrary JSON object containing any data you'd like
                included in the incident log. Optional

        :raises: An :class:`IncidentKeyException <pagerduty_api.exceptions.IncidentKeyException>` if the Alert
                doesn't have an incident key and one is not passed to the method

        :rtype: dict
        :return: The JSON response of the API

            ::

                {
                    "status": "success",
                    "message": "Event processed",
                    "incident_key": "srv01/HTTP"
                }

        """
        incident_key = incident_key or self.incident_key

        if incident_key is None:
            raise IncidentKeyException()

        data = {
            'service_key': self.service_key,
            'event_type': AlertTypes.RESOLVE,
            'description': description,
            'incident_key': incident_key,
            'details': details
        }
        LOG.info('Resolving PagerDuty incident {0}'.format(incident_key))

        return self._post(
            url=self.URL,
            data=data,
            headers=self.headers
        )
