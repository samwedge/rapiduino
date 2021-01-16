from typing import Optional, Tuple, Type, Union

from rapiduino import GlobalParameter
from rapiduino.commands import (
    CMD_ANALOGREAD,
    CMD_ANALOGWRITE,
    CMD_DIGITALREAD,
    CMD_DIGITALWRITE,
    CMD_PARROT,
    CMD_PINMODE,
    CMD_POLL,
    CMD_VERSION,
)
from rapiduino.communication import SerialConnection
from rapiduino.exceptions import NotAnalogPinError, NotPwmPinError
from rapiduino.globals.common import HIGH, INPUT, INPUT_PULLUP, LOW, OUTPUT
from rapiduino.pin import Pin


def _get_uno_pins() -> Tuple[Pin, ...]:
    return (
        Pin(0),
        Pin(1),
        Pin(2),
        Pin(3, is_pwm=True),
        Pin(4),
        Pin(5, is_pwm=True),
        Pin(6, is_pwm=True),
        Pin(7),
        Pin(8),
        Pin(9, is_pwm=True),
        Pin(10, is_pwm=True),
        Pin(11, is_pwm=True),
        Pin(12),
        Pin(13),
        Pin(14, is_analog=True),
        Pin(15, is_analog=True),
        Pin(16, is_analog=True),
        Pin(17, is_analog=True),
        Pin(18, is_analog=True),
        Pin(19, is_analog=True),
    )


def _get_mega2560_pins() -> Tuple[Pin, ...]:
    return (
        Pin(0),
        Pin(1),
        Pin(2, is_pwm=True),
        Pin(3, is_pwm=True),
        Pin(4, is_pwm=True),
        Pin(5, is_pwm=True),
        Pin(6, is_pwm=True),
        Pin(7, is_pwm=True),
        Pin(8, is_pwm=True),
        Pin(9, is_pwm=True),
        Pin(10, is_pwm=True),
        Pin(11, is_pwm=True),
        Pin(12, is_pwm=True),
        Pin(13, is_pwm=True),
        Pin(14),
        Pin(15),
        Pin(16),
        Pin(17),
        Pin(18),
        Pin(19),
        Pin(20),
        Pin(21),
        Pin(22),
        Pin(23),
        Pin(24),
        Pin(25),
        Pin(26),
        Pin(27),
        Pin(28),
        Pin(29),
        Pin(30),
        Pin(31),
        Pin(32),
        Pin(33),
        Pin(34),
        Pin(35),
        Pin(36),
        Pin(37),
        Pin(38),
        Pin(39),
        Pin(40),
        Pin(41),
        Pin(42),
        Pin(43),
        Pin(44, is_pwm=True),
        Pin(45, is_pwm=True),
        Pin(46, is_pwm=True),
        Pin(47),
        Pin(48),
        Pin(49),
        Pin(50),
        Pin(51),
        Pin(52),
        Pin(53),
        Pin(54, is_analog=True),
        Pin(55, is_analog=True),
        Pin(56, is_analog=True),
        Pin(57, is_analog=True),
        Pin(58, is_analog=True),
        Pin(59, is_analog=True),
        Pin(60, is_analog=True),
        Pin(61, is_analog=True),
        Pin(62, is_analog=True),
        Pin(63, is_analog=True),
        Pin(64, is_analog=True),
        Pin(65, is_analog=True),
        Pin(66, is_analog=True),
        Pin(67, is_analog=True),
        Pin(68, is_analog=True),
        Pin(69, is_analog=True),
    )


class Arduino:
    def __init__(
        self,
        pins: Tuple[Pin, ...],
        port: Optional[str],
        conn_class: Type[SerialConnection],
    ) -> None:
        self._pins = pins
        self.connection = conn_class.build(port)

    @classmethod
    def uno(
        cls,
        port: Optional[str] = None,
        conn_class: Type[SerialConnection] = SerialConnection,
    ) -> "Arduino":
        return cls(_get_uno_pins(), port, conn_class)

    @classmethod
    def mega2560(
        cls,
        port: Optional[str] = None,
        conn_class: Type[SerialConnection] = SerialConnection,
    ) -> "Arduino":
        return cls(_get_mega2560_pins(), port, conn_class)

    def poll(self) -> int:
        return self.connection.process_command(CMD_POLL)[0]

    def parrot(self, value: int) -> Optional[Union[int, Tuple[int, ...]]]:
        return self.connection.process_command(CMD_PARROT, value)[0]

    def version(self) -> Tuple[int, ...]:
        return self.connection.process_command(CMD_VERSION)

    def pin_mode(self, pin_no: int, mode: GlobalParameter) -> None:
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self.connection.process_command(CMD_PINMODE, pin_no, mode.value)

    def digital_read(self, pin_no: int) -> GlobalParameter:
        self._assert_valid_pin_number(pin_no)
        state = self.connection.process_command(CMD_DIGITALREAD, pin_no)
        if state[0] == 1:
            return HIGH
        else:
            return LOW

    def digital_write(self, pin_no: int, state: GlobalParameter) -> None:
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
        if not isinstance(value, int):
            raise TypeError(
                f"Expected analog value type to be int, but found {type(value)}"
            )
        if (value < 0) or (value > 255):
            raise ValueError(
                f"Specified analog value {value} is outside valid range 0 to 255"
            )

    @staticmethod
    def _assert_valid_pin_mode(mode: GlobalParameter) -> None:
        if not isinstance(mode, GlobalParameter):
            raise TypeError(f"Expected GlobalParameter but received type {type(mode)}")
        if mode not in [INPUT, OUTPUT, INPUT_PULLUP]:
            raise ValueError(
                f"pin_mode must be INPUT, OUTPUT orINPUT_PULLUP"
                f"but {mode.name} was found"
            )

    @staticmethod
    def _assert_valid_pin_state(state: GlobalParameter) -> None:
        if not isinstance(state, GlobalParameter):
            raise TypeError(f"Expected GlobalParameter but received type {type(state)}")
        if state not in [HIGH, LOW]:
            raise ValueError(
                f"pin_state must be HIGH or LOW but {state.name} was found"
            )

    @property
    def pins(self) -> Tuple[Pin, ...]:
        return self._pins
