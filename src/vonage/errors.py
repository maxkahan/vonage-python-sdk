class Error(Exception):
    pass


class ClientError(Error):
    pass


class ServerError(Error):
    pass


class AuthenticationError(ClientError):
    pass


class CallbackRequiredError(Error):
    """
    Indicates a callback is required but was not present.
    """

class MessagesApiError(Error):
    """
    Indicates an error related to the Messages API.
    """

class InvalidMessageTypeError(Error):
    """
    Indicates that the supplied 'message_type' was invalid.
    """