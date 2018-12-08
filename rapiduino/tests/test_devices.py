import unittest2
from mock import Mock, patch

from rapiduino.pin import ComponentPin, DevicePin
from rapiduino.communication import (SerialConnection)
from rapiduino.commands import *
from rapiduino.components.base import BaseComponent
from rapiduino.devices import ArduinoBase, ArduinoUno, ArduinoMega2560
from rapiduino.exceptions import PinError
from rapiduino.globals.common import *
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


class TestArduinoMixin(object):

    def setup_mixin(self):
        self.device = self.device_class()

        self.num_pins = len(self.valid_pins)
        self.out_of_range_pin = self.num_pins

        self.mocked_send = Mock()
        self.mocked_recv = Mock()

        self.device.connection._send = self.mocked_send
        self.device.connection._recv = self.mocked_recv

    def test_init(self):
        self.assertIsInstance(self.device._pins, tuple)
        self.assertIsInstance(self.device.connection, SerialConnection)

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

    def test_poll(self):
        self.mocked_recv.return_value = (1,)
        value = self.device.poll()
        self.mocked_send.assert_called_once_with(CMD_POLL, ())
        self.assertEqual(value, 1)

    def test_parrot(self):
        self.mocked_recv.return_value = (5,)
        value = self.device.parrot(5)

        self.mocked_send.assert_called_once_with(CMD_PARROT, (5,))
        self.assertEqual(value, 5)

    def test_version(self):
        self.mocked_recv.return_value = (1, 2, 3)
        version = self.device.version()
        self.mocked_send.assert_called_once_with(CMD_VERSION, ())
        self.assertEqual(version, (1, 2, 3))

    def test_pin_mode(self):
        self.device.pin_mode(self.valid_digital_pin, OUTPUT)
        self.mocked_send.assert_called_once_with(CMD_PINMODE, (self.valid_digital_pin, OUTPUT.value))

    def test_pin_mode_on_protected_pin(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        with self.assertRaisesRegex(PinError, 'protected'):
            self.device.pin_mode(self.valid_digital_pin, INPUT)

    def test_pin_mode_on_protected_pin_with_force(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        self.device.pin_mode(self.valid_digital_pin, OUTPUT, force=True)
        self.mocked_send.assert_called_once_with(CMD_PINMODE, (self.valid_digital_pin, OUTPUT.value))

    def test_pin_mode_with_incorrect_mode(self):
        with self.assertRaises(ValueError):
            self.device.pin_mode(self.valid_digital_pin, HIGH)

    def test_pin_mode_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.pin_mode(self.out_of_range_pin, OUTPUT)

    def test_digital_read(self):
        self.mocked_recv.return_value = (1,)
        state = self.device.digital_read(self.valid_digital_pin)

        self.mocked_send.assert_called_once_with(CMD_DIGITALREAD, (self.valid_digital_pin,))
        self.assertEqual(state, HIGH)

    def test_digital_read_on_protected_pin(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        with self.assertRaisesRegex(PinError, 'protected'):
            self.device.digital_read(self.valid_digital_pin)

    def test_digital_read_on_protected_pin_with_force(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        self.mocked_recv.return_value = (1,)
        state = self.device.digital_read(self.valid_digital_pin, force=True)
        self.mocked_send.assert_called_once_with(CMD_DIGITALREAD, (self.valid_digital_pin,))
        self.assertEqual(state, HIGH)

    def test_digital_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_read(self.out_of_range_pin)

    def test_digital_write(self):
        self.device.digital_write(self.valid_digital_pin, HIGH)
        self.mocked_send.assert_called_once_with(CMD_DIGITALWRITE, (self.valid_digital_pin, HIGH.value))

    def test_digital_write_on_protected_pin(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        with self.assertRaisesRegex(PinError, 'protected'):
            self.device.digital_write(self.valid_digital_pin, HIGH)

    def test_digital_write_on_protected_pin_with_force(self):
        self.device.pins[self.valid_digital_pin]._protected = True
        self.device.digital_write(self.valid_digital_pin, HIGH, force=True)
        self.mocked_send.assert_called_once_with(CMD_DIGITALWRITE, (self.valid_digital_pin, HIGH.value))

    def test_digital_write_with_incorrect_state(self):
        with self.assertRaises(ValueError):
            self.device.digital_write(self.valid_digital_pin, OUTPUT)

    def test_digital_write_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.digital_write(self.out_of_range_pin, HIGH)

    def test_analog_read(self):
        self.mocked_recv.return_value = (100,)
        value = self.device.analog_read(self.valid_analog_pin)

        self.mocked_send.assert_called_once_with(CMD_ANALOGREAD, (self.valid_analog_pin,))
        self.assertEqual(value, 100)

    def test_analog_read_on_protected_pin(self):
        self.device.pins[self.valid_analog_pin]._protected = True
        with self.assertRaisesRegex(PinError, 'protected'):
            self.device.analog_read(self.valid_analog_pin)

    def test_analog_read_on_protected_pin_with_force(self):
        self.device.pins[self.valid_analog_pin]._protected = True
        self.mocked_recv.return_value = (100,)
        value = self.device.analog_read(self.valid_analog_pin, force=True)
        self.mocked_send.assert_called_once_with(CMD_ANALOGREAD, (self.valid_analog_pin,))
        self.assertEqual(value, 100)

    def test_analog_read_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.analog_read(self.out_of_range_pin)

    def test_analog_read_on_non_analog_pin_raises_error(self):
        with self.assertRaisesRegex(PinError, 'cannot complete operation as analog=False for pin {}'.format(self.invalid_analog_pin)):
            self.device.analog_read(self.invalid_analog_pin)

    def test_analog_write(self):
        self.device.analog_write(self.valid_pwm_pin, 100)
        self.mocked_send.assert_called_once_with(CMD_ANALOGWRITE, (self.valid_pwm_pin, 100))

    def test_analog_write_on_protected_pin(self):
        self.device.pins[self.valid_pwm_pin]._protected = True
        with self.assertRaisesRegex(PinError, 'protected'):
            self.device.analog_write(self.valid_pwm_pin, 100)

    def test_analog_write_on_protected_pin_with_force(self):
        self.device.pins[self.valid_pwm_pin]._protected = True
        self.device.analog_write(self.valid_pwm_pin, 100, force=True)
        self.mocked_send.assert_called_once_with(CMD_ANALOGWRITE, (self.valid_pwm_pin, 100))

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
        with self.assertRaisesRegex(PinError, 'cannot complete operation as pwm=False for pin {}'.format(self.invalid_pwm_pin)):
            self.device.analog_write(self.invalid_pwm_pin, self.invalid_pwm_pin)

    def test_bind_component(self):
        component = ExampleTestComponent()
        component.setup = Mock()
        pin_mappings = ((self.valid_digital_pin, 0), (self.valid_pwm_pin, 1), (self.valid_analog_pin, 2))
        self.device.bind_component(component, pin_mappings)
        self.assertIsInstance(component.bound_device, self.device_class)
        for device_pin_no, component_pin_no in pin_mappings:
            self.assertTupleEqual(self.device.pins[device_pin_no].bound_to, (component, component_pin_no))
            self.assertTupleEqual(component.pins[component_pin_no].bound_to, (self.device, device_pin_no))
            self.assertTrue(self.device.pins[device_pin_no].is_protected)
        component.setup.assert_called_once()

    def test_bind_component_with_incompatible_pins(self):
        component = ExampleTestComponent()
        component.setup = Mock()
        pin_mappings = ((self.valid_digital_pin, 0), (self.invalid_pwm_pin, 1), (self.valid_analog_pin, 2))
        with self.assertRaisesRegex(PinError, 'pin with pwm attribute'):
            self.device.bind_component(component, pin_mappings)
        self.assertIsNone(component.bound_device)
        for device_pin_no, component_pin_no in pin_mappings:
            self.assertIsNone(self.device.pins[device_pin_no].bound_to)
            self.assertIsNone(component.pins[component_pin_no].bound_to)
        component.setup.assert_not_called()

    def test_bind_component_with_duplicate_pin_in_mapping(self):
        component = ExampleTestComponent()
        component.setup = Mock()
        pin_mappings = ((self.valid_pwm_pin, 0), (self.valid_pwm_pin, 1), (self.valid_analog_pin, 2))
        with self.assertRaises(PinError):
            self.device.bind_component(component, pin_mappings)
        self.assertIsNone(component.bound_device)
        for device_pin_no, component_pin_no in pin_mappings:
            self.assertIsNone(self.device.pins[device_pin_no].bound_to)
            self.assertIsNone(component.pins[component_pin_no].bound_to)
        component.setup.assert_not_called()

    def test_undo_bind_component(self):
        component = ExampleTestComponent()
        component.setup = Mock()
        pin_mappings = ((self.valid_digital_pin, 0), (self.valid_pwm_pin, 1), (self.valid_analog_pin, 2))
        self.device.bind_component(component, pin_mappings)
        self.device._undo_bind_component(component, pin_mappings)

        self.assertIsNone(component.bound_device)
        for device_pin_no, component_pin_no in pin_mappings:
            self.assertIsNone(self.device.pins[device_pin_no].bound_to)
            self.assertIsNone(component.pins[component_pin_no].bound_to)
            self.assertFalse(self.device.pins[device_pin_no].is_protected)

    def test_unbind_component(self):
        component = ExampleTestComponent()
        component.setup = Mock()
        pin_mappings = ((self.valid_digital_pin, 0), (self.valid_pwm_pin, 1), (self.valid_analog_pin, 2))
        self.device.bind_component(component, pin_mappings)
        self.device.unbind_component(component)

        self.assertIsNone(component.bound_device)
        for device_pin_no, component_pin_no in pin_mappings:
            self.assertIsNone(self.device.pins[device_pin_no].bound_to)
            self.assertIsNone(component.pins[component_pin_no].bound_to)
            self.assertFalse(self.device.pins[device_pin_no].is_protected)

    def test_assert_pins_compatible(self):
        self.device._assert_pins_compatible(DevicePin(0), ComponentPin(1))
        self.device._assert_pins_compatible(DevicePin(0, analog=True), ComponentPin(1, analog=True))
        self.device._assert_pins_compatible(DevicePin(0, pwm=True), ComponentPin(1, pwm=True))
        self.device._assert_pins_compatible(DevicePin(0, pwm=True), ComponentPin(1))
        self.device._assert_pins_compatible(DevicePin(0, analog=True), ComponentPin(1))

    def test_assert_pins_incompatible(self):
        with self.assertRaises(PinError):
            self.device._assert_pins_compatible(DevicePin(0), ComponentPin(1, analog=True))
        with self.assertRaises(PinError):
            self.device._assert_pins_compatible(DevicePin(0, pwm=True), ComponentPin(1, analog=True))
        with self.assertRaises(PinError):
            self.device._assert_pins_compatible(DevicePin(0), ComponentPin(1, pwm=True))
        with self.assertRaises(PinError):
            self.device._assert_pins_compatible(DevicePin(0, analog=True), ComponentPin(1, pwm=True))

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
                with self.assertRaisesRegex(PinError, 'pin {}'.format(pin_no)):
                    self.device._assert_analog_pin(pin_no)

    def test_assert_pwm_pin(self):
        for pin_no in self.valid_pins:
            if pin_no in self.valid_pwm_pins:
                self.device._assert_pwm_pin(pin_no)
            else:
                with self.assertRaisesRegex(PinError, 'pin {}'.format(pin_no)):
                    self.device._assert_pwm_pin(pin_no)

    def test_assert_tx_rx_pins_protected(self):
        for pin_no in self.valid_pins:
            if pin_no in [self.tx_pin, self.rx_pin]:
                with self.assertRaisesRegex(PinError, 'pin {}'.format(pin_no)):
                    self.device._assert_pin_not_protected(pin_no)
            else:
                self.device._assert_pin_not_protected(pin_no)

    def test_assert_analog_write_range(self):
        for integer in range(256):
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

    def test_analog_alias_globals(self):
        for analog_alias, pin_num in enumerate(self.valid_analog_pins):
            self.assertEqual(getattr(self.analog_alias, 'A{}'.format(analog_alias)), pin_num)


class TestArduinoUno(unittest2.TestCase, TestArduinoMixin):

    def setUp(self):
        self.device_class = ArduinoUno
        self.analog_alias = arduino_uno_globals
        self.valid_pins = list(range(20))
        self.valid_analog_pins = list(range(14, 20))
        self.valid_pwm_pins = [3, 5, 6, 9, 10, 11]
        self.tx_pin = 0
        self.rx_pin = 1
        self.valid_digital_pin = 2
        self.valid_analog_pin = 14
        self.valid_pwm_pin = 3
        self.invalid_analog_pin = 8
        self.invalid_pwm_pin = 7

        self.setup_mixin()


class TestArduinoMega2560(unittest2.TestCase, TestArduinoMixin):

    def setUp(self):
        self.device_class = ArduinoMega2560
        self.analog_alias = arduino_mega_2560_globals
        self.valid_pins = list(range(70))
        self.valid_analog_pins = list(range(54, 70))
        self.valid_pwm_pins = list(range(2, 14)) + [44, 45, 46]
        self.tx_pin = 0
        self.rx_pin = 1
        self.valid_digital_pin = 2
        self.valid_analog_pin = 54
        self.valid_pwm_pin = 3
        self.invalid_analog_pin = 4
        self.invalid_pwm_pin = 22

        self.setup_mixin()


if __name__ == '__main__':
    unittest2.main()
