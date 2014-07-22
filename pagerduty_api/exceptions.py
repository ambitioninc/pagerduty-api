class ConfigurationException(Exception):
    """
    An exception for Configuration errors
    """
    message = 'There was an error in the configuration'


class IncidentKeyException(Exception):
    """
    An exception when no Incident Key exists
    """
    message = 'There was not an Incident Key for the alert'
