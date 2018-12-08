class RapiduinoError(Exception):
    pass


class SerialConnectionSendDataError(RapiduinoError):
    pass


class SerialConnectionError(RapiduinoError):
    pass


class ReceiveDataSerialConnectionError(SerialConnectionError):
    pass


class NotConnectedSerialConnectionError(SerialConnectionError):
    pass


class PinError(RapiduinoError):
    pass


class NotAnalogPinError(PinError):
    pass


class NotPwmPinError(PinError):
    pass


class ProtectedPinError(PinError):
    pass


class AlreadyBoundPinError(PinError):
    pass


class NoDeviceBoundError(RapiduinoError):
    pass
