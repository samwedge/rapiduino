from typing import Dict, Optional, Tuple, Type

from rapiduino.boards.pins import Pin, get_mega2560_pins, get_uno_pins
from rapiduino.communication.command_spec import (
    CMD_ANALOGREAD,
    CMD_ANALOGWRITE,
    CMD_DIGITALREAD,
    CMD_DIGITALWRITE,
    CMD_PARROT,
    CMD_PINMODE,
    CMD_POLL,
    CMD_VERSION,
)
from rapiduino.communication.serial import SerialConnection
from rapiduino.exceptions import (
    ComponentAlreadyRegisteredError,
    NotAnalogPinError,
    NotPwmPinError,
    PinAlreadyRegisteredError,
    PinDoesNotExistError,
    ProtectedPinError,
)
from rapiduino.globals.common import (
    HIGH,
    INPUT,
    INPUT_PULLUP,
    LOW,
    OUTPUT,
    PinMode,
    PinState,
)


class Arduino:
    def __init__(
        self,
        pins: Tuple[Pin, ...],
        port: Optional[str],
        conn_class: Type[SerialConnection] = SerialConnection,
    ) -> None:
        self._pins = pins
        self.connection = conn_class.build(port)
        self.pin_register: Dict[int, str] = {}

    @classmethod
    def uno(
        cls,
        port: Optional[str] = None,
        conn_class: Type[SerialConnection] = SerialConnection,
    ) -> "Arduino":
        return cls(get_uno_pins(), port, conn_class)

    @classmethod
    def mega2560(
        cls,
        port: Optional[str] = None,
        conn_class: Type[SerialConnection] = SerialConnection,
    ) -> "Arduino":
        return cls(get_mega2560_pins(), port, conn_class)

    @property
    def pins(self) -> Tuple[Pin, ...]:
        return self._pins

    def poll(self) -> int:
        return self.connection.process_command(CMD_POLL)[0]

    def parrot(self, value: int) -> int:
        return self.connection.process_command(CMD_PARROT, value)[0]

    def version(self) -> Tuple[int, ...]:
        return self.connection.process_command(CMD_VERSION)

    def pin_mode(self, pin_no: int, mode: PinMode, token: Optional[str] = None) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self._assert_pin_not_protected(pin_no, token)
        self.connection.process_command(CMD_PINMODE, pin_no, mode.value)

    def digital_read(self, pin_no: int, token: Optional[str] = None) -> PinState:
        self._assert_valid_pin_number(pin_no)
        self._assert_pin_not_protected(pin_no, token)
        state = self.connection.process_command(CMD_DIGITALREAD, pin_no)
        if state[0] == 1:
            return HIGH
        else:
            return LOW

    def digital_write(
        self, pin_no: int, state: PinState, token: Optional[str] = None
    ) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_state(state)
        self._assert_pin_not_protected(pin_no, token)
        self.connection.process_command(CMD_DIGITALWRITE, pin_no, state.value)

    def analog_read(self, pin_no: int, token: Optional[str] = None) -> int:
        self._assert_valid_pin_number(pin_no)
        self._assert_analog_pin(pin_no)
        self._assert_pin_not_protected(pin_no, token)
        return self.connection.process_command(CMD_ANALOGREAD, pin_no)[0]

    def analog_write(
        self, pin_no: int, value: int, token: Optional[str] = None
    ) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_analog_write_range(value)
        self._assert_pwm_pin(pin_no)
        self._assert_pin_not_protected(pin_no, token)
        self.connection.process_command(CMD_ANALOGWRITE, pin_no, value)

    def register_component(self, component_token: str, pins: Tuple[Pin, ...]) -> None:
        self._assert_requested_pins_are_valid(component_token, pins)
        for pin in pins:
            self.pin_register[pin.pin_id] = component_token

    def _assert_requested_pins_are_valid(
        self, component_token: str, pins: Tuple[Pin, ...]
    ) -> None:
        for pin in pins:
            if pin.pin_id in self.pin_register:
                raise PinAlreadyRegisteredError(
                    f"Pin {pin.pin_id} is already registered on this board"
                )
            if pin.pin_id >= len(self._pins):
                raise PinDoesNotExistError(
                    f"Pin {pin.pin_id} does not exist on this board"
                )
            if pin.is_analog and not self._pins[pin.pin_id].is_analog:
                raise NotAnalogPinError(
                    f"Component requires Pin {pin.pin_id} to be analog"
                )
            if pin.is_pwm and not self._pins[pin.pin_id].is_pwm:
                raise NotPwmPinError(f"Component requires Pin {pin.pin_id} to be pwm")
        if component_token in self.pin_register.values():
            raise ComponentAlreadyRegisteredError

    def _assert_valid_pin_number(self, pin_no: int) -> None:
        if (pin_no >= len(self.pins)) or (pin_no < 0):
            raise IndexError(
                f"Specified pin number {pin_no} is outside"
                f"pin range of {len(self.pins)}"
            )

    def _assert_analog_pin(self, pin_no: int) -> None:
        if not self.pins[pin_no].is_analog:
            raise NotAnalogPinError(
                f"cannot complete operation as analog=False for pin {pin_no}"
            )

    def _assert_pwm_pin(self, pin_no: int) -> None:
        if not self.pins[pin_no].is_pwm:
            raise NotPwmPinError(
                f"cannot complete operation as pwm=False for pin {pin_no}"
            )

    def _assert_pin_not_protected(self, pin_no: int, token: Optional[str]) -> None:
        if pin_no in self.pin_register and self.pin_register[pin_no] != token:
            if token is None:
                raise ProtectedPinError(
                    "Cannot perform this operation because "
                    "the pin is registered to a component"
                )
            else:
                raise ProtectedPinError(
                    "Cannot perform this operation because "
                    "the pin is registered to a different component"
                )

    @staticmethod
    def _assert_valid_analog_write_range(value: int) -> None:
        if (value < 0) or (value > 255):
            raise ValueError(
                f"Specified analog value {value} should be an int in the range 0 to 255"
            )

    @staticmethod
    def _assert_valid_pin_mode(mode: PinMode) -> None:
        if mode not in [INPUT, OUTPUT, INPUT_PULLUP]:
            raise ValueError(
                f"pin_mode must be INPUT, OUTPUT or INPUT_PULLUP"
                f"but {mode.name} was found"
            )

    @staticmethod
    def _assert_valid_pin_state(state: PinState) -> None:
        if state not in [HIGH, LOW]:
            raise ValueError(
                f"pin_state must be HIGH or LOW but {state.name} was found"
            )
