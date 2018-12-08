import abc
from collections import namedtuple

import six

from rapiduino.commands import CMD_POLL, CMD_PARROT, CMD_VERSION, CMD_PINMODE, CMD_DIGITALREAD, CMD_ANALOGREAD, \
    CMD_DIGITALWRITE, CMD_ANALOGWRITE
from rapiduino.exceptions import NotAnalogPinError, NotPwmPinError, ProtectedPinError, PinError
from rapiduino.pin import DevicePin
from rapiduino.communication import SerialConnection
from rapiduino.globals.common import GlobalParameter, INPUT, OUTPUT, INPUT_PULLUP, LOW, HIGH


def enable_pin_protection(func):
    def return_function(self, pin_no, *args, **kwargs):
        if not kwargs.get('force', False):
            self._assert_pin_not_protected(pin_no)
        return func(self, pin_no, *args)
    return return_function


PinMapping = namedtuple('PinMapping', ['device_pin_no', 'component_pin_no'])


@six.add_metaclass(abc.ABCMeta)
class ArduinoBase(object):

    def __init__(self, port=None):
        self.connection = SerialConnection.build(port)

    def poll(self):
        return self.connection.process_command(CMD_POLL)[0]

    def parrot(self, value):
        return self.connection.process_command(CMD_PARROT, value)[0]

    def version(self):
        return self.connection.process_command(CMD_VERSION)

    @enable_pin_protection
    def pin_mode(self, pin_no, mode):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self.connection.process_command(CMD_PINMODE, pin_no, mode.value)

    @enable_pin_protection
    def digital_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        state = self.connection.process_command(CMD_DIGITALREAD, pin_no)
        if state[0] == 1:
            return HIGH
        else:
            return LOW

    @enable_pin_protection
    def digital_write(self, pin_no, state):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_state(state)
        self.connection.process_command(CMD_DIGITALWRITE, pin_no, state.value)

    @enable_pin_protection
    def analog_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        self._assert_analog_pin(pin_no)
        return self.connection.process_command(CMD_ANALOGREAD, pin_no)[0]

    @enable_pin_protection
    def analog_write(self, pin_no, value):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_analog_write_range(value)
        self._assert_pwm_pin(pin_no)
        self.connection.process_command(CMD_ANALOGWRITE, pin_no, value)

    def bind_component(self, component, pin_mappings):
        try:
            for device_pin_no, component_pin_no in pin_mappings:
                device_pin = self.pins[device_pin_no]
                component_pin = component.pins[component_pin_no]
                self._assert_pins_compatible(device_pin, component_pin)
                device_pin.bind(component, component_pin_no)
                component_pin.bind(self, device_pin_no)
            component.bind_to_device(self)
        except PinError:
            self._undo_bind_component(component, pin_mappings)
            raise

    def unbind_component(self, component):
        for component_pin in component.pins:
            self.pins[component_pin.bound_pin_num].unbind()
            component_pin.unbind()
        component.unbind_to_device()

    def _undo_bind_component(self, component, pin_mappings):
        for device_pin_no, component_pin_no in pin_mappings:
            device_pin = self.pins[device_pin_no]
            component_pin = component.pins[component_pin_no]
            device_pin.unbind()
            component_pin.unbind()
        component.unbind_to_device()

    @staticmethod
    def _assert_pins_compatible(device_pin, component_pin):
        if component_pin.is_analog and not device_pin.is_analog:
            raise NotAnalogPinError('Component pin requires a Device pin with analog attribute')
        if component_pin.is_pwm and not device_pin.is_pwm:
            raise NotPwmPinError('Component pin requires a Device pin with pwm attribute')

    def _assert_valid_pin_number(self, pin_no):
        if (pin_no >= len(self.pins)) or (pin_no < 0):
            raise IndexError('Specified pin number {} is outside pin range of {}'.format(pin_no, len(self.pins)))

    def _assert_analog_pin(self, pin_no):
        if not self.pins[pin_no].is_analog:
            raise NotAnalogPinError('cannot complete operation as analog=False for pin {}'.format(pin_no))

    def _assert_pwm_pin(self, pin_no):
        if not self.pins[pin_no].is_pwm:
            raise NotPwmPinError('cannot complete operation as pwm=False for pin {}'.format(pin_no))

    def _assert_pin_not_protected(self, pin_no):
        if self.pins[pin_no].is_protected:
            raise ProtectedPinError('cannot complete operation as pin {} is protected'.format(pin_no))

    @staticmethod
    def _assert_valid_analog_write_range(value):
        if not isinstance(value, int):
            raise TypeError('Expected analog value type to be int, but found {}'.format(type(value)))
        if (value < 0) or (value > 255):
            raise ValueError('Specified analog value {} is outside valid range 0 to 255'.format(value))

    @staticmethod
    def _assert_valid_pin_mode(mode):
        if not isinstance(mode, GlobalParameter):
            raise TypeError('Expected GlobalParameter but received type {}'.format(type(mode)))
        if mode not in [INPUT, OUTPUT, INPUT_PULLUP]:
            raise ValueError(
                'pin_mode must be INPUT, OUTPUT or INPUT_PULLUP but {} was found'.format(mode.name)
            )

    @staticmethod
    def _assert_valid_pin_state(state):
        if not isinstance(state, GlobalParameter):
            raise TypeError('Expected GlobalParameter but received type {}'.format(type(state)))
        if state not in [HIGH, LOW]:
            raise ValueError(
                'pin_state must be HIGH or LOW but {} was found'.format(state.name)
            )

    @property
    def pins(self):
        return self._pins


class ArduinoUno(ArduinoBase):

    def __init__(self, *args, **kwargs):
        super(ArduinoUno, self).__init__(*args, **kwargs)
        self._pins = (
            DevicePin(0, protected=True),
            DevicePin(1, protected=True),
            DevicePin(2),
            DevicePin(3, pwm=True),
            DevicePin(4),
            DevicePin(5, pwm=True),
            DevicePin(6, pwm=True),
            DevicePin(7),
            DevicePin(8),
            DevicePin(9, pwm=True),
            DevicePin(10, pwm=True),
            DevicePin(11, pwm=True),
            DevicePin(12),
            DevicePin(13),
            DevicePin(14, analog=True),
            DevicePin(15, analog=True),
            DevicePin(16, analog=True),
            DevicePin(17, analog=True),
            DevicePin(18, analog=True),
            DevicePin(19, analog=True),
        )


class ArduinoMega2560(ArduinoBase):

    def __init__(self, *args, **kwargs):
        super(ArduinoMega2560, self).__init__(*args, **kwargs)
        self._pins = (
            DevicePin(0, protected=True),
            DevicePin(1, protected=True),
            DevicePin(2, pwm=True),
            DevicePin(3, pwm=True),
            DevicePin(4, pwm=True),
            DevicePin(5, pwm=True),
            DevicePin(6, pwm=True),
            DevicePin(7, pwm=True),
            DevicePin(8, pwm=True),
            DevicePin(9, pwm=True),
            DevicePin(10, pwm=True),
            DevicePin(11, pwm=True),
            DevicePin(12, pwm=True),
            DevicePin(13, pwm=True),
            DevicePin(14),
            DevicePin(15),
            DevicePin(16),
            DevicePin(17),
            DevicePin(18),
            DevicePin(19),
            DevicePin(20),
            DevicePin(21),
            DevicePin(22),
            DevicePin(23),
            DevicePin(24),
            DevicePin(25),
            DevicePin(26),
            DevicePin(27),
            DevicePin(28),
            DevicePin(29),
            DevicePin(30),
            DevicePin(31),
            DevicePin(32),
            DevicePin(33),
            DevicePin(34),
            DevicePin(35),
            DevicePin(36),
            DevicePin(37),
            DevicePin(38),
            DevicePin(39),
            DevicePin(40),
            DevicePin(41),
            DevicePin(42),
            DevicePin(43),
            DevicePin(44, pwm=True),
            DevicePin(45, pwm=True),
            DevicePin(46, pwm=True),
            DevicePin(47),
            DevicePin(48),
            DevicePin(49),
            DevicePin(50),
            DevicePin(51),
            DevicePin(52),
            DevicePin(53),
            DevicePin(54, analog=True),
            DevicePin(55, analog=True),
            DevicePin(56, analog=True),
            DevicePin(57, analog=True),
            DevicePin(58, analog=True),
            DevicePin(59, analog=True),
            DevicePin(60, analog=True),
            DevicePin(61, analog=True),
            DevicePin(62, analog=True),
            DevicePin(63, analog=True),
            DevicePin(64, analog=True),
            DevicePin(65, analog=True),
            DevicePin(66, analog=True),
            DevicePin(67, analog=True),
            DevicePin(68, analog=True),
            DevicePin(69, analog=True),
        )
