class RapiduinoError(Exception):
    pass


class SerialConnectionError(RapiduinoError):
    pass


class PinError(RapiduinoError):
    pass
