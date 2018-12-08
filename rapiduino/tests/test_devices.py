import abc
import six
import unittest2
from mock import Mock, call

from rapiduino.commands import (CMD_POLL, CMD_PARROT, CMD_VERSION, CMD_PINMODE, CMD_DIGITALREAD, CMD_DIGITALWRITE,
                                CMD_ANALOGREAD, CMD_ANALOGWRITE)
from rapiduino.globals.common import INPUT, OUTPUT, HIGH
from rapiduino.pin import ComponentPin
from rapiduino.communication import (SerialConnection)
from rapiduino.components.base import BaseComponent
from rapiduino.devices import ArduinoBase, ArduinoUno, ArduinoMega2560, PinMapping
from rapiduino.exceptions import NotPwmPinError, NotAnalogPinError, ProtectedPinError, AlreadyBoundPinError
import rapiduino.globals.arduino_uno as arduino_uno_globals
import rapiduino.globals.arduino_mega_2560 as arduino_mega_2560_globals


class ExampleTestComponent(BaseComponent):

    def __init__(self):
        super(ExampleTestComponent, self).__init__()
        self._pins = (
            ComponentPin(0),
            ComponentPin(1, pwm=True),
            ComponentPin(2, analog=True),
        )


class ArduinoCommon(object):

    @six.add_metaclass(abc.ABCMeta)
    class TestCase(unittest2.TestCase):

        def setUp(self):
            self.device = self.device_class()

            self.num_pins = len(self.valid_pins)
            self.out_of_range_pin = self.num_pins

            self.mocked_send = Mock()
            self.mocked_recv = Mock()

            self.device.connection._send = self.mocked_send
            self.device.connection._recv = self.mocked_recv

            self.component = ExampleTestComponent()
            self.component._setup = Mock()

        @abc.abstractproperty
        def device_class(self):
            pass

        @abc.abstractproperty
        def analog_alias(self):
            pass

        @abc.abstractproperty
        def valid_pins(self):
            pass

        @abc.abstractproperty
        def valid_analog_pins(self):
            pass

        @abc.abstractproperty
        def valid_pwm_pins(self):
            pass

        @abc.abstractproperty
        def tx_pin(self):
            pass

        @abc.abstractproperty
        def rx_pin(self):
            pass

        @abc.abstractproperty
        def valid_digital_pin(self):
            pass

        @abc.abstractproperty
        def valid_analog_pin(self):
            pass

        @abc.abstractproperty
        def valid_pwm_pin(self):
            pass

        @abc.abstractproperty
        def invalid_analog_pin(self):
            pass

        @abc.abstractproperty
        def invalid_pwm_pin(self):
            pass

        def test_class_builds_serial_connection(self):
            self.assertIsInstance(self.device_class().connection, SerialConnection)

        def test_class_has_required_pins_attribute(self):
            self.assertIsInstance(self.device._pins, tuple)

        def test_class_implements_base_abstract_class(self):
            self.assertTrue(isinstance(self.device, ArduinoBase))

        def test_device_has_correct_number_of_pins(self):
            self.assertEqual(len(self.device.pins), self.num_pins)

        def test_pin_ids_are_sequential(self):
            for pin_no, pin in enumerate(self.device.pins):
                self.assertEqual(pin_no, pin.id)

        def test_pins_are_private_and_cannot_be_modified(self):
            with self.assertRaises(AttributeError):
                self.device.pins = []
            self.assertIsInstance(self.device.pins, tuple)

        def test_poll_sends_correct_message(self):
            self.mocked_recv.return_value = (1,)
            value = self.device.poll()
            self.assertEqual(self.mocked_send.call_args, call(CMD_POLL, ()))
            self.assertEqual(value, 1)

        def test_parrot(self):
            self.mocked_recv.return_value = (5,)
            value = self.device.parrot(5)
            self.assertEqual(self.mocked_send.call_args, call(CMD_PARROT, (5,)))
            self.assertEqual(value, 5)

        def test_version(self):
            self.mocked_recv.return_value = (1, 2, 3)
            version = self.device.version()
            self.assertEqual(self.mocked_send.call_args, call(CMD_VERSION, ()))
            self.assertEqual(version, (1, 2, 3))

        def test_pin_mode_with_valid_args(self):
            from rapiduino.globals.common import OUTPUT
            self.device.pin_mode(self.valid_digital_pin, OUTPUT)
            self.assertEqual(self.mocked_send.call_args, call(CMD_PINMODE, (self.valid_digital_pin, OUTPUT.value)))

        def test_pin_mode_on_protected_pin_raises_error(self):
            with self.assertRaises(ProtectedPinError):
                self.device.pin_mode(self.tx_pin, INPUT)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_pin_mode_on_protected_pin_with_force_is_successful(self):
            self.device.pin_mode(self.tx_pin, OUTPUT, force=True)
            self.assertEqual(self.mocked_send.call_args, call(CMD_PINMODE, (self.tx_pin, OUTPUT.value)))

        def test_pin_mode_with_incorrect_mode(self):
            with self.assertRaises(ValueError):
                self.device.pin_mode(self.valid_digital_pin, HIGH)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_pin_mode_with_pin_no_out_of_range(self):
            with self.assertRaises(IndexError):
                self.device.pin_mode(self.out_of_range_pin, OUTPUT)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_digital_read_with_valid_args(self):
            self.mocked_recv.return_value = (1,)
            state = self.device.digital_read(self.valid_digital_pin)
            self.assertEqual(self.mocked_send.call_args, call(CMD_DIGITALREAD, (self.valid_digital_pin,)))
            self.assertEqual(state, HIGH)

        def test_digital_read_on_protected_pin(self):
            with self.assertRaises(ProtectedPinError):
                self.device.digital_read(self.tx_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_digital_read_on_protected_pin_with_force(self):
            self.mocked_recv.return_value = (1,)
            state = self.device.digital_read(self.tx_pin, force=True)
            self.assertEqual(self.mocked_send.call_args, call(CMD_DIGITALREAD, (self.tx_pin,)))
            self.assertEqual(state, HIGH)

        def test_digital_read_with_pin_no_out_of_range(self):
            with self.assertRaises(IndexError):
                self.device.digital_read(self.out_of_range_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_digital_write_with_valid_args(self):
            self.device.digital_write(self.valid_digital_pin, HIGH)
            self.assertEqual(self.mocked_send.call_args, call(CMD_DIGITALWRITE, (self.valid_digital_pin, HIGH.value)))

        def test_digital_write_on_protected_pin(self):
            with self.assertRaises(ProtectedPinError):
                self.device.digital_write(self.tx_pin, HIGH)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_digital_write_on_protected_pin_with_force(self):
            self.device.pins[self.valid_digital_pin]._protected = True
            self.device.digital_write(self.valid_digital_pin, HIGH, force=True)
            self.assertEqual(self.mocked_send.call_args, call(CMD_DIGITALWRITE, (self.valid_digital_pin, HIGH.value)))

        def test_digital_write_with_incorrect_state(self):
            with self.assertRaises(ValueError):
                self.device.digital_write(self.valid_digital_pin, OUTPUT)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_digital_write_with_pin_no_out_of_range(self):
            with self.assertRaises(IndexError):
                self.device.digital_write(self.out_of_range_pin, HIGH)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_read_with_valid_args(self):
            self.mocked_recv.return_value = (100,)
            value = self.device.analog_read(self.valid_analog_pin)
            self.assertEqual(self.mocked_send.call_args, call(CMD_ANALOGREAD, (self.valid_analog_pin,)))
            self.assertEqual(value, 100)

        def test_analog_read_on_protected_pin(self):
            with self.assertRaises(ProtectedPinError):
                self.device.analog_read(self.tx_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_read_on_protected_pin_with_force(self):
            self.device.pins[self.valid_analog_pin]._protected = True
            self.mocked_recv.return_value = (100,)
            value = self.device.analog_read(self.valid_analog_pin, force=True)
            self.assertEqual(self.mocked_send.call_args, call(CMD_ANALOGREAD, (self.valid_analog_pin,)))
            self.assertEqual(value, 100)

        def test_analog_read_with_pin_no_out_of_range(self):
            with self.assertRaises(IndexError):
                self.device.analog_read(self.out_of_range_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_read_on_non_analog_pin_raises_error(self):
            with six.assertRaisesRegex(self, NotAnalogPinError, 'pin {}'.format(self.invalid_analog_pin)):
                self.device.analog_read(self.invalid_analog_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_with_valid_args(self):
            self.device.analog_write(self.valid_pwm_pin, 100)
            self.assertEqual(self.mocked_send.call_args, call(CMD_ANALOGWRITE, (self.valid_pwm_pin, 100)))

        def test_analog_write_on_protected_pin(self):
            with self.assertRaises(ProtectedPinError):
                self.device.analog_write(self.tx_pin, 100)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_on_protected_pin_with_force(self):
            self.device.pins[self.valid_pwm_pin]._protected = True
            self.device.analog_write(self.valid_pwm_pin, 100, force=True)
            self.assertEqual(self.mocked_send.call_args, call(CMD_ANALOGWRITE, (self.valid_pwm_pin, 100)))

        def test_analog_write_with_value_too_high(self):
            with self.assertRaises(ValueError):
                self.device.analog_write(self.valid_pwm_pin, 256)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_with_negative_value(self):
            with self.assertRaises(ValueError):
                self.device.analog_write(self.valid_pwm_pin, -1)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_with_non_integer_value(self):
            with self.assertRaises(TypeError):
                self.device.analog_write(self.valid_pwm_pin, 10.1)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_with_pin_no_out_of_range(self):
            with self.assertRaises(IndexError):
                self.device.analog_write(self.out_of_range_pin, self.out_of_range_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_analog_write_on_non_pwm_pin_raises_error(self):
            with six.assertRaisesRegex(self, NotPwmPinError, 'pin {}'.format(self.invalid_pwm_pin)):
                self.device.analog_write(self.invalid_pwm_pin, self.invalid_pwm_pin)
            self.assertEqual(self.mocked_send.call_count, 0)

        def test_bind_component_with_valid_args(self):
            pin_mappings = (
                PinMapping(device_pin_no=self.valid_digital_pin, component_pin_no=0),
                PinMapping(device_pin_no=self.valid_pwm_pin, component_pin_no=1),
                PinMapping(device_pin_no=self.valid_analog_pin, component_pin_no=2)
            )
            self.device.bind_component(self.component, pin_mappings)
            self.assertIsInstance(self.component.bound_device, self.device_class)
            for device_pin_no, component_pin_no in pin_mappings:
                self.assertTupleEqual(self.device.pins[device_pin_no].bound_to, (self.component, component_pin_no))
                self.assertTupleEqual(self.component.pins[component_pin_no].bound_to, (self.device, device_pin_no))
                self.assertTrue(self.device.pins[device_pin_no].is_protected)
                self.assertEqual(self.component._setup.call_count, 1)

        def test_bind_component_with_incompatible_pins(self):
            pin_mappings = (
                PinMapping(device_pin_no=self.valid_digital_pin, component_pin_no=0),
                PinMapping(device_pin_no=self.invalid_pwm_pin, component_pin_no=1),
                PinMapping(device_pin_no=self.valid_analog_pin, component_pin_no=2)
            )
            with self.assertRaises(NotPwmPinError):
                self.device.bind_component(self.component, pin_mappings)
            self.assertIsNone(self.component.bound_device)
            for device_pin_no, component_pin_no in pin_mappings:
                self.assertIsNone(self.device.pins[device_pin_no].bound_to)
                self.assertIsNone(self.component.pins[component_pin_no].bound_to)
                self.assertEqual(self.component._setup.call_count, 0)

        def test_bind_component_with_duplicate_pin_in_mapping(self):
            pin_mappings = (
                PinMapping(device_pin_no=self.valid_pwm_pin, component_pin_no=0),
                PinMapping(device_pin_no=self.valid_pwm_pin, component_pin_no=1),
                PinMapping(device_pin_no=self.valid_analog_pin, component_pin_no=2)
            )
            with self.assertRaises(AlreadyBoundPinError):
                self.device.bind_component(self.component, pin_mappings)
            self.assertIsNone(self.component.bound_device)
            for device_pin_no, component_pin_no in pin_mappings:
                self.assertIsNone(self.device.pins[device_pin_no].bound_to)
                self.assertIsNone(self.component.pins[component_pin_no].bound_to)
                self.assertEqual(self.component._setup.call_count, 0)

        def test_bind_component_does_not_bind_pins_if_error(self):
            pin_mappings = (
                PinMapping(device_pin_no=self.valid_digital_pin, component_pin_no=0),
                PinMapping(device_pin_no=self.invalid_pwm_pin, component_pin_no=1),
                PinMapping(device_pin_no=self.valid_analog_pin, component_pin_no=2)
            )
            with self.assertRaises(NotPwmPinError):
                self.device.bind_component(self.component, pin_mappings)

            self.assertIsNone(self.component.bound_device)
            for device_pin_no, component_pin_no in pin_mappings:
                self.assertIsNone(self.device.pins[device_pin_no].bound_to)
                self.assertIsNone(self.component.pins[component_pin_no].bound_to)
                self.assertFalse(self.device.pins[device_pin_no].is_protected)

        def test_unbind_component(self):
            pin_mappings = (
                PinMapping(device_pin_no=self.valid_digital_pin, component_pin_no=0),
                PinMapping(device_pin_no=self.valid_pwm_pin, component_pin_no=1),
                PinMapping(device_pin_no=self.valid_analog_pin, component_pin_no=2)
            )
            self.device.bind_component(self.component, pin_mappings)
            self.device.unbind_component(self.component)

            self.assertIsNone(self.component.bound_device)
            for device_pin_no, component_pin_no in pin_mappings:
                self.assertIsNone(self.device.pins[device_pin_no].bound_to)
                self.assertIsNone(self.component.pins[component_pin_no].bound_to)
                self.assertFalse(self.device.pins[device_pin_no].is_protected)

        def test_analog_alias_globals(self):
            for analog_alias, pin_num in enumerate(self.valid_analog_pins):
                self.assertEqual(getattr(self.analog_alias, 'A{}'.format(analog_alias)), pin_num)


class TestArduinoUno(ArduinoCommon.TestCase):

    @property
    def device_class(self):
        return ArduinoUno

    @property
    def analog_alias(self):
        return arduino_uno_globals

    @property
    def valid_pins(self):
        return list(range(20))

    @property
    def valid_analog_pins(self):
        return list(range(14, 20))

    @property
    def valid_pwm_pins(self):
        return [3, 5, 6, 9, 10, 11]

    @property
    def tx_pin(self):
        return 0

    @property
    def rx_pin(self):
        return 1

    @property
    def valid_digital_pin(self):
        return 2

    @property
    def valid_analog_pin(self):
        return 14

    @property
    def valid_pwm_pin(self):
        return 3

    @property
    def invalid_analog_pin(self):
        return 8

    @property
    def invalid_pwm_pin(self):
        return 7


class TestArduinoMega2560(ArduinoCommon.TestCase):

    @property
    def device_class(self):
        return ArduinoMega2560

    @property
    def analog_alias(self):
        return arduino_mega_2560_globals

    @property
    def valid_pins(self):
        return list(range(70))

    @property
    def valid_analog_pins(self):
        return list(range(54, 70))

    @property
    def valid_pwm_pins(self):
        return list(range(2, 14)) + [44, 45, 46]

    @property
    def tx_pin(self):
        return 0

    @property
    def rx_pin(self):
        return 1

    @property
    def valid_digital_pin(self):
        return 2

    @property
    def valid_analog_pin(self):
        return 54

    @property
    def valid_pwm_pin(self):
        return 3

    @property
    def invalid_analog_pin(self):
        return 4

    @property
    def invalid_pwm_pin(self):
        return 22
