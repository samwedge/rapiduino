import unittest

from rapiduino.components.servo import Servo
from rapiduino.tests.components.mixin import TestComponentMixin


class TestServo(unittest.TestCase, TestComponentMixin):

    def setUp(self):
        self.component = Servo()

    def test_init(self):
        self.assertEqual(self.component.angle_min, 0)
        self.assertEqual(self.component.angle_max, 180)
        self.assertEqual(self.component.pwm_min, 0)
        self.assertEqual(self.component.pwm_max, 1023)

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
            self.component.pwm_min = -1
        with self.assertRaises(ValueError):
            self.component.pwm_max = 1024
        with self.assertRaises(ValueError):
            self.component.pwm_min = 1024
        with self.assertRaises(ValueError):
            self.component.pwm_max = -1

    def test_set_invalid_pwm(self):
        with self.assertRaises(ValueError):
            self.component.angle_min = -1
        with self.assertRaises(ValueError):
            self.component.angle_max = 181
        with self.assertRaises(ValueError):
            self.component.angle_min = 181
        with self.assertRaises(ValueError):
            self.component.angle_max = -1


if __name__ == '__main__':
    unittest.main()
