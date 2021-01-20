import pytest

from rapiduino.boards.pins import Pin


@pytest.fixture
def digital_pin() -> Pin:
    return Pin(0)


@pytest.fixture
def analog_pwm_pin() -> Pin:
    return Pin(0, is_pwm=True, is_analog=True)


def test_defaults(digital_pin: Pin) -> None:
    assert digital_pin.pin_id == 0
    assert digital_pin.is_pwm is False
    assert digital_pin.is_analog is False


def test_pin_default_overrides(analog_pwm_pin: Pin) -> None:
    assert analog_pwm_pin.pin_id == 0
    assert analog_pwm_pin.is_pwm is True
    assert analog_pwm_pin.is_analog is True
