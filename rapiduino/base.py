from rapiduino.globals import *


class Pin(object):

    def __init__(self):
        self._pin_mode = INPUT
        self._pwm_enabled = False
        self._is_analog = False

    @property
    def pin_mode(self):
        return self._pin_mode

    @property
    def is_analog(self):
        return self._is_analog

    @pin_mode.setter
    def pin_mode(self, value):
        if value in [INPUT, INPUT_PULLUP, OUTPUT]:
            self._pin_mode = value
        else:
            raise ValueError(
                'pin_mode must be INPUT, OUTPUT or INPUT_PULLUP but {} was found'.format(value)
            )

    @property
    def pwm_enabled(self):
        return self._pwm_enabled