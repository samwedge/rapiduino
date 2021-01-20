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
from rapiduino.components import BaseComponent
from rapiduino.exceptions import (
    ComponentAlreadyRegisteredError,
    NotAnalogPinError,
    NotPwmPinError,
    PinAlreadyRegisteredError,
    PinDoesNotExistError,
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
        self.pin_register: Dict[int, BaseComponent] = {}

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

    def pin_mode(self, pin_no: int, mode: PinMode) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self.connection.process_command(CMD_PINMODE, pin_no, mode.value)

    def digital_read(self, pin_no: int) -> PinState:
        self._assert_valid_pin_number(pin_no)
        state = self.connection.process_command(CMD_DIGITALREAD, pin_no)
        if state[0] == 1:
            return HIGH
        else:
            return LOW

    def digital_write(self, pin_no: int, state: PinState) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_state(state)
        self.connection.process_command(CMD_DIGITALWRITE, pin_no, state.value)

    def analog_read(self, pin_no: int) -> int:
        self._assert_valid_pin_number(pin_no)
        self._assert_analog_pin(pin_no)
        return self.connection.process_command(CMD_ANALOGREAD, pin_no)[0]

    def analog_write(self, pin_no: int, value: int) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_analog_write_range(value)
        self._assert_pwm_pin(pin_no)
        self.connection.process_command(CMD_ANALOGWRITE, pin_no, value)

    def register_component(
        self, component: BaseComponent, pins: Tuple[int, ...]
    ) -> None:
        for pin in pins:
            if pin in self.pin_register:
                raise PinAlreadyRegisteredError(
                    f"Pin {pin} is already registered on this board"
                )
            if pin >= len(self._pins):
                raise PinDoesNotExistError(f"Pin {pin} does not exist on this board")
        if component in self.pin_register.values():
            raise ComponentAlreadyRegisteredError
        for pin in pins:
            self.pin_register[pin] = component

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
