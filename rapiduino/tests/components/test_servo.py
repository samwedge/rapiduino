from mock import Mock

from rapiduino.components.servo import Servo
from rapiduino.pin import ComponentPin
from rapiduino.tests.components.common import ComponentCommon


class TestServo(ComponentCommon.TestCase):

    def setUp(self):
        self.pin_num = 9
        self.pins = (
            ComponentPin(0, pwm=True),
        )
        self.component = Servo()
        self.mock_device = Mock()
        self.component._bound_device = self.mock_device
        self.component._pins[0]._bound_to = (self.mock_device, self.pin_num)

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

    def test_set_invalid_angle(self):
        with self.assertRaises(ValueError):
            self.component.angle_min = -1
        with self.assertRaises(ValueError):
            self.component.angle_max = 181
        with self.assertRaises(ValueError):
            self.component.angle_min = 181
        with self.assertRaises(ValueError):
            self.component.angle_max = -1
