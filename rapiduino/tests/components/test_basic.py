import unittest2
from mock import Mock, call

from rapiduino.components.basic import LED, DimmableLED
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.pin import ComponentPin
from rapiduino.tests.components.mixin import TestComponentMixin


class TestLED(unittest2.TestCase, TestComponentMixin):

    def setUp(self):
        self.pin_num = 13
        self.pins = (
            ComponentPin(0),
        )
        self.component = LED()
        self.mock_device = Mock()
        self.component._bound_device = self.mock_device
        self.component._pins[0]._bound_to = (self.mock_device, self.pin_num)

    def test_setup(self):
        self.component.setup()
        self.mock_device.pin_mode.assert_called_once_with(self.pin_num, OUTPUT, force=True)
        self.mock_device.digital_write.assert_called_once_with(self.pin_num, LOW, force=True)

    def test_turn_on(self):
        self.component.turn_on()
        self.mock_device.digital_write.assert_called_once_with(self.pin_num, HIGH, force=True)

    def test_turn_off(self):
        self.component.turn_off()
        self.mock_device.digital_write.assert_called_once_with(self.pin_num, LOW, force=True)

    def test_toggle(self):
        self.mock_device.digital_read.side_effect = [LOW, HIGH]
        digital_read_calls = [
            call(self.pin_num, force=True),
            call(self.pin_num, force=True)
        ]
        digital_write_calls = [
            call(self.pin_num, HIGH, force=True),
            call(self.pin_num, LOW, force=True)
        ]

        self.component.toggle()
        self.component.toggle()

        self.mock_device.digital_read.assert_has_calls(digital_read_calls)
        self.assertEqual(self.mock_device.digital_read.call_count, len(digital_read_calls))
        self.mock_device.digital_write.assert_has_calls(digital_write_calls)
        self.assertEqual(self.mock_device.digital_write.call_count, len(digital_write_calls))


class TestDimmableLED(TestLED):
    def setUp(self):
        self.pin_num = 9
        self.pins = (
            ComponentPin(0, pwm=True),
        )
        self.component = DimmableLED()
        self.mock_device = Mock()
        self.component._bound_device = self.mock_device
        self.component._pins[0]._bound_to = (self.mock_device, self.pin_num)

    def test_set_brightness(self):
        self.component.set_brightness(100)
        self.mock_device.analog_write.assert_called_once_with(self.pin_num, 100, force=True)


if __name__ == '__main__':
    unittest2 .main()
