from rapiduino.exceptions import PinError
from rapiduino.globals.common import *


class Pin(object):

    def __init__(self, id, pwm=False, analog=False, protected=False):
        self._pin_mode = INPUT
        self._pwm = pwm
        self._analog = analog
        self._pin_state = LOW
        self._id = id
        self._bound_to = None
        self._protected = protected

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
    def is_protected(self):
        return self._protected

    @property
    def bound_to(self):
        return self._bound_to

    @property
    def bound_instance(self):
        return self._bound_to[0]

    @property
    def bound_pin(self):
        return self._bound_to[1]

    def bind(self, instance, pin_no):
        if self._bound_to is not None:
            raise PinError('Cannot bind pin - already bound')
        self._bound_to = (instance, pin_no)

    def unbind(self):
        self._bound_to = None
