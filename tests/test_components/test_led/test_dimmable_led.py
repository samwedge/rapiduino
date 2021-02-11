from unittest.mock import ANY, Mock, call

import pytest

from rapiduino.boards.arduino import Arduino
from rapiduino.components.led.dimmable_led import DimmableLED
from rapiduino.globals.common import OUTPUT

PIN_NUM = 1
TOKEN = ANY


@pytest.fixture
def arduino() -> Mock:
    arduino = Mock(spec=Arduino)
    return arduino


@pytest.fixture
def led(arduino: Arduino) -> DimmableLED:
    return DimmableLED(arduino, PIN_NUM)


def test_setup(arduino: Mock, led: DimmableLED) -> None:
    assert arduino.pin_mode.call_args_list == [call(PIN_NUM, OUTPUT, TOKEN)]
    assert arduino.analog_write.call_args_list == [call(PIN_NUM, 0, TOKEN)]


def test_turn_on(arduino: Mock, led: DimmableLED) -> None:
    led.turn_on()
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
        call(PIN_NUM, 255, TOKEN),
    ]


def test_turn_off(arduino: Mock, led: DimmableLED) -> None:
    led.turn_off()
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
        call(PIN_NUM, 0, TOKEN),
    ]


def test_is_on(arduino: Mock, led: DimmableLED) -> None:
    assert led.is_on() is False
    led.turn_on()
    assert led.is_on() is True


def test_is_toggle(arduino: Mock, led: DimmableLED) -> None:
    led.toggle()
    led.toggle()
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
        call(PIN_NUM, 255, TOKEN),
        call(PIN_NUM, 0, TOKEN),
    ]


def test_brightness_when_on(arduino: Mock, led: DimmableLED) -> None:
    led.turn_on()
    led.brightness = 100
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
        call(PIN_NUM, 255, TOKEN),
        call(PIN_NUM, 100, TOKEN),
    ]
    assert led.brightness == 100


def test_brightness_when_off(arduino: Mock, led: DimmableLED) -> None:
    led.brightness = 100
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
    ]
    assert led.brightness == 100


def test_non_default_brightness_is_set_when_turning_on(
    arduino: Mock, led: DimmableLED
) -> None:
    led.brightness = 100
    led.turn_on()
    assert arduino.analog_write.call_args_list == [
        call(PIN_NUM, 0, TOKEN),
        call(PIN_NUM, 100, TOKEN),
    ]
    assert led.brightness == 100
