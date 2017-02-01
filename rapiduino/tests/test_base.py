import unittest
from mock import Mock

from rapiduino.base import Pin


class TestPin(unittest.TestCase):

    def setUp(self):
        self.analog_pwm_pin = Pin(0, pwm=True, analog=True)
        self.digital_pin = Pin(5)

    def test_init(self):
        self.assertIsInstance(self.digital_pin, Pin)

    def test_defaults(self):
        self.assertEqual(self.digital_pin.is_pwm, False)
        self.assertEqual(self.digital_pin.is_analog, False)
        self.assertEqual(self.digital_pin.id, 5)
        self.assertIsNone(self.digital_pin.bound_to)

    def test_pin_default_overrides(self):
        self.assertEqual(self.analog_pwm_pin.is_analog, True)
        self.assertEqual(self.analog_pwm_pin.is_pwm, True)
        self.assertEqual(self.analog_pwm_pin.id, 0)

    def test_is_pwm_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_pwm = True

    def test_is_analog_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_analog = True

    def test_id_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.id = 0

    def test_bound_to_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.bound_to = 0

    def test_bind(self):
        mock_instance = Mock()
        self.digital_pin.bind(mock_instance, 5)
        binding = self.digital_pin.bound_to
        self.assertTupleEqual(binding, (mock_instance, 5))


if __name__ == '__main__':
    unittest.main()
