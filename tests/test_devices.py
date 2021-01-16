import unittest
from typing import List
from unittest.mock import Mock, call

import rapiduino.globals.arduino_uno as arduino_uno_globals
from rapiduino.commands import (
    CMD_ANALOGREAD,
    CMD_ANALOGWRITE,
    CMD_DIGITALREAD,
    CMD_DIGITALWRITE,
    CMD_PARROT,
    CMD_PINMODE,
    CMD_POLL,
    CMD_VERSION,
)
from rapiduino.communication import SerialConnection
from rapiduino.devices import Arduino
from rapiduino.exceptions import NotAnalogPinError, NotPwmPinError
from rapiduino.globals.common import HIGH, OUTPUT


class ArduinoUnoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.device = Arduino.uno()

        self.mocked_send = Mock()
        self.mocked_recv = Mock()

        self.device.connection._send = self.mocked_send  # type: ignore
        self.device.connection._recv = self.mocked_recv  # type: ignore

        self.num_pins = len(self.valid_pins)
        self.out_of_range_pin = self.num_pins

    @property
    def valid_pins(self) -> List[int]:
        return list(range(20))

    @property
    def valid_analog_pins(self) -> List[int]:
        return list(range(14, 20))

    @property
    def valid_pwm_pins(self) -> List[int]:
        return [3, 5, 6, 9, 10, 11]

    @property
    def tx_pin(self) -> int:
        return 0

    @property
    def rx_pin(self) -> int:
        return 1

    @property
    def valid_digital_pin(self) -> int:
        return 2

    @property
    def valid_analog_pin(self) -> int:
        return 14

    @property
    def valid_pwm_pin(self) -> int:
        return 3

    @property
    def invalid_analog_pin(self) -> int:
        return 8

    @property
    def invalid_pwm_pin(self) -> int:
        return 7

    def test_class_builds_serial_connection(self) -> None:
        self.assertIsInstance(self.device.connection, SerialConnection)

    def test_class_has_required_pins_attribute(self) -> None:
        self.assertIsInstance(self.device._pins, tuple)

    def test_class_implements_base_abstract_class(self) -> None:
        self.assertTrue(isinstance(self.device, Arduino))

    def test_device_has_correct_number_of_pins(self) -> None:
        self.assertEqual(len(self.device.pins), self.num_pins)

    def test_pin_ids_are_sequential(self) -> None:
        for pin_no, pin in enumerate(self.device.pins):
            self.assertEqual(pin_no, pin.pin_id)

    def test_poll_sends_correct_message(self) -> None:
        self.mocked_recv.return_value = (1,)
        value = self.device.poll()
        self.assertEqual(self.mocked_send.call_args, call(CMD_POLL, ()))
        self.assertEqual(value, 1)

    def test_parrot(self) -> None:
        self.mocked_recv.return_value = (5,)
        value = self.device.parrot(5)
        self.assertEqual(self.mocked_send.call_args, call(CMD_PARROT, (5,)))
        self.assertEqual(value, 5)

    def test_version(self) -> None:
        self.mocked_recv.return_value = (1, 2, 3)
        version = self.device.version()
        self.assertEqual(self.mocked_send.call_args, call(CMD_VERSION, ()))
        self.assertEqual(version, (1, 2, 3))

    def test_pin_mode_with_valid_args(self) -> None:
        self.device.pin_mode(self.valid_digital_pin, OUTPUT)
        self.assertEqual(
            self.mocked_send.call_args,
            call(CMD_PINMODE, (self.valid_digital_pin, OUTPUT.value)),
        )

    def test_pin_mode_with_incorrect_mode(self) -> None:
        with self.assertRaises(ValueError):
            self.device.pin_mode(self.valid_digital_pin, HIGH)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_pin_mode_with_pin_no_out_of_range(self) -> None:
        with self.assertRaises(IndexError):
            self.device.pin_mode(self.out_of_range_pin, OUTPUT)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_digital_read_with_valid_args(self) -> None:
        self.mocked_recv.return_value = (1,)
        state = self.device.digital_read(self.valid_digital_pin)
        self.assertEqual(
            self.mocked_send.call_args, call(CMD_DIGITALREAD, (self.valid_digital_pin,))
        )
        self.assertEqual(state, HIGH)

    def test_digital_read_with_pin_no_out_of_range(self) -> None:
        with self.assertRaises(IndexError):
            self.device.digital_read(self.out_of_range_pin)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_digital_write_with_valid_args(self) -> None:
        self.device.digital_write(self.valid_digital_pin, HIGH)
        self.assertEqual(
            self.mocked_send.call_args,
            call(CMD_DIGITALWRITE, (self.valid_digital_pin, HIGH.value)),
        )

    def test_digital_write_with_incorrect_state(self) -> None:
        with self.assertRaises(ValueError):
            self.device.digital_write(self.valid_digital_pin, OUTPUT)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_digital_write_with_pin_no_out_of_range(self) -> None:
        with self.assertRaises(IndexError):
            self.device.digital_write(self.out_of_range_pin, HIGH)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_read_with_valid_args(self) -> None:
        self.mocked_recv.return_value = (100,)
        value = self.device.analog_read(self.valid_analog_pin)
        self.assertEqual(
            self.mocked_send.call_args, call(CMD_ANALOGREAD, (self.valid_analog_pin,))
        )
        self.assertEqual(value, 100)

    def test_analog_read_with_pin_no_out_of_range(self) -> None:
        with self.assertRaises(IndexError):
            self.device.analog_read(self.out_of_range_pin)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_read_on_non_analog_pin_raises_error(self) -> None:
        with self.assertRaisesRegex(
            NotAnalogPinError, f"pin {self.invalid_analog_pin}"
        ):
            self.device.analog_read(self.invalid_analog_pin)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_write_with_valid_args(self) -> None:
        self.device.analog_write(self.valid_pwm_pin, 100)
        self.assertEqual(
            self.mocked_send.call_args, call(CMD_ANALOGWRITE, (self.valid_pwm_pin, 100))
        )

    def test_analog_write_with_value_too_high(self) -> None:
        with self.assertRaises(ValueError):
            self.device.analog_write(self.valid_pwm_pin, 256)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_write_with_negative_value(self) -> None:
        with self.assertRaises(ValueError):
            self.device.analog_write(self.valid_pwm_pin, -1)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_write_with_pin_no_out_of_range(self) -> None:
        with self.assertRaises(IndexError):
            self.device.analog_write(self.out_of_range_pin, self.out_of_range_pin)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_write_on_non_pwm_pin_raises_error(self) -> None:
        with self.assertRaisesRegex(NotPwmPinError, f"pin {self.invalid_pwm_pin}"):
            self.device.analog_write(self.invalid_pwm_pin, self.invalid_pwm_pin)
        self.assertEqual(self.mocked_send.call_count, 0)

    def test_analog_alias_globals(self) -> None:
        for analog_alias, pin_num in enumerate(self.valid_analog_pins):
            self.assertEqual(getattr(arduino_uno_globals, f"A{analog_alias}"), pin_num)
