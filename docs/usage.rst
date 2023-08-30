Usage
=====


Using Alerts
------------
``pagerduty_api`` comes with an interface for PagerDuty called ``Alert``. All an
alert needs to be instantiated is a ``service_key``. This Service API Key is a
unique ID generated in PagerDuty for a Generic API Service.

.. code-block:: python

    from pagerduty_api import Alert

    alert = Alert(service_key='4baa5d20cfba466a5e075b02698f455c')
    

Trigger Alert
-------------
To trigger an alert, use ``.trigger()`` on the interface. If you don't pass in an
incident_key, one will be computed as the md5 hash of the description

.. code-block:: python

    from pagerduty_api import Alert


    alert = Alert(service_key='4baa5d20cfba466a5e075b02698f455c')
    alert.trigger(
        description='No data received',
        client='My Client',
        client_url='http://mysite.com',
        details={'some_key': 'some_value'}
    )

Acknowledge Alert
-----------------
To acknowledge an alert, use ``.acknowledge()`` on the interface. If you created
this alert with ``.trigger()``, you won't need to provide an ``incident_key``.

.. code-block:: python

    from pagerduty_api import Alert

    alert = Alert(service_key='4baa5d20cfba466a5e075b02698f455c')
    alert.acknowledge(
        incident_key='0ace123ba99999160f35ea3bd381a318',
        description='Working on it.',
        details={'some_key': 'some_value'}
    )

Resolve Alert
-------------
To resolve an alert, use ``.resolve()`` on the interface. If you created
this alert with ``.trigger()``, you won't need to provide an ``incident_key``.

.. code-block:: python

    from pagerduty_api import Alert

    alert = Alert(service_key='4baa5d20cfba466a5e075b02698f455c')
    alert.resolve(
        incident_key='0ace123ba99999160f35ea3bd381a318',
        description='Fixed it.',
        details={'some_key': 'some_value'}
    )
