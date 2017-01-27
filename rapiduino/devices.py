from rapiduino.base import Pin
from rapiduino.communication import SerialConnection
from rapiduino.exceptions import PinError
from rapiduino.globals import *


class ArduinoBase(object):

    def __init__(self):
        self.connection = SerialConnection()

    def digital_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        state = self.connection.process_command('digitalRead', pin_no)
        if state[0] == 1:
            return HIGH
        else:
            return LOW

    def digital_write(self, pin_no, state):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_state(state)
        self.connection.process_command('digitalWrite', pin_no, state.value)

    def analog_read(self, pin_no):
        self._assert_valid_pin_number(pin_no)
        self._assert_analog_pin(pin_no)
        return self.connection.process_command('analogRead', pin_no)[0]

    def analog_write(self, pin_no, value):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_analog_write_range(value)
        self._assert_pwm_pin(pin_no)
        self.connection.process_command('analogWrite', pin_no, value)

    def pin_mode(self, pin_no, mode):
        self._assert_valid_pin_number(pin_no)
        self._assert_valid_pin_mode(mode)
        self.connection.process_command('pinMode', pin_no, mode.value)

    def _assert_valid_pin_number(self, pin_no):
        if (pin_no >= len(self.pins)) or (pin_no < 0):
            raise IndexError('Specified pin number {} is outside pin range of {}'.format(pin_no, len(self.pins)))

    def _assert_analog_pin(self, pin_no):
        if not self.pins[pin_no].is_analog:
            raise PinError('cannot complete operation as analog=False for pin {}'.format(pin_no))

    def _assert_pwm_pin(self, pin_no):
        if not self.pins[pin_no].is_pwm:
            raise PinError('cannot complete operation as pwm=False for pin {}'.format(pin_no))

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


class ArduinoMega2560(ArduinoBase):

    def __init__(self):
        super(ArduinoMega2560, self).__init__()
        self._pins = (
            Pin(0),
            Pin(1),
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
