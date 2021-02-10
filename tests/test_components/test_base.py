from unittest.mock import Mock, call

import pytest

from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.communication.command_spec import (
    CMD_ANALOGREAD,
    CMD_ANALOGWRITE,
    CMD_DIGITALREAD,
    CMD_DIGITALWRITE,
    CMD_PINMODE,
)
from rapiduino.communication.serial import SerialConnection
from rapiduino.components.base_component import BaseComponent
from rapiduino.exceptions import (
    ComponentAlreadyRegisteredWithArduinoError,
    ComponentNotRegisteredWithArduinoError,
)
from rapiduino.globals.common import HIGH, INPUT, PinMode, PinState

DIGITAL_PIN_NUM = 2
PWM_PIN_NUM = 3
ANALOG_PIN_NUM = 14
ANALOG_WRITE_VALUE = 100


@pytest.fixture
def serial() -> Mock:
    mock = Mock(spec=SerialConnection)
    mock.build.return_value.process_command.return_value = (1,)
    return mock


@pytest.fixture
def arduino(serial: Mock) -> Arduino:
    arduino = Arduino.uno(port="", conn_class=serial)
    return arduino


class DummyComponent(BaseComponent):
    def __init__(
        self, arduino: Arduino, digital_pin_no: int, pwm_pin_no: int, analog_pin_no: int
    ) -> None:
        self.set_pins(
            Pin(digital_pin_no),
            Pin(pwm_pin_no, is_pwm=True),
            Pin(analog_pin_no, is_analog=True),
        )
        self.set_board(arduino)

    def _setup(self) -> None:
        self._pin_mode(DIGITAL_PIN_NUM, INPUT)
        self._digital_read(DIGITAL_PIN_NUM)
        self._digital_write(DIGITAL_PIN_NUM, HIGH)
        self._analog_read(ANALOG_PIN_NUM)
        self._analog_write(PWM_PIN_NUM, ANALOG_WRITE_VALUE)

    def pin_mode(self, pin_no: int, mode: PinMode) -> None:
        self._pin_mode(pin_no, mode)

    def digital_read(self, pin_no: int) -> PinState:
        return self._digital_read(pin_no)

    def digital_write(self, pin_no: int, state: PinState) -> None:
        self._digital_write(pin_no, state)

    def analog_read(self, pin_no: int) -> int:
        return self._analog_read(pin_no)

    def analog_write(self, pin_no: int, value: int) -> None:
        self._analog_write(pin_no, value)


@pytest.fixture
def dummy_component(arduino: Arduino) -> DummyComponent:
    return DummyComponent(arduino, DIGITAL_PIN_NUM, PWM_PIN_NUM, ANALOG_PIN_NUM)


def test_component_connect_runs_setup(
    serial: Mock, dummy_component: DummyComponent
) -> None:
    dummy_component.connect()

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
    ]
    assert calls == expected_calls


def test_component_connect_registers_component(
    dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()

    assert len(set(arduino.pin_register.values())) == 1


def test_component_connect_cannot_be_done_twice(
    dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    with pytest.raises(ComponentAlreadyRegisteredWithArduinoError):
        dummy_component.connect()


def test_component_disconnect_cannot_be_done_if_not_connected(
    dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.disconnect()


def test_component_disconnect_deregisters_component(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.disconnect()

    assert len(arduino.pin_register.values()) == 0


def test_pin_mode_if_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.pin_mode(DIGITAL_PIN_NUM, INPUT)

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
    ]
    assert calls == expected_calls


def test_digital_read_if_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.digital_read(DIGITAL_PIN_NUM)

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
    ]
    assert calls == expected_calls


def test_digital_write_if_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.digital_write(DIGITAL_PIN_NUM, HIGH)

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
    ]
    assert calls == expected_calls


def test_analog_read_if_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.analog_read(ANALOG_PIN_NUM)

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
    ]
    assert calls == expected_calls


def test_analog_write_if_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.analog_write(PWM_PIN_NUM, ANALOG_WRITE_VALUE)

    calls = serial.build.return_value.process_command.call_args_list
    expected_calls = [
        call(CMD_PINMODE, DIGITAL_PIN_NUM, INPUT.value),
        call(CMD_DIGITALREAD, DIGITAL_PIN_NUM),
        call(CMD_DIGITALWRITE, DIGITAL_PIN_NUM, HIGH.value),
        call(CMD_ANALOGREAD, ANALOG_PIN_NUM),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
        call(CMD_ANALOGWRITE, PWM_PIN_NUM, ANALOG_WRITE_VALUE),
    ]
    assert calls == expected_calls


def test_pin_mode_cannot_be_done_if_not_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.pin_mode(DIGITAL_PIN_NUM, INPUT)


def test_digital_read_cannot_be_done_if_not_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.digital_read(DIGITAL_PIN_NUM)


def test_digital_write_cannot_be_done_if_not_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.digital_write(DIGITAL_PIN_NUM, HIGH)


def test_analog_read_cannot_be_done_if_not_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.analog_read(DIGITAL_PIN_NUM)


def test_analog_write_cannot_be_done_if_not_connected(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    with pytest.raises(ComponentNotRegisteredWithArduinoError):
        dummy_component.analog_write(DIGITAL_PIN_NUM, ANALOG_WRITE_VALUE)
