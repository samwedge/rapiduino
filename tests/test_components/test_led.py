from unittest.mock import ANY, Mock, call

import pytest

from rapiduino.boards.arduino import Arduino
from rapiduino.components.led import LED
from rapiduino.globals.common import HIGH, LOW, OUTPUT

PIN_NUM = 1
TOKEN = ANY


@pytest.fixture
def arduino() -> Mock:
    arduino = Mock(spec=Arduino)
    arduino.digital_read.side_effect = [LOW, HIGH]
    return arduino


@pytest.fixture
def led(arduino: Arduino) -> LED:
    return LED(arduino, PIN_NUM)


def test_setup(arduino: Mock, led: LED) -> None:
    assert arduino.pin_mode.call_args_list == [call(PIN_NUM, OUTPUT, TOKEN)]
    assert arduino.digital_write.call_args_list == [call(PIN_NUM, LOW, TOKEN)]


def test_turn_on(arduino: Mock, led: LED) -> None:
    led.turn_on()
    assert arduino.digital_write.call_args_list == [
        call(PIN_NUM, LOW, TOKEN),
        call(PIN_NUM, HIGH, TOKEN),
    ]


def test_turn_off(arduino: Mock, led: LED) -> None:
    led.turn_off()
    assert arduino.digital_write.call_args_list == [
        call(PIN_NUM, LOW, TOKEN),
        call(PIN_NUM, LOW, TOKEN),
    ]


def test_is_on(arduino: Mock, led: LED) -> None:
    assert led.is_on() is False
    led.turn_on()
    assert led.is_on() is True


def test_is_toggle(arduino: Mock, led: LED) -> None:
    led.toggle()
    led.toggle()
    assert arduino.digital_write.call_args_list == [
        call(PIN_NUM, LOW, TOKEN),
        call(PIN_NUM, HIGH, TOKEN),
        call(PIN_NUM, LOW, TOKEN),
    ]
