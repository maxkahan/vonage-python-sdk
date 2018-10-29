Nexmo Client Library for Python
===============================

|PyPI version| |Build Status| |Coverage Status|

This is the Python client library for Nexmo's API. To use it you'll need
a Nexmo account. Sign up `for free at
nexmo.com <https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__.

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `SMS API <#sms-api>`__
-  `Voice API <#voice-api>`__
-  `Verify API <#verify-api>`__
-  `Number Insight API <#number-insight-api>`__
-  `Managing Secrets <#managing-secrets>`__
-  `Application API <#application-api>`__
-  `License <#license>`__

Installation
------------

To install the Python client library using pip:

::

    pip install nexmo

To upgrade your installed client library using pip:

::

    pip install nexmo --upgrade

Alternatively you can clone the repository:

::

    git clone git@github.com:Nexmo/nexmo-python.git

Usage
-----

Begin by importing the ``nexmo`` module:

.. code:: python

    import nexmo

Then construct a client object with your key and secret:

.. code:: python

    client = nexmo.Client(key=api_key, secret=api_secret)

For production, you can specify the ``NEXMO_API_KEY`` and
``NEXMO_API_SECRET`` environment variables instead of specifying the key
and secret explicitly.

For newer endpoints that support JWT authentication such as the Voice
API, you can also specify the ``application_id`` and ``private_key``
arguments:

.. code:: python

    client = nexmo.Client(application_id=application_id, private_key=private_key)

In order to check signatures for incoming webhook requests, you'll also
need to specify the ``signature_secret`` argument (or the
``NEXMO_SIGNATURE_SECRET`` environment variable).

SMS API
-------

Send a text message
~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})

    response = response['messages'][0]

    if response['status'] == '0':
      print('Sent message', response['message-id'])

      print('Remaining balance is', response['remaining-balance'])
    else:
      print('Error:', response['error-text'])

Docs:
`https://docs.nexmo.com/messaging/sms-api/api-reference#request <https://docs.nexmo.com/messaging/sms-api/api-reference#request?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Tell Nexmo the SMS was received
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following submits a successful conversion to Nexmo with the current
timestamp. This feature must be enabled on your account first.

.. code:: python

    response = client.submit_sms_conversion(message_id)

Voice API
---------

Make a call
~~~~~~~~~~~

.. code:: python

    response = client.create_call({
      'to': [{'type': 'phone', 'number': '14843331234'}],
      'from': {'type': 'phone', 'number': '14843335555'},
      'answer_url': ['https://example.com/answer']
    })

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_create <https://docs.nexmo.com/voice/voice-api/api-reference#call_create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a list of calls
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_calls()

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_retrieve <https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a single call
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_call(uuid)

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_retrieve\_single <https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Update a call
~~~~~~~~~~~~~

.. code:: python

    response = client.update_call(uuid, action='hangup')

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_modify\_single <https://docs.nexmo.com/voice/voice-api/api-reference#call_modify_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Stream audio to a call
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'

    response = client.send_audio(uuid, stream_url=stream_url)

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#stream\_put <https://docs.nexmo.com/voice/voice-api/api-reference#stream_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Stop streaming audio to a call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.stop_audio(uuid)

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#stream\_delete <https://docs.nexmo.com/voice/voice-api/api-reference#stream_delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Send a synthesized speech message to a call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.send_speech(uuid, text='Hello')

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#talk\_put <https://docs.nexmo.com/voice/voice-api/api-reference#talk_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Stop sending a synthesized speech message to a call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.stop_speech(uuid)

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#talk\_delete <https://docs.nexmo.com/voice/voice-api/api-reference#talk_delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Send DTMF tones to a call
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.send_dtmf(uuid, digits='1234')

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#dtmf\_put <https://docs.nexmo.com/voice/voice-api/api-reference#dtmf_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Get recording
~~~~~~~~~~~~~

.. code:: python

    response = client.get_recording(RECORDING_URL)

Verify API
----------

Start a verification
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.start_verification(number='441632960960', brand='MyApp')

    if response['status'] == '0':
      print('Started verification request_id=' + response['request_id'])
    else:
      print('Error:', response['error_text'])

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#vrequest <https://docs.nexmo.com/verify/api-reference/api-reference#vrequest?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

The response contains a verification request id which you will need to
store temporarily (in the session, database, url etc).

Check a verification
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.check_verification('00e6c3377e5348cdaf567e1417c707a5', code='1234')

    if response['status'] == '0':
      print('Verification complete, event_id=' + response['event_id'])
    else:
      print('Error:', response['error_text'])

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#check <https://docs.nexmo.com/verify/api-reference/api-reference#check?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

The verification request id comes from the call to the
start\_verification method. The PIN code is entered into your
application by the user.

Cancel a verification
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.cancel_verification('00e6c3377e5348cdaf567e1417c707a5')

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#control <https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Trigger next verification step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.trigger_next_verification_event('00e6c3377e5348cdaf567e1417c707a5')

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#control <https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Number Insight API
------------------

Basic Number Insight
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.get_basic_number_insight(number='447700900000')

Docs:
`https://docs.nexmo.com/number-insight/basic <https://docs.nexmo.com/number-insight/basic?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Standard Number Insight
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.get_standard_number_insight(number='447700900000')

Docs:
`https://docs.nexmo.com/number-insight/standard <https://docs.nexmo.com/number-insight/basic?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Advanced Number Insight
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.get_advanced_number_insight(number='447700900000')

Docs:
`https://docs.nexmo.com/number-insight/advanced <https://docs.nexmo.com/number-insight/advanced?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Managing Secrets
----------------

An API is provided to allow you to rotate your API secrets. You can
create a new secret (up to a maximum of two secrets) and delete the
existing one once all applications have been updated.

List Secrets
~~~~~~~~~~~~

``python secrets = client.list_secrets(API_KEY)``

Create A New Secret
~~~~~~~~~~~~~~~~~~~

Create a new secret (the created dates will help you know which is
which): ``python client.create_secret(API_KEY, 'awes0meNewSekret!!;');``

Delete A Secret
~~~~~~~~~~~~~~~

Delete the old secret (any application still using these credentials
will stop working):

.. code:: python

    client.delete_secret(API_KEY, 'my-secret-id')

Application API
---------------

Create an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.create_application(name='Example App', type='voice', answer_url=answer_url, event_url=event_url)

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#create <https://docs.nexmo.com/tools/application-api/api-reference#create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a list of applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_applications()

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#list <https://docs.nexmo.com/tools/application-api/api-reference#list?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a single application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_application(uuid)

Docs:
`https://developer.nexmo.com/api/application#retrieve-an-application <https://developer.nexmo.com/api/application#retrieve-an-application>`__

Update an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.update_application(uuid, answer_method='POST')

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#update <https://docs.nexmo.com/tools/application-api/api-reference#update?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Delete an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.delete_application(uuid)

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#delete <https://docs.nexmo.com/tools/application-api/api-reference#delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Validate webhook signatures
---------------------------

.. code:: python

    client = nexmo.Client(signature_secret='secret')

    if client.check_signature(request.query):
      # valid signature
    else:
      # invalid signature

Docs:
`https://docs.nexmo.com/messaging/signing-messages <https://docs.nexmo.com/messaging/signing-messages?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Note: you'll need to contact support@nexmo.com to enable message signing
on your account before you can validate webhook signatures.

JWT parameters
--------------

By default, the library generates short-lived tokens for JWT
authentication.

Use the auth method to specify parameters for a longer life token or to
specify a different token identifier:

.. code:: python

    client.auth(nbf=nbf, exp=exp, jti=jti)

Contributing
------------

We :heart: contributions! But if you plan to work on something big or
controversial, please `contact us <mailto:devrel@nexmo.com>`__ first!

We recommend working on ``nexmo-python`` with a
`virtualenv <https://virtualenv.pypa.io/en/stable/>`__. The following
command will install all the Python dependencies you need to run the
tests:

.. code:: bash

    make install

The tests are all written with pytest. You run them with:

.. code:: bash

    make test

License
-------

This library is released under the `MIT License <LICENSE.txt>`__

.. |PyPI version| image:: https://badge.fury.io/py/nexmo.svg
   :target: https://badge.fury.io/py/nexmo
.. |Build Status| image:: https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master
   :target: https://travis-ci.org/Nexmo/nexmo-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/Nexmo/nexmo-python/badge.svg?branch=master
   :target: https://coveralls.io/github/Nexmo/nexmo-python?branch=master
