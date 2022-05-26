from .errors import InvalidMessageTypeError

class BaseMessage(object):
    def __init__(self, to, sender, channel, message_type):
        self.to = to
        self.sender = sender
        self.channel = channel
        self.message_type = message_type

class SmsMessage(BaseMessage):
    def __init__(self, message_type='text'):
        self.valid_message_types = {'text'}
        if message_type == 'text':
            self.message_type = 'text'
        else:
            raise InvalidMessageTypeError

class MmsMessage(BaseMessage):
    def __init__(self, image):
        self.valid_message_types = {'image', 'vcard', 'audio', 'video'}
        if self.message_type not in self.valid_message_types:
            raise InvalidMessageTypeError

class WhatsAppMessage(BaseMessage):
    def __init__(self, message_type):
        self.valid_message_types = {'text', 'image', 'audio', 'video', 'file', 'template', 'custom'}
        if message_type in self.valid_message_types:
            self.message_type = message_type
        else:
            raise InvalidMessageTypeError

class MessengerMessage(BaseMessage):
     def __init__(self, message_type):
        self.valid_message_types = {'text', 'image', 'audio', 'video', 'file'}
        if message_type in self.valid_message_types:
            self.message_type = message_type
        else:
            raise InvalidMessageTypeError

class ViberMessage(BaseMessage):
    def __init__(self, message_type):
        self.valid_message_types = {'text', 'image'}
        if message_type in self.valid_message_types:
            self.message_type = message_type
        else:
            raise InvalidMessageTypeError
