import pytest

from rapiduino.boards.pins import Pin


@pytest.fixture
def default_pin() -> Pin:
    return Pin(0)


@pytest.fixture
def non_default_pin() -> Pin:
    return Pin(0, is_pwm=True, is_analog=True, is_reserved=True)


def test_defaults(default_pin: Pin) -> None:
    assert default_pin.pin_id == 0
    assert default_pin.is_pwm is False
    assert default_pin.is_analog is False
    assert default_pin.is_reserved is False


def test_pin_default_overrides(non_default_pin: Pin) -> None:
    assert non_default_pin.pin_id == 0
    assert non_default_pin.is_pwm is True
    assert non_default_pin.is_analog is True
    assert non_default_pin.is_reserved is True
