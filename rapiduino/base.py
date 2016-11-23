from rapiduino.globals import *


class Pin(object):
    def __init__(self):
        self._pin_mode = INPUT
        self.pwm_enabled = False

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