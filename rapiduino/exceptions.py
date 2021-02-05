class RapiduinoError(Exception):
    """Inherited by all rapiduino errors to allow a catch-all"""


class SerialConnectionSendDataError(RapiduinoError):
    """Error in transmitting data. Not all sent bytes were reported as being received"""


class ReceiveDataSerialConnectionError(RapiduinoError):
    """Received a different number of bytes than specified by the CommandSped"""


class NotAnalogPinError(RapiduinoError):
    """This action requires an analog pin, which the specified pin does not support"""


class NotPwmPinError(RapiduinoError):
    """This action requires a pwm pin, which the specified pin does not support"""


class PinAlreadyRegisteredError(RapiduinoError):
    """The specified pin cannot be registered because it has been registered to a
    different component"""


class ComponentAlreadyRegisteredError(RapiduinoError):
    """The component has already been registered to this board"""


class PinDoesNotExistError(RapiduinoError):
    """You have specified a pin that does not exist on this board"""


class ProtectedPinError(RapiduinoError):
    """The action cannot be completed because the specified pin is registered to a
    component"""


class ComponentNotRegisteredWithArduinoError(RapiduinoError):
    """Action cannot be performed because the component is not registered to an
    Arduino"""


class ComponentAlreadyRegisteredWithArduinoError(RapiduinoError):
    """Action cannot be performed because the component is already registered
    to an Arduino"""
