from rapiduino.globals import *


class Pin(object):

    def __init__(self, id, pwm=False, analog=False):
        self._pin_mode = INPUT
        self._pwm = pwm
        self._analog = analog
        self._pin_state = LOW
        self._id = id

    @property
    def id(self):
        return self._id

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
        return self._pwm

    @property
    def is_analog(self):
        return self._analog
