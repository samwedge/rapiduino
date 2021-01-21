class RapiduinoError(Exception):
    pass


class SerialConnectionSendDataError(RapiduinoError):
    pass


class ReceiveDataSerialConnectionError(RapiduinoError):
    pass


class NotAnalogPinError(RapiduinoError):
    pass


class NotPwmPinError(RapiduinoError):
    pass


class PinAlreadyRegisteredError(RapiduinoError):
    pass


class ComponentAlreadyRegisteredError(RapiduinoError):
    pass


class PinDoesNotExistError(RapiduinoError):
    pass


class ProtectedPinError(RapiduinoError):
    pass
