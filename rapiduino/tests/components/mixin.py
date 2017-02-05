from rapiduino.globals.common import OUTPUT, HIGH
from rapiduino.pin import ComponentPin
from rapiduino.components.base import BaseComponent


class TestComponentMixin(object):

    def test_subclass(self):
        self.assertTrue(isinstance(self.component, BaseComponent))
        for pin in self.component.pins:
            self.assertTrue(isinstance(pin, ComponentPin))

    def test_number_of_pins(self):
        self.assertEqual(len(self.component.pins), 1)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.component.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.component.pins = []
        self.assertIsInstance(self.component.pins, tuple)

    def test_device_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.component.bound_device = 0

    def test_digital_read(self):
        value = self.component._digital_read(13)
        self.mock_device.digital_read.assert_called_once_with(13, force=True)
        self.assertEqual(value, self.mock_device.digital_read.return_value)

    def test_digital_write(self):
        self.component._digital_write(13, HIGH)
        self.mock_device.digital_write.assert_called_once_with(13, HIGH, force=True)

    def test_analog_read(self):
        value = self.component._analog_read(13)
        self.mock_device.analog_read.assert_called_once_with(13, force=True)
        self.assertEqual(value, self.mock_device.analog_read.return_value)

    def test_analog_write(self):
        self.component._analog_write(13, 100)
        self.mock_device.analog_write.assert_called_once_with(13, 100, force=True)

    def test_pin_mode(self):
        self.component._pin_mode(13, OUTPUT)
        self.mock_device.pin_mode.assert_called_once_with(13, OUTPUT, force=True)
