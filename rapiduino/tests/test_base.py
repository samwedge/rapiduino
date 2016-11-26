import unittest
from rapiduino.base import Pin


class TestPin(unittest.TestCase):

    def setUp(self):
        self.analog_pwm_pin = Pin(0, is_pwm=True, is_analog=True)
        self.digital_pin = Pin(5)

    def test_init(self):
        self.assertIsInstance(self.digital_pin, Pin)
        self.assertTrue(issubclass(Pin, object))

    def test_defaults(self):
        self.assertEqual(self.digital_pin.pin_mode, 'INPUT')
        self.assertEqual(self.digital_pin.pin_state, 'LOW')
        self.assertEqual(self.digital_pin.is_pwm, False)
        self.assertEqual(self.digital_pin.is_analog, False)
        self.assertEqual(self.digital_pin.id, 5)

    def test_pin_default_overrides(self):
        self.assertEqual(self.analog_pwm_pin.pin_mode, 'INPUT')
        self.assertEqual(self.analog_pwm_pin.pin_state, 'LOW')
        self.assertEqual(self.analog_pwm_pin.is_analog, True)
        self.assertEqual(self.analog_pwm_pin.is_pwm, True)
        self.assertEqual(self.analog_pwm_pin.id, 0)

    def test_pin_mode_setget(self):
        self.digital_pin.pin_mode = 'OUTPUT'
        self.assertEqual(self.digital_pin.pin_mode, 'OUTPUT')
        self.digital_pin.pin_mode = 'INPUT'
        self.assertEqual(self.digital_pin.pin_mode, 'INPUT')
        self.digital_pin.pin_mode = 'INPUT_PULLUP'
        self.assertEqual(self.digital_pin.pin_mode, 'INPUT_PULLUP')
        with self.assertRaises(ValueError):
            self.digital_pin.pin_mode = 'some_incorrect_value'

    def test_pin_state_setget(self):
        self.digital_pin.pin_state = 'HIGH'
        self.assertEqual(self.digital_pin.pin_state, 'HIGH')
        self.digital_pin.pin_state = 'LOW'
        self.assertEqual(self.digital_pin.pin_state, 'LOW')
        with self.assertRaises(ValueError):
            self.digital_pin.pin_state = 'some_incorrect_value'

    def test_is_pwm_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_pwm = True

    def test_is_analog_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.is_analog = True

    def test_id_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.digital_pin.id = 0



if __name__ == '__main__':
    unittest.main()
