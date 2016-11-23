import unittest
from rapiduino.base import Pin


class TestPin(unittest.TestCase):

    def setUp(self):
        self.pin = Pin()

    def test_init(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(issubclass(Pin, object))

    def test_defaults(self):
        self.assertEqual(self.pin.pin_mode, 'INPUT')
        self.assertEqual(self.pin.pin_state, 'LOW')
        self.assertEqual(self.pin.is_pwm, False)
        self.assertEqual(self.pin.is_analog, False)

    def test_pin_mode_setget(self):
        self.pin.pin_mode = 'OUTPUT'
        self.assertEqual(self.pin.pin_mode, 'OUTPUT')
        self.pin.pin_mode = 'INPUT'
        self.assertEqual(self.pin.pin_mode, 'INPUT')
        self.pin.pin_mode = 'INPUT_PULLUP'
        self.assertEqual(self.pin.pin_mode, 'INPUT_PULLUP')
        with self.assertRaises(ValueError):
            self.pin.pin_mode = 'some_incorrect_value'

    def test_pin_state_setget(self):
        self.pin.pin_state = 'HIGH'
        self.assertEqual(self.pin.pin_state, 'HIGH')
        self.pin.pin_state = 'LOW'
        self.assertEqual(self.pin.pin_state, 'LOW')
        with self.assertRaises(ValueError):
            self.pin.pin_state = 'some_incorrect_value'

    def test_is_pwm_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.pin.is_pwm = True

    def test_is_analog_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.pin.is_analog = True

    def test_pin_preset_overrides(self):
        analog_pwm_pin = Pin(is_pwm=True, is_analog=True)
        self.assertEqual(analog_pwm_pin.is_analog, True)
        self.assertEqual(analog_pwm_pin.is_pwm, True)


if __name__ == '__main__':
    unittest.main()
