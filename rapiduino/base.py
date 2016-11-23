from rapiduino.globals import *


class Pin(object):

    def __init__(self):
        self._pin_mode = INPUT
        self._is_pwm = False
        self._is_analog = False
        self._pin_state = LOW

    @property
    def pin_mode(self):
        return self._pin_mode

    @pin_mode.setter
    def pin_mode(self, value):
        if value in [INPUT, INPUT_PULLUP, OUTPUT]:
            self._pin_mode = value
        else:
            raise ValueError(
                'pin_mode must be INPUT, OUTPUT or INPUT_PULLUP but {} was found'.format(value)
            )

    @property
    def pin_state(self):
        return self._pin_state

    @pin_state.setter
    def pin_state(self, value):
        if value in [HIGH, LOW]:
            self._pin_state = value
        else:
            raise ValueError(
                'pin_state must be INPUT, OUTPUT or INPUT_PULLUP but {} was found'.format(value)
            )

    @property
    def is_pwm(self):
        return self._is_pwm

    @property
    def is_analog(self):
        return self._is_analog
