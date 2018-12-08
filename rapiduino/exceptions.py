class RapiduinoError(Exception):
    pass


class SerialConnectionSendDataError(RapiduinoError):
    pass


class SerialConnectionReceiveDataError(RapiduinoError):
    pass


class SerialConnectionNotConnectedError(RapiduinoError):
    pass


class PinError(RapiduinoError):
    pass
