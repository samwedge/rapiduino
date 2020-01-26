from collections import namedtuple

from rapiduino.commands import CMD_POLL, CMD_PARROT, CMD_VERSION, CMD_PINMODE, CMD_DIGITALREAD, CMD_ANALOGREAD, \
    CMD_DIGITALWRITE, CMD_ANALOGWRITE
from rapiduino.exceptions import NotAnalogPinError, NotPwmPinError, ProtectedPinError, PinError, UnknownBoardError
from rapiduino.pin import Pin
from rapiduino.communication import SerialConnection
from rapiduino.globals.common import GlobalParameter, INPUT, OUTPUT, INPUT_PULLUP, LOW, HIGH


def enable_pin_protection(func):
    def return_function(self, pin_no, *args, **kwargs):
        if not kwargs.get('force', False):
            self._assert_pin_not_protected(pin_no)
        return func(self, pin_no, *args)
    return return_function


PinMapping = namedtuple('PinMapping', ['device_pin_no', 'component_pin_no'])

UNO = 'UNO'
MEGA2560 = 'MEGA2560'


def _get_uno_pins():
    return (
        Pin(0, protected=True),
        Pin(1, protected=True),
        Pin(2),
        Pin(3, pwm=True),
        Pin(4),
        Pin(5, pwm=True),
        Pin(6, pwm=True),
        Pin(7),
        Pin(8),
        Pin(9, pwm=True),
        Pin(10, pwm=True),
        Pin(11, pwm=True),
        Pin(12),
        Pin(13),
        Pin(14, analog=True),
        Pin(15, analog=True),
        Pin(16, analog=True),
        Pin(17, analog=True),
        Pin(18, analog=True),
        Pin(19, analog=True),
    )


def _get_mega2560_pins():
    return (
        Pin(0, protected=True),
        Pin(1, protected=True),
        Pin(2, pwm=True),
        Pin(3, pwm=True),
        Pin(4, pwm=True),
        Pin(5, pwm=True),
        Pin(6, pwm=True),
        Pin(7, pwm=True),
        Pin(8, pwm=True),
        Pin(9, pwm=True),
        Pin(10, pwm=True),
        Pin(11, pwm=True),
        Pin(12, pwm=True),
        Pin(13, pwm=True),
        Pin(14),
        Pin(15),
        Pin(16),
        Pin(17),
        Pin(18),
        Pin(19),
        Pin(20),
        Pin(21),
        Pin(22),
        Pin(23),
        Pin(24),
        Pin(25),
        Pin(26),
        Pin(27),
        Pin(28),
        Pin(29),
        Pin(30),
        Pin(31),
        Pin(32),
        Pin(33),
        Pin(34),
        Pin(35),
        Pin(36),
        Pin(37),
        Pin(38),
        Pin(39),
        Pin(40),
        Pin(41),
        Pin(42),
        Pin(43),
        Pin(44, pwm=True),
        Pin(45, pwm=True),
        Pin(46, pwm=True),
        Pin(47),
        Pin(48),
        Pin(49),
        Pin(50),
        Pin(51),
        Pin(52),
        Pin(53),
        Pin(54, analog=True),
        Pin(55, analog=True),
        Pin(56, analog=True),
        Pin(57, analog=True),
        Pin(58, analog=True),
        Pin(59, analog=True),
        Pin(60, analog=True),
        Pin(61, analog=True),
        Pin(62, analog=True),
        Pin(63, analog=True),
        Pin(64, analog=True),
        Pin(65, analog=True),
        Pin(66, analog=True),
        Pin(67, analog=True),
        Pin(68, analog=True),
        Pin(69, analog=True),
    )


class Arduino:

    def __init__(self, board_type, port=None):
        if board_type == UNO:
            self._pins = _get_uno_pins()
        elif board_type == MEGA2560:
            self._pins = _get_mega2560_pins()
        else:
            raise UnknownBoardError('Unknown `board_type` of "{}" specified'.format(board_type))
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
