import unittest
from unittest.mock import Mock

from rapiduino.pin import Pin


class TestComponentPin(unittest.TestCase):
    def setUp(self) -> None:
        self.pin_class = Pin
        self.analog_pwm_pin = Pin(0, is_pwm=True, is_analog=True)
        self.digital_pin = Pin(5)
        self.mock_instance = Mock()

    def test_init(self) -> None:
        self.assertIsInstance(self.digital_pin, self.pin_class)

    def test_defaults(self) -> None:
        self.assertFalse(self.digital_pin.is_pwm)
        self.assertFalse(self.digital_pin.is_analog)
        self.assertEqual(self.digital_pin.pin_id, 5)

    def test_pin_default_overrides(self) -> None:
        self.assertTrue(self.analog_pwm_pin.is_analog, True)
        self.assertTrue(self.analog_pwm_pin.is_pwm, True)
        self.assertEqual(self.analog_pwm_pin.pin_id, 0)
