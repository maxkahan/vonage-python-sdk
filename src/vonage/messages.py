from .errors import MessagesError

import re
import json

class Messages:
    valid_message_channels = {'sms', 'mms', 'whatsapp', 'messenger', 'viber_service'}
    valid_message_types = {
        'sms': {'text'},
        'mms': {'image', 'vcard', 'audio', 'video'},
        'whatsapp': {'text', 'image', 'audio', 'video', 'file', 'template', 'custom'},
        'messenger': {'text', 'image', 'audio', 'video', 'file'},
        'viber_service': {'text', 'image'}
    }
    
    def __init__(self, client):
        self._client = client

    def send_message(self, params: dict, header_auth=False):        
        self.validate_send_message_input(params)

        json_formatted_params = json.dumps(params)
        if header_auth: # Using base64 encoded API key/secret pair
            return self._client.post(
                self._client.api_host(), 
                "/v1/messages",
                json_formatted_params, 
                header_auth=header_auth,
                additional_headers={'Content-Type': 'application/json'})
        else: # If using jwt auth
            return self._client._jwt_signed_post(
                "/v1/messages",
                params)

    def validate_send_message_input(self, params):
        self._check_input_is_dict(params)
        self._check_valid_message_channel(params)
        self._check_valid_message_type(params)
        self._check_valid_recipient(params)
        self._check_valid_sender(params)
        self._channel_specific_checks(params)
        self._check_valid_client_ref(params)
    
    def _check_input_is_dict(self, params):
        if type(params) is not dict:
            raise MessagesError(f'Parameters to the send_message method must be specified as a dictionary.')

    def _check_valid_message_channel(self, params):
        if params['channel'] not in Messages.valid_message_channels:
            raise MessagesError(f"""
            '{params['channel']}' is an invalid message channel. 
            Must be one of the following types: {self.valid_message_channels}'
            """)

    def _check_valid_message_type(self, params):
        if params['message_type'] not in self.valid_message_types[params['channel']]:
            raise MessagesError(f"""
                "{params['message_type']}" is not a valid message type for channel "{params["channel"]}". 
                Must be one of the following types: {self.valid_message_types[params["channel"]]}
            """)

    def _check_valid_recipient(self, params):
        if not isinstance(params['to'], str):
            raise MessagesError(f'Message recipient ("to={params["to"]}") not in a valid format.')
        elif params['channel'] != 'messenger' and not re.search(r'^[1-9]\d{6,14}$', params['to']):
            raise MessagesError(f'Message recipient number ("to={params["to"]}") not in a valid format.')
        elif params['channel'] == 'messenger' and not 0 < len(params['to']) < 50:
            raise MessagesError(f'Message recipient ID ("to={params["to"]}") not in a valid format.')

    def _check_valid_sender(self, params):
        if not isinstance(params['from'], str) or params['from'] == "":
            raise MessagesError(f'Message sender ("frm={params["from"]}") set incorrectly. Set a valid name or number for the sender.')

    def _channel_specific_checks(self, params):
        try:        
            if params['channel'] == 'whatsapp' and params['message_type'] == 'template':
                params['whatsapp']
            if params['channel'] == 'viber_service':
                params['viber_service']
        except (KeyError, TypeError):
            raise MessagesError(f'''You must specify all required properties for message channel "{params["channel"]}".''')

    def _check_valid_client_ref(self, params):
        if 'client_ref' in params:
            if len(params['client_ref']) <= 40:
                self._client_ref = params['client_ref']
            else:
                raise MessagesError('client_ref can be a maximum of 40 characters.')
