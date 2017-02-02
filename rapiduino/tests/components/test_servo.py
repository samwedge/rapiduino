import unittest

from rapiduino.base import Pin
from rapiduino.components.servo import Servo
from rapiduino.components.base import BaseComponent


class TestServo(unittest.TestCase):

    def setUp(self):
        self.servo = Servo()

    def test_init(self):
        self.assertEqual(self.servo.angle_min, 0)
        self.assertEqual(self.servo.angle_max, 180)
        self.assertEqual(self.servo.pwm_min, 0)
        self.assertEqual(self.servo.pwm_max, 1023)

    def test_init_with_invalid_pwm(self):
        with self.assertRaises(ValueError):
            Servo(pwm_min=-1)
        with self.assertRaises(ValueError):
            Servo(pwm_max=1024)
        with self.assertRaises(ValueError):
            Servo(pwm_min=1024)
        with self.assertRaises(ValueError):
            Servo(pwm_max=-1)

    def test_init_with_invalid_angle(self):
        with self.assertRaises(ValueError):
            Servo(angle_min=-1)
        with self.assertRaises(ValueError):
            Servo(angle_max=181)
        with self.assertRaises(ValueError):
            Servo(angle_min=181)
        with self.assertRaises(ValueError):
            Servo(angle_max=-1)

    def test_set_invalid_pwm(self):
        with self.assertRaises(ValueError):
            self.servo.pwm_min = -1
        with self.assertRaises(ValueError):
            self.servo.pwm_max = 1024
        with self.assertRaises(ValueError):
            self.servo.pwm_min = 1024
        with self.assertRaises(ValueError):
            self.servo.pwm_max = -1

    def test_set_invalid_pwm(self):
        with self.assertRaises(ValueError):
            self.servo.angle_min = -1
        with self.assertRaises(ValueError):
            self.servo.angle_max = 181
        with self.assertRaises(ValueError):
            self.servo.angle_min = 181
        with self.assertRaises(ValueError):
            self.servo.angle_max = -1

    def test_subclass(self):
        self.assertTrue(isinstance(self.servo, BaseComponent))
        for pin in self.servo.pins:
            self.assertTrue(isinstance(pin, Pin))

    def test_number_of_pins(self):
        self.assertEqual(len(self.servo.pins), 1)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.servo.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.servo.pins = []
        self.assertIsInstance(self.servo.pins, tuple)

    def test_device_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.servo.bound_device = 0


if __name__ == '__main__':
    unittest.main()
