from typing import Tuple
from unittest.mock import Mock

import pytest

import rapiduino.globals.arduino_mega_2560 as mega_analog_alias
import rapiduino.globals.arduino_uno as uno_analog_alias
from rapiduino.boards.arduino import Arduino
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
    CommandSpec,
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
from rapiduino.globals.common import HIGH, INPUT, LOW, OUTPUT


@pytest.fixture
def test_arduino() -> Arduino:
    def dummy_process_command(command: CommandSpec, *args: int) -> Tuple[int, ...]:
        data: Tuple[int, ...]
        if command == CMD_POLL:
            data = (1,)
        elif command == CMD_PARROT:
            data = (args[0],)
        elif command == CMD_VERSION:
            data = (1, 2, 3)
        elif command == CMD_PINMODE:
            data = ()
        elif command == CMD_DIGITALREAD:
            data = (args[0],)
        elif command == CMD_DIGITALWRITE:
            data = ()
        elif command == CMD_ANALOGREAD:
            data = (100,)
        elif command == CMD_ANALOGWRITE:
            data = ()
        else:
            raise ValueError(f"Mock Arduino does not know how to process {CommandSpec}")
        return data

    pins = (Pin(0), Pin(1, is_analog=True), Pin(2, is_pwm=True), Pin(3))
    conn_class = Mock(spec=SerialConnection)
    conn_class.build.return_value.process_command.side_effect = dummy_process_command
    return Arduino(pins=pins, port=None, conn_class=conn_class)


@pytest.fixture
def test_component() -> BaseComponent:
    class TestComponent(BaseComponent):
        pass

    return TestComponent()


def test_poll(test_arduino: Arduino) -> None:
    assert test_arduino.poll() == 1


def test_parrot(test_arduino: Arduino) -> None:
    assert test_arduino.parrot(1) == 1
    assert test_arduino.parrot(2) == 2


def test_version(test_arduino: Arduino) -> None:
    assert test_arduino.version() == (1, 2, 3)


def test_pin_mode_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.pin_mode(0, INPUT)


def test_pin_mode_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(IndexError):
        test_arduino.pin_mode(4, OUTPUT)


def test_pin_mode_with_incorrect_mode(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.pin_mode(0, HIGH)  # type: ignore


def test_digital_read_with_valid_args_high(test_arduino: Arduino) -> None:
    state = test_arduino.digital_read(1)
    assert state == HIGH


def test_digital_read_with_valid_args_low(test_arduino: Arduino) -> None:
    state = test_arduino.digital_read(0)
    assert state == LOW


def test_digital_read_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(IndexError):
        test_arduino.digital_read(4)


def test_digital_write_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.digital_write(0, HIGH)


def test_digital_write_with_incorrect_state(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.digital_write(0, INPUT)  # type: ignore


def test_digital_write_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(IndexError):
        test_arduino.digital_write(4, HIGH)


def test_analog_read_with_valid_args(test_arduino: Arduino) -> None:
    state = test_arduino.analog_read(1)
    assert state == 100


def test_analog_read_with_non_analog_pin(test_arduino: Arduino) -> None:
    with pytest.raises(NotAnalogPinError):
        test_arduino.analog_read(0)


def test_analog_read_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(IndexError):
        test_arduino.analog_read(4)


def test_analog_write_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.analog_write(2, 100)


def test_analog_write_with_non_pwm_pin(test_arduino: Arduino) -> None:
    with pytest.raises(NotPwmPinError):
        test_arduino.analog_write(0, 100)


def test_analog_write_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(IndexError):
        test_arduino.analog_write(4, 0)


def test_analog_write_with_value_too_high(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.analog_write(2, 256)


def test_analog_write_with_negative_value(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.analog_write(2, -1)


def test_uno_pin_ids_are_sequential() -> None:
    for pin_no, pin in enumerate(get_uno_pins()):
        assert pin_no == pin.pin_id


def test_mega_pin_ids_are_sequential() -> None:
    for pin_no, pin in enumerate(get_mega2560_pins()):
        assert pin_no == pin.pin_id


def test_uno_classmethod_sets_correct_pins() -> None:
    arduino = Arduino.uno()
    assert arduino.pins == get_uno_pins()


def test_mega_classmethod_sets_correct_pins() -> None:
    arduino = Arduino.mega2560()
    assert arduino.pins == get_mega2560_pins()


def test_analog_alias_globals_refer_to_analog_pins_for_uno() -> None:
    analog_pins = [v for k, v in uno_analog_alias.__dict__.items() if k.startswith("A")]
    pins = get_uno_pins()
    for pin_alias in analog_pins:
        assert pins[pin_alias].is_analog


def test_all_analog_pins_have_an_alias_for_uno() -> None:
    analog_pins = [pin for pin in get_uno_pins() if pin.is_analog]
    for analog_alias_num, pin in enumerate(analog_pins):
        assert getattr(uno_analog_alias, f"A{analog_alias_num}") == pin.pin_id


def test_analog_alias_globals_refer_to_analog_pins_for_mega() -> None:
    analog_pins = [
        v for k, v in mega_analog_alias.__dict__.items() if k.startswith("A")
    ]
    pins = get_mega2560_pins()
    for pin_alias in analog_pins:
        assert pins[pin_alias].is_analog, f"Pin {pin_alias} should be an analog pin"


def test_all_analog_pins_have_an_alias_for_mega() -> None:
    analog_pins = [pin for pin in get_mega2560_pins() if pin.is_analog]
    for analog_alias_num, pin in enumerate(analog_pins):
        assert getattr(mega_analog_alias, f"A{analog_alias_num}") == pin.pin_id


def test_pins_cannot_be_reused(
    test_arduino: Arduino, test_component: BaseComponent
) -> None:
    test_arduino.register_component(test_component, pins=(0, 1))
    with pytest.raises(PinAlreadyRegisteredError):
        test_arduino.register_component(test_component, pins=(1, 2))


def test_component_can_only_be_registered_once(
    test_arduino: Arduino, test_component: BaseComponent
) -> None:
    test_arduino.register_component(test_component, pins=(0, 1))
    with pytest.raises(ComponentAlreadyRegisteredError):
        test_arduino.register_component(test_component, pins=(2, 3))


def test_pins_must_exist_for_component_to_exist(
    test_arduino: Arduino, test_component: BaseComponent
) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.register_component(test_component, pins=(4,))
