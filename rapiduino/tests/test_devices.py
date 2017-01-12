import unittest

from rapiduino.communication import Commands
from rapiduino.devices import ArduinoBase, ArduinoUno
from rapiduino.exceptions import PinError
from rapiduino.globals import *


class TestArduinoUno(unittest.TestCase):

    def setUp(self):
        self.device = ArduinoUno()

    def test_init(self):
        self.assertIsInstance(self.device._pins, tuple)
        self.assertIsInstance(self.device.commands, Commands)

    def test_subclass(self):
        self.assertIsInstance(self.device, ArduinoBase)

    def test_number_of_pins(self):
        self.assertEqual(len(self.device.pins), 20)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.device.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.device.pins = []
        self.assertIsInstance(self.device.pins, tuple)

    def test_pin_mode_sets_mode(self):
        self.device.pin_mode(0, OUTPUT)
        expected = (10, 0, OUTPUT.value)
        self.assertEqual(self.device.commands.next_command(), expected)

    def test_pin_mode_with_incorrect_mode(self):
        with self.assertRaises(ValueError):
            self.device.pin_mode(0, HIGH)

    def test_pin_mode_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.pin_mode(500, OUTPUT)

    def test_digital_read_gets_state(self):
        self.device.digital_read(0)
        expected = (20, 0)
        self.assertEqual(self.device.commands.next_command(), expected)

    def test_digital_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_read(500)

    def test_digital_write_sets_state(self):
        self.device.digital_write(0, HIGH)
        expected = (21, 0, HIGH.value)
        self.assertEqual(self.device.commands.next_command(), expected)

    def test_digital_write_with_incorrect_state(self):
        with self.assertRaises(ValueError):
            self.device.digital_write(0, OUTPUT)

    def test_digital_write_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_write(500, HIGH)

    def test_analog_read_gets_state(self):
        self.device.analog_read(0)
        expected = (30, 0)
        self.assertEqual(self.device.commands.next_command(), expected)

    def test_analog_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.analog_read(500)

    def test_analog_write_sets_state(self):
        self.device.analog_write(14, 100)
        expected = (31, 14, 100)
        self.assertEqual(self.device.commands.next_command(), expected)

    def test_analog_write_with_incorrect_state(self):
        with self.assertRaises(ValueError):
            self.device.analog_write(14, 500)
            self.device.analog_write(14, -1)
        with self.assertRaises(TypeError):
            self.device.analog_write(14, 10.1)

    def test_analog_write_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.analog_write(500, 100)

    def test_analog_write_on_non_analog_pin_raises_error(self):
        with self.assertRaisesRegexp(PinError, 'cannot complete operation as analog=False for pin 0'):
            self.device.analog_write(0, 1)

    def test_assert_valid_pin_number(self):
        for pin_no in range(20):
            self.device._assert_valid_pin_number(pin_no)
        with self.assertRaises(IndexError):
            self.device._assert_valid_pin_number(20)
        with self.assertRaises(IndexError):
            self.device._assert_valid_pin_number(-1)

    def test_assert_analog_pin(self):
        for pin_no in range(14):
            with self.assertRaisesRegexp(PinError, 'pin {}'.format(pin_no)):
                self.device._assert_analog_pin(pin_no)
        for pin_no in range(14, 20):
            self.device._assert_analog_pin(pin_no)

    def test_assert_analog_write_range(self):
        for integer in range(255):
            self.device._assert_valid_analog_write_range(integer)
        with self.assertRaises(ValueError):
            self.device._assert_valid_analog_write_range(256)
            self.device._assert_valid_analog_write_range(-1)
        with self.assertRaises(TypeError):
            self.device._assert_valid_analog_write_range(0.9)

    def test_assert_valid_pin_mode(self):
        with self.assertRaises(TypeError):
            self.device._assert_valid_pin_mode('INPUT')
        valid_modes = [INPUT, OUTPUT, INPUT_PULLUP]
        for mode in valid_modes:
            self.device._assert_valid_pin_mode(mode)
        with self.assertRaises(ValueError):
            self.device._assert_valid_pin_mode(HIGH)

    def test_assert_valid_pin_state(self):
        with self.assertRaises(TypeError):
            self.device._assert_valid_pin_state('LOW')
        valid_states = [LOW, HIGH]
        for state in valid_states:
            self.device._assert_valid_pin_state(state)
        with self.assertRaises(ValueError):
            self.device._assert_valid_pin_state(OUTPUT)


if __name__ == '__main__':
    unittest.main()
