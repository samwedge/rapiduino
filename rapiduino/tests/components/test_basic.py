import unittest2
from mock import Mock, call

from rapiduino.components.basic import LED
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.tests.components.mixin import TestComponentMixin


class TestLED(unittest2.TestCase, TestComponentMixin):

    def setUp(self):
        self.component = LED()
        self.mock_device = Mock()
        self.component._bound_device = self.mock_device
        self.component._pins[0]._bound_to = (self.mock_device, 13)

    def test_setup(self):
        self.component.setup()
        self.mock_device.pin_mode.assert_called_once_with(13, OUTPUT, force=True)
        self.mock_device.digital_write.assert_called_once_with(13, LOW, force=True)

    def test_turn_on(self):
        self.component.turn_on()
        self.mock_device.digital_write.assert_called_once_with(13, HIGH, force=True)

    def test_turn_off(self):
        self.component.turn_off()
        self.mock_device.digital_write.assert_called_once_with(13, LOW, force=True)

    def test_toggle(self):
        self.mock_device.digital_read.side_effect = [LOW, HIGH]
        digital_read_calls = [
            call(13, force=True),
            call(13, force=True)
        ]
        digital_write_calls = [
            call(13, HIGH, force=True),
            call(13, LOW, force=True)
        ]

        self.component.toggle()
        self.component.toggle()

        self.mock_device.digital_read.assert_has_calls(digital_read_calls)
        self.assertEqual(self.mock_device.digital_read.call_count, len(digital_read_calls))
        self.mock_device.digital_write.assert_has_calls(digital_write_calls)
        self.assertEqual(self.mock_device.digital_write.call_count, len(digital_write_calls))


if __name__ == '__main__':
    unittest2 .main()
