from typing import Any, Tuple
from unittest.mock import Mock

import pytest

import rapiduino.globals.arduino_mega as mega_analog_alias
import rapiduino.globals.arduino_nano as nano_analog_alias
import rapiduino.globals.arduino_uno as uno_analog_alias
from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin, get_mega_pins, get_nano_pins, get_uno_pins
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
from rapiduino.exceptions import (
    ArduinoSketchVersionIncompatibleError,
    ComponentAlreadyRegisteredError,
    NotAnalogPinError,
    NotPwmPinError,
    PinAlreadyRegisteredError,
    PinDoesNotExistError,
    PinIsReservedForSerialCommsError,
    ProtectedPinError,
)
from rapiduino.globals.common import HIGH, INPUT, LOW, OUTPUT


def get_mock_conn_class() -> Mock:
    def dummy_process_command(command: CommandSpec, *args: int) -> Tuple[int, ...]:
        data: Tuple[int, ...]
        if command == CMD_POLL:
            data = (1,)
        elif command == CMD_PARROT:
            data = (args[0],)
        elif command == CMD_VERSION:
            data = Arduino.min_version
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

    mock_conn_class = Mock(spec=SerialConnection)
    mock_conn_class.build.return_value.process_command.side_effect = (
        dummy_process_command
    )

    return mock_conn_class


@pytest.fixture
def test_arduino() -> Arduino:
    pins = (
        Pin(0),
        Pin(1, is_analog=True),
        Pin(2, is_pwm=True),
        Pin(3),
        Pin(4),
        Pin(5),
    )
    return Arduino(
        pins=pins, port="", conn_class=get_mock_conn_class(), rx_pin=4, tx_pin=5
    )


def test_if_sketch_version_is_major_change_below_minimum_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0] - 1, v[1], v[2])
    conn_class.build.return_value.process_command.return_value = sketch_version
    with pytest.raises(ArduinoSketchVersionIncompatibleError):
        Arduino(pins=(), port="", conn_class=conn_class)


def test_if_sketch_version_is_minor_change_below_minimum_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0], v[1] - 1, v[2])
    conn_class.build.return_value.process_command.return_value = sketch_version
    with pytest.raises(ArduinoSketchVersionIncompatibleError):
        Arduino(pins=(), port="", conn_class=conn_class)


def test_if_sketch_version_is_micro_change_below_minimum_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0], v[1], v[2] - 1)
    conn_class.build.return_value.process_command.return_value = sketch_version
    with pytest.raises(ArduinoSketchVersionIncompatibleError):
        Arduino(pins=(), port="", conn_class=conn_class)


def test_if_sketch_version_is_a_major_change_above_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0] + 1, v[1], v[2])
    conn_class.build.return_value.process_command.return_value = sketch_version
    with pytest.raises(ArduinoSketchVersionIncompatibleError):
        Arduino(pins=(), port="", conn_class=conn_class)


def test_if_sketch_version_is_a_minor_change_above_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0], v[1] + 1, v[2])
    conn_class.build.return_value.process_command.return_value = sketch_version
    Arduino(pins=(), port="", conn_class=conn_class)


def test_if_sketch_version_is_a_micro_change_above_required_version() -> None:
    conn_class = Mock(spec=SerialConnection)
    v = Arduino.min_version
    sketch_version = (v[0], v[1], v[2] + 1)
    conn_class.build.return_value.process_command.return_value = sketch_version
    Arduino(pins=(), port="", conn_class=conn_class)


def test_poll(test_arduino: Arduino) -> None:
    assert test_arduino.poll() == 1


def test_parrot(test_arduino: Arduino) -> None:
    assert test_arduino.parrot(1) == 1
    assert test_arduino.parrot(2) == 2


def test_version(test_arduino: Arduino) -> None:
    assert test_arduino.version() == Arduino.min_version


def test_pin_mode_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.pin_mode(0, INPUT)


def test_pin_mode_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.pin_mode(6, OUTPUT)


def test_pin_mode_with_incorrect_mode(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.pin_mode(0, HIGH)  # type: ignore


def test_pin_mode_with_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.pin_mode(4, OUTPUT)


def test_digital_read_with_valid_args_high(test_arduino: Arduino) -> None:
    state = test_arduino.digital_read(1)
    assert state == HIGH


def test_digital_read_with_valid_args_low(test_arduino: Arduino) -> None:
    state = test_arduino.digital_read(0)
    assert state == LOW


def test_digital_read_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.digital_read(6)


def test_digital_read_with_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.digital_read(4)


def test_digital_write_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.digital_write(0, HIGH)


def test_digital_write_with_incorrect_state(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.digital_write(0, INPUT)  # type: ignore


def test_digital_write_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.digital_write(6, HIGH)


def test_digital_write_with_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.digital_write(4, HIGH)


def test_analog_read_with_valid_args(test_arduino: Arduino) -> None:
    state = test_arduino.analog_read(1)
    assert state == 100


def test_analog_read_with_non_analog_pin(test_arduino: Arduino) -> None:
    with pytest.raises(NotAnalogPinError):
        test_arduino.analog_read(0)


def test_analog_read_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.analog_read(6)


def test_analog_read_with_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.analog_read(4)


def test_analog_write_with_valid_args(test_arduino: Arduino) -> None:
    test_arduino.analog_write(2, 100)


def test_analog_write_with_non_pwm_pin(test_arduino: Arduino) -> None:
    with pytest.raises(NotPwmPinError):
        test_arduino.analog_write(0, 100)


def test_analog_write_with_pin_no_out_of_range(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.analog_write(6, 0)


def test_analog_write_with_value_too_high(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.analog_write(2, 256)


def test_analog_write_with_negative_value(test_arduino: Arduino) -> None:
    with pytest.raises(ValueError):
        test_arduino.analog_write(2, -1)


def test_analog_write_with_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.analog_write(4, 100)


def test_nano_pin_ids_are_sequential() -> None:
    for pin_no, pin in enumerate(get_nano_pins()):
        assert pin_no == pin.pin_id


def test_uno_pin_ids_are_sequential() -> None:
    for pin_no, pin in enumerate(get_uno_pins()):
        assert pin_no == pin.pin_id


def test_mega_pin_ids_are_sequential() -> None:
    for pin_no, pin in enumerate(get_mega_pins()):
        assert pin_no == pin.pin_id


@pytest.mark.parametrize(
    "arduino,expected_pins",
    [
        pytest.param(
            Arduino.uno(port="", conn_class=get_mock_conn_class()), get_uno_pins()
        ),
        pytest.param(
            Arduino.nano(port="", conn_class=get_mock_conn_class()), get_nano_pins()
        ),
        pytest.param(
            Arduino.mega(port="", conn_class=get_mock_conn_class()), get_mega_pins()
        ),
    ],
)
def test_classmethods_set_correct_pins(
    arduino: Arduino, expected_pins: Tuple[Pin, ...]
) -> None:
    assert arduino.pins == expected_pins


@pytest.mark.parametrize(
    "analog_alias,pins",
    [
        pytest.param(uno_analog_alias, get_uno_pins()),
        pytest.param(nano_analog_alias, get_nano_pins()),
        pytest.param(mega_analog_alias, get_mega_pins()),
    ],
)
def test_analog_alias_globals_refer_to_analog_pins(
    analog_alias: Any, pins: Tuple[Pin, ...]
) -> None:
    analog_pins = [v for k, v in analog_alias.__dict__.items() if k.startswith("A")]
    for pin_alias in analog_pins:
        assert pins[pin_alias].is_analog


@pytest.mark.parametrize(
    "analog_alias,pins",
    [
        pytest.param(uno_analog_alias, get_uno_pins()),
        pytest.param(nano_analog_alias, get_nano_pins()),
        pytest.param(mega_analog_alias, get_mega_pins()),
    ],
)
def test_all_analog_pins_have_an_alias(
    analog_alias: Any, pins: Tuple[Pin, ...]
) -> None:
    analog_pins = [pin for pin in pins if pin.is_analog]
    for analog_alias_num, pin in enumerate(analog_pins):
        assert getattr(analog_alias, f"A{analog_alias_num}") == pin.pin_id


@pytest.mark.parametrize(
    "arduino",
    [
        pytest.param(Arduino.uno(port="", conn_class=get_mock_conn_class())),
        pytest.param(Arduino.nano(port="", conn_class=get_mock_conn_class())),
        pytest.param(Arduino.mega(port="", conn_class=get_mock_conn_class())),
    ],
)
def test_serial_comms_pins_cannot_be_used(arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        arduino.digital_write(0, HIGH)
    with pytest.raises(PinIsReservedForSerialCommsError):
        arduino.digital_write(1, HIGH)


def test_pins_cannot_be_reused(test_arduino: Arduino) -> None:
    test_arduino.register_component("component_id_1", pins=(Pin(0), Pin(1)))
    with pytest.raises(PinAlreadyRegisteredError):
        test_arduino.register_component("component_id_2", pins=(Pin(1), Pin(2)))


def test_pins_cannot_be_registered_to_a_reserved_pin(test_arduino: Arduino) -> None:
    with pytest.raises(PinIsReservedForSerialCommsError):
        test_arduino.register_component("component_id_1", pins=(Pin(4),))


def test_component_can_only_be_registered_once(test_arduino: Arduino) -> None:
    test_arduino.register_component("component_id_1", pins=(Pin(0), Pin(1)))
    with pytest.raises(ComponentAlreadyRegisteredError):
        test_arduino.register_component("component_id_1", pins=(Pin(2), Pin(3)))


def test_pins_must_exist_for_component_to_exist(test_arduino: Arduino) -> None:
    with pytest.raises(PinDoesNotExistError):
        test_arduino.register_component("component_id_1", pins=(Pin(6),))


def test_pins_must_be_compatible_when_registering_a_pwm_pin(
    test_arduino: Arduino,
) -> None:
    with pytest.raises(NotPwmPinError):
        test_arduino.register_component("component_id_1", pins=(Pin(0, is_pwm=True),))


def test_pins_must_be_compatible_when_registering_an_analog_pin(
    test_arduino: Arduino,
) -> None:
    with pytest.raises(NotAnalogPinError):
        test_arduino.register_component(
            "component_id_1", pins=(Pin(0, is_analog=True),)
        )


def test_pin_mode_can_only_be_done_by_registered_component(
    test_arduino: Arduino,
) -> None:
    test_arduino.pin_mode(0, INPUT)

    test_arduino.register_component("component_id_1", pins=(Pin(0),))

    test_arduino.pin_mode(0, INPUT, token="component_id_1")
    with pytest.raises(ProtectedPinError):
        test_arduino.pin_mode(0, INPUT)
    with pytest.raises(ProtectedPinError):
        test_arduino.pin_mode(0, INPUT, token="component_id_2")


def test_digital_read_can_only_be_done_by_registered_component(
    test_arduino: Arduino,
) -> None:
    test_arduino.digital_read(0)

    test_arduino.register_component("component_id_1", pins=(Pin(0),))

    test_arduino.digital_read(0, token="component_id_1")
    with pytest.raises(ProtectedPinError):
        test_arduino.digital_read(0)
    with pytest.raises(ProtectedPinError):
        test_arduino.digital_read(0, token="component_id_2")


def test_digital_write_can_only_be_done_by_registered_component(
    test_arduino: Arduino,
) -> None:
    test_arduino.digital_write(0, HIGH)

    test_arduino.register_component("component_id_1", pins=(Pin(0),))

    test_arduino.digital_write(0, HIGH, token="component_id_1")
    with pytest.raises(ProtectedPinError):
        test_arduino.digital_write(0, HIGH)
    with pytest.raises(ProtectedPinError):
        test_arduino.digital_write(0, HIGH, token="component_id_2")


def test_analog_read_can_only_be_done_by_registered_component(
    test_arduino: Arduino,
) -> None:
    test_arduino.analog_read(1)

    test_arduino.register_component("component_id_1", pins=(Pin(1),))

    test_arduino.analog_read(1, token="component_id_1")
    with pytest.raises(ProtectedPinError):
        test_arduino.analog_read(1)
    with pytest.raises(ProtectedPinError):
        test_arduino.analog_read(1, token="component_id_2")


def test_analog_write_can_only_be_done_by_registered_component(
    test_arduino: Arduino,
) -> None:
    test_arduino.analog_write(2, 0)

    test_arduino.register_component("component_id_1", pins=(Pin(2),))

    test_arduino.analog_write(2, 1, token="component_id_1")
    with pytest.raises(ProtectedPinError):
        test_arduino.analog_write(2, 1)
    with pytest.raises(ProtectedPinError):
        test_arduino.analog_write(2, 1, token="component_id_2")


def test_component_can_be_re_registered_after_being_deregistered(
    test_arduino: Arduino,
) -> None:
    test_arduino.register_component("component_id_1", pins=(Pin(0), Pin(1)))
    test_arduino.deregister_component("component_id_1")
    test_arduino.register_component("component_id_1", pins=(Pin(2), Pin(3)))
