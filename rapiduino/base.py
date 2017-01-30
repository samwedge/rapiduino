from rapiduino.globals.common import *


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
    def is_pwm(self):
        return self._pwm

    @property
    def is_analog(self):
        return self._analog
