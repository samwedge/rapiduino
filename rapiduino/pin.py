from rapiduino.exceptions import AlreadyBoundPinError
from rapiduino.globals.common import INPUT, LOW


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


class DevicePin(Pin):
    def __init__(self, id, pwm=False, analog=False, protected=False):
        super(DevicePin, self).__init__(id, pwm, analog)
        self._protected = protected

    @property
    def is_protected(self):
        return self._protected

    def bind(self, instance, pin_no):
        super(DevicePin, self).bind(instance, pin_no)
        self._protected = True

    def unbind(self):
        super(DevicePin, self).unbind()
        self._protected = False


class ComponentPin(Pin):
    def __init__(self, id, pwm=False, analog=False):
        super(ComponentPin, self).__init__(id, pwm, analog)
