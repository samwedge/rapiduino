from typing import Optional, Tuple

import rapiduino


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


class ArduinoSketchVersionIncompatibleError(Exception):
    def __init__(
        self, sketch_version: Tuple[int, ...], min_version: Tuple[int, int, int]
    ) -> None:
        sketch_version_str = (
            f"{sketch_version[0]}.{sketch_version[1]}.{sketch_version[2]}"
        )
        min_version_str = f"{min_version[0]}.{min_version[1]}.{min_version[2]}"
        max_version_str = f"{min_version[0] + 1}.0.0"

        message = (
            f"Arduino sketch version {sketch_version_str} is incompatible with"
            f" Rapiduino version {rapiduino.__version__}.\n"
            "Please upload a compatible sketch version:"
            f" Greater or equal to {min_version_str}, less than {max_version_str}"
        )
        super().__init__(message)
