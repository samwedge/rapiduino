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
from rapiduino.components.base import BaseComponent
from rapiduino.globals.common import HIGH, INPUT

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
    def _setup(self) -> None:
        self._pin_mode(DIGITAL_PIN_NUM, INPUT)
        self._digital_read(DIGITAL_PIN_NUM)
        self._digital_write(DIGITAL_PIN_NUM, HIGH)
        self._analog_read(ANALOG_PIN_NUM)
        self._analog_write(PWM_PIN_NUM, ANALOG_WRITE_VALUE)


@pytest.fixture
def dummy_component(arduino: Arduino) -> DummyComponent:
    return DummyComponent(
        arduino, (Pin(DIGITAL_PIN_NUM), Pin(PWM_PIN_NUM), Pin(ANALOG_PIN_NUM))
    )


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


def test_component_disconnect_deregisters_component(
    serial: Mock, dummy_component: DummyComponent, arduino: Arduino
) -> None:
    dummy_component.connect()
    dummy_component.disconnect()

    assert len(arduino.pin_register.values()) == 0
