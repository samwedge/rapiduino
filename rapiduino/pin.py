from rapiduino.exceptions import AlreadyBoundPinError
from rapiduino.globals.common import INPUT, LOW


class Pin:

    def __init__(self, pin_id, pwm=False, analog=False):
        self._pin_mode = INPUT
        self._pwm = pwm
        self._analog = analog
        self._pin_state = LOW
        self._pin_id = pin_id
        self._bound_to = None

    @property
    def pin_id(self):
        return self._pin_id

    @property
    def is_pwm(self):
        return self._pwm

    @property
    def is_analog(self):
        return self._analog

    @property
    def bound_to(self):
        return self._bound_to

    @property
    def bound_instance(self):
        return self._bound_to[0]

    @property
    def bound_pin_num(self):
        return self._bound_to[1]

    def bind(self, instance, pin_no):
        if self._bound_to is not None:
            raise AlreadyBoundPinError('Cannot bind pin - already bound')
        self._bound_to = (instance, pin_no)

    def unbind(self):
        self._bound_to = None

    def is_bound(self):
        return self.bound_to is not None
