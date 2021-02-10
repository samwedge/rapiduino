from typing import Optional


class SerialConnectionSendDataError(Exception):
    def __init__(self, n_bytes_intended: int, n_bytes_actual: int) -> None:
        message = (
            f"Transmitted {n_bytes_actual} bytes "
            f"but expected to transmit {n_bytes_intended} bytes"
        )
        super().__init__(message)


class SerialConnectionReceiveDataError(Exception):
    def __init__(self, n_bytes_intended: int, n_bytes_actual: int) -> None:
        message = (
            f"Received {n_bytes_actual} bytes "
            f"but expected to receive {n_bytes_intended} bytes"
        )
        super().__init__(message)


class NotAnalogPinError(Exception):
    def __init__(self, pin_no: int) -> None:
        message = f"cannot complete operation as is_analog=False for pin {pin_no}"
        super().__init__(message)


class NotPwmPinError(Exception):
    def __init__(self, pin_no: int) -> None:
        message = f"cannot complete operation as is_pwm=False for pin {pin_no}"
        super().__init__(message)


class PinAlreadyRegisteredError(Exception):
    def __init__(self, pin_no: int) -> None:
        message = f"Pin {pin_no} is already registered on this board"
        super().__init__(message)


class ComponentAlreadyRegisteredError(Exception):
    def __init__(self) -> None:
        message = "The component has already been registered to this board"
        super().__init__(message)


class PinDoesNotExistError(Exception):
    def __init__(self, pin_no: int) -> None:
        message = f"The specified pin number {pin_no} does not exist on this board"
        super().__init__(message)


class PinIsReservedForSerialCommsError(Exception):
    def __init__(self, pin_no: int) -> None:
        message = (
            f"Pin {pin_no} is reserved for serial comms and cannot be used"
            "for any other purpose"
        )
        super().__init__(message)


class ProtectedPinError(Exception):
    """The action cannot be completed because the specified pin is registered to a
    component"""

    def __init__(self, token: Optional[str]) -> None:
        base_message = "Cannot perform this operation because the pin is registered"
        if token is None:
            message = f"{base_message} to a component"
        else:
            message = f"{base_message} to a different component"
        super().__init__(message)


class ComponentNotRegisteredWithArduinoError(Exception):
    def __init__(self) -> None:
        message = "Device must be registered to an Arduino"
        super().__init__(message)


class ComponentAlreadyRegisteredWithArduinoError(Exception):
    def __init__(self) -> None:
        message = "Device is already registered to an Arduino"
        super().__init__(message)
