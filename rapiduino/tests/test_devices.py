import unittest

from mock import Mock

from rapiduino.communication import Connection, SerialConnection
from rapiduino.devices import ArduinoBase, ArduinoUno, ArduinoMega2560
from rapiduino.exceptions import PinError
from rapiduino.globals import *


class TestArduinoMixin(object):

    def setup_mixin(self):
        self.valid_analog_pin = self.valid_analog_pins[0]
        self.valid_digital_pin = self.valid_pins[0]
        self.valid_pwm_pin = self.valid_pwm_pins[0]

        self.num_pins = len(self.valid_pins)
        self.out_of_range_pin = self.num_pins

        self.invalid_analog_pin = None
        self.invalid_pwm_pin = None
        for pin_num in self.valid_pins:
            if (self.invalid_analog_pin is None) and (pin_num not in self.valid_analog_pins):
                self.invalid_analog_pin = pin_num
            if (self.invalid_pwm_pin is None) and (pin_num not in self.valid_pwm_pins):
                self.invalid_pwm_pin = pin_num
            if (self.invalid_analog_pin is not None) and (self.invalid_pwm_pin is not None):
                break

        self.mocked_send = Mock()
        self.mocked_recv = Mock()
        self.device.connection._send = self.mocked_send
        self.device.connection._recv = self.mocked_recv

    def test_init(self):
        self.assertIsInstance(self.device._pins, tuple)
        self.assertIsInstance(self.device.connection, SerialConnection)
        self.assertIsInstance(self.device.connection, Connection)

    def test_subclass(self):
        self.assertTrue(isinstance(self.device, ArduinoBase))

    def test_number_of_pins(self):
        self.assertEqual(len(self.device.pins), self.num_pins)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.device.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.device.pins = []
        self.assertIsInstance(self.device.pins, tuple)

    def test_pin_mode_sets_mode(self):
        self.device.pin_mode(self.valid_digital_pin, OUTPUT)
        pin_mode_cmd_spec = {
            'cmd': 10,
            'tx_len': 2,
            'tx_type': 'B',
            'rx_len': 0,
            'rx_type': ''
        }
        self.mocked_send.assert_called_once_with(pin_mode_cmd_spec, (self.valid_digital_pin, OUTPUT.value))

    def test_pin_mode_with_incorrect_mode(self):
        with self.assertRaises(ValueError):
            self.device.pin_mode(self.valid_digital_pin, HIGH)

    def test_pin_mode_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.pin_mode(self.out_of_range_pin, OUTPUT)

    def test_digital_read_gets_state(self):
        self.device.digital_read(self.valid_digital_pin)
        digital_read_cmd_spec = {
            'cmd': 20,
            'tx_len': 1,
            'tx_type': 'B',
            'rx_len': 1,
            'rx_type': 'B'
        }
        self.mocked_send.assert_called_once_with(digital_read_cmd_spec, (self.valid_digital_pin,))

    def test_digital_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_read(self.out_of_range_pin)

    def test_digital_write_sets_state(self):
        self.device.digital_write(self.valid_digital_pin, HIGH)
        digital_write_cmd_spec = {
            'cmd': 21,
            'tx_len': 2,
            'tx_type': 'B',
            'rx_len': 0,
            'rx_type': ''
        }
        self.mocked_send.assert_called_once_with(digital_write_cmd_spec, (self.valid_digital_pin, HIGH.value))

    def test_digital_write_with_incorrect_state(self):
        with self.assertRaises(ValueError):
            self.device.digital_write(self.valid_digital_pin, OUTPUT)

    def test_digital_write_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_write(self.out_of_range_pin, HIGH)

    def test_analog_read_gets_state(self):
        self.device.analog_read(self.valid_analog_pin)
        analog_read_cmd_spec = {
            'cmd': 30,
            'tx_len': 1,
            'tx_type': 'B',
            'rx_len': 1,
            'rx_type': 'H'
        }
        self.mocked_send.assert_called_once_with(analog_read_cmd_spec, (self.valid_analog_pin,))

    def test_analog_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.analog_read(self.out_of_range_pin)

    def test_analog_read_on_non_analog_pin_raises_error(self):
        with self.assertRaisesRegexp(PinError, 'cannot complete operation as analog=False for pin {}'.format(self.invalid_analog_pin)):
            self.device.analog_read(self.invalid_analog_pin)

    def test_analog_write_sets_state(self):
        self.device.analog_write(self.valid_pwm_pin, 100)
        analog_write_cmd_spec = {
            'cmd': 31,
            'tx_len': 2,
            'tx_type': 'B',
            'rx_len': 0,
            'rx_type': ''
        }
        self.mocked_send.assert_called_once_with(analog_write_cmd_spec, (self.valid_pwm_pin, 100))

    def test_analog_write_with_incorrect_state(self):
        with self.assertRaises(ValueError):
            self.device.analog_write(self.valid_pwm_pin, self.out_of_range_pin)
            self.device.analog_write(self.valid_pwm_pin, -1)
        with self.assertRaises(TypeError):
            self.device.analog_write(self.valid_pwm_pin, 10.1)

    def test_analog_write_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.analog_write(self.out_of_range_pin, 100)

    def test_analog_write_on_non_pwm_pin_raises_error(self):
        with self.assertRaisesRegexp(PinError, 'cannot complete operation as pwm=False for pin {}'.format(self.invalid_pwm_pin)):
            self.device.analog_write(self.invalid_pwm_pin, self.invalid_pwm_pin)

    def test_assert_valid_pin_number(self):
        for pin_no in range(self.num_pins):
            self.device._assert_valid_pin_number(pin_no)
        with self.assertRaises(IndexError):
            self.device._assert_valid_pin_number(self.num_pins)
        with self.assertRaises(IndexError):
            self.device._assert_valid_pin_number(-1)

    def test_assert_analog_pin(self):
        for pin_no in self.valid_pins:
            if pin_no in self.valid_analog_pins:
                self.device._assert_analog_pin(pin_no)
            else:
                with self.assertRaisesRegexp(PinError, 'pin {}'.format(pin_no)):
                    self.device._assert_analog_pin(pin_no)

    def test_assert_pwm_pin(self):
        for pin_no in self.valid_pins:
            if pin_no in self.valid_pwm_pins:
                self.device._assert_pwm_pin(pin_no)
            else:
                with self.assertRaisesRegexp(PinError, 'pin {}'.format(pin_no)):
                    self.device._assert_pwm_pin(pin_no)

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


class TestArduinoUno(unittest.TestCase, TestArduinoMixin):

    def setUp(self):
        self.device = ArduinoUno()
        self.valid_pins = range(20)
        self.valid_analog_pins = range(14, 20)
        self.valid_pwm_pins = [3, 5, 6, 9, 10, 11]

        self.setup_mixin()


class TestArduinoMega2560(unittest.TestCase, TestArduinoMixin):

    def setUp(self):
        self.device = ArduinoMega2560()
        self.valid_pins = range(70)
        self.valid_analog_pins = range(54, 70)
        self.valid_pwm_pins = list(range(2, 14)) + [44, 45, 46]

        self.setup_mixin()


if __name__ == '__main__':
    unittest.main()
