import unittest
from mock import Mock, call

from rapiduino.components.basic import LED
from rapiduino.globals.common import HIGH, LOW
from rapiduino.tests.components.mixin import TestComponentMixin


class TestLED(unittest.TestCase, TestComponentMixin):

    def setUp(self):
        self.component = LED()
        self.mock_device = Mock()
        self.component._bound_device = self.mock_device
        self.component._pins[0]._bound_to = (self.mock_device, 13)

    def test_turn_on(self):
        self.component.turn_on()
        self.mock_device.digital_write.assert_called_once_with(13, HIGH)

    def test_turn_off(self):
        self.component.turn_off()
        self.mock_device.digital_write.assert_called_once_with(13, LOW)

    def test_toggle(self):
        self.mock_device.digital_read.side_effect = [LOW, HIGH]
        digital_read_calls = [
            call(13),
            call(13)
        ]
        digital_write_calls = [
            call(13, HIGH),
            call(13, LOW)
        ]

        self.component.toggle()
        self.component.toggle()

        self.mock_device.digital_read.assert_has_calls(digital_read_calls)
        self.assertEqual(self.mock_device.digital_read.call_count, len(digital_read_calls))
        self.mock_device.digital_write.assert_has_calls(digital_write_calls)
        self.assertEqual(self.mock_device.digital_write.call_count, len(digital_write_calls))


if __name__ == '__main__':
    unittest.main()
