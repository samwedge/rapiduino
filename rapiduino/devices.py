from rapiduino.base import Pin
from rapiduino.communication import Commands
from rapiduino.exceptions import PinError
from rapiduino.globals import *


class ArduinoBase(object):

    def __init__(self):
        self.commands = Commands()

    def digital_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        self.commands.add_command('digitalRead', pin_no)

    def digital_write(self, pin_no, state):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_state(state)
        self.commands.add_command('digitalWrite', pin_no, state.value)

    def analog_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        self.commands.add_command('analogRead', pin_no)

    def analog_write(self, pin_no, value):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_analog_write_range(value)
        self._assert_analog_pin(pin_no)
        self.commands.add_command('analogWrite', pin_no, value)

    def pin_mode(self, pin_no, mode):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self.commands.add_command('pinMode', pin_no, mode.value)

    def _assert_valid_pin_number(self, pin_no):
        if (pin_no >= len(self.pins)) or (pin_no < 0):
            raise IndexError('Specified pin number {} is outside pin range of {}'.format(pin_no, len(self.pins)))

    def _assert_analog_pin(self, pin_no):
        if not self.pins[pin_no].is_analog:
            raise PinError('cannot complete operation as analog=False for pin {}'.format(pin_no))

    @staticmethod
    def _assert_valid_analog_write_range(value):
        if not isinstance(value, int):
            raise TypeError('Expected analog value type to be int, but found {}'.format(type(value)))
        if (value < 0) or (value >= 255):
            raise ValueError('Specified analog value {} is not valid'.format(value))

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

    def __init__(self):
        super(ArduinoUno, self).__init__()
        self._pins = (
            Pin(0),
            Pin(1),
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
