import unittest
from unittest.mock import Mock

from rapiduino.pin import Pin
from rapiduino.exceptions import PinError


class TestComponentPin(unittest.TestCase):

    def setUp(self):
        self.pin_class = Pin
        self.analog_pwm_pin = Pin(0, pwm=True, analog=True)
        self.digital_pin = Pin(5)
        self.mock_instance = Mock()

    def test_init(self):
        self.assertIsInstance(self.digital_pin, self.pin_class)

    def test_defaults(self):
        self.assertFalse(self.digital_pin.is_pwm)
        self.assertFalse(self.digital_pin.is_analog)
        self.assertEqual(self.digital_pin.pin_id, 5)
        self.assertIsNone(self.digital_pin.bound_to)

    def test_pin_default_overrides(self):
        self.assertTrue(self.analog_pwm_pin.is_analog, True)
        self.assertTrue(self.analog_pwm_pin.is_pwm, True)
        self.assertEqual(self.analog_pwm_pin.pin_id, 0)

    def test_is_pwm_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_pwm = True

    def test_is_analog_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_analog = True

    def test_pin_id_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.pin_id = 0

    def test_bind(self):
        self.digital_pin.bind(self.mock_instance, 5)
        self.assertTupleEqual(self.digital_pin._bound_to, (self.mock_instance, 5))

    def test_bind_when_already_bound(self):
        self.digital_pin.bind(self.mock_instance, 5)
        self.assertTupleEqual(self.digital_pin._bound_to, (self.mock_instance, 5))
        with self.assertRaisesRegex(PinError, 'already bound'):
            self.digital_pin.bind(self.mock_instance, 5)

    def test_unbind(self):
        self.digital_pin.bind(self.mock_instance, 5)
        self.digital_pin.unbind()
        self.assertIsNone(self.digital_pin._bound_to)

    def test_bound_to(self):
        self.digital_pin._bound_to = (self.mock_instance, 5)
        self.assertTupleEqual(self.digital_pin.bound_to, (self.mock_instance, 5))

    def test_bound_to_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.bound_to = 0

    def test_bound_pin(self):
        self.digital_pin._bound_to = (self.mock_instance, 5)
        self.assertEqual(self.digital_pin.bound_pin_num, 5)

    def test_bound_instance(self):
        self.digital_pin._bound_to = (self.mock_instance, 5)
        self.assertEqual(self.digital_pin.bound_instance, self.mock_instance)

    def test_is_bound_when_bound(self):
        self.digital_pin.bind(self.mock_instance, 5)
        self.assertTrue(self.digital_pin.is_bound())

    def test_is_bound_when_not_bound(self):
        self.assertFalse(self.digital_pin.is_bound())
