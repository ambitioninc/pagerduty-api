class ConfigurationException(Exception):
    """
    An exception for Configuration errors
    """
    message = 'There was an error in the configuration'


class PagerDutyAPIServerException(Exception):
    """
    An exception for Pager Duty server errors
    """
    message = 'There was an error from Pager Duty'


class IncidentKeyException(Exception):
    """
    An exception when no Incident Key exists
    """
    message = 'There was not an Incident Key for the alert'
