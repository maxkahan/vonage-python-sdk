import vonage
# from message_classes import *

class Messages:
    def __init__(
        self,
        client=None,
        key=None,
        secret=None,
        signature_secret=None,
        signature_method=None
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = vonage.Client(
                    key=key,
                    secret=secret,
                    signature_secret=signature_secret,
                    signature_method=signature_method
                )
        except Exception as e:
            print(f'Error: {str(e)}')
        
    def send_message(self, params):
        return self._client.post(self._client.api_host(), "/v1/messages", params, header_auth=True)


