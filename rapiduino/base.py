from rapiduino.globals.common import *


class Pin(object):

    def __init__(self, id, pwm=False, analog=False):
        self._pin_mode = INPUT
        self._pwm = pwm
        self._analog = analog
        self._pin_state = LOW
        self._id = id
        self._bound_to = None

    @property
    def id(self):
        return self._id

    @property
    def is_pwm(self):
        return self._pwm

    @property
    def is_analog(self):
        return self._analog

    @property
    def bound_to(self):
        return self._bound_to

    def bind(self, instance, pin_no):
        self._bound_to = (instance, pin_no)
