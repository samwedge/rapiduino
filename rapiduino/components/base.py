import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseComponent(object):

    def __init__(self):
        self._bound_device = None

    def setup(self):
        pass

    @property
    def pins(self):
        return self._pins

    @property
    def bound_device(self):
        return self._bound_device

    def bind_to_device(self, device):
        self._bound_device = device
        self.setup()

    def unbind_to_device(self):
        self._bound_device = None

    def _digital_read(self, pin_no):
        return self._bound_device.digital_read(pin_no, force=True)

    def _digital_write(self, pin_no, state):
        self._bound_device.digital_write(pin_no, state, force=True)

    def _analog_read(self, pin_no):
        return self._bound_device.analog_read(pin_no, force=True)

    def _analog_write(self, pin_no, value):
        self._bound_device.analog_write(pin_no, value, force=True)

    def _pin_mode(self, pin_no, mode):
        self._bound_device.pin_mode(pin_no, mode, force=True)
