import abc
import six

from rapiduino.exceptions import NoDeviceBoundError


@six.add_metaclass(abc.ABCMeta)
class BaseComponent(object):

    _bound_device = None

    def _setup(self):
        pass

    @property
    def pins(self):
        return self._pins

    @property
    def bound_device(self):
        return self._bound_device

    def bind_to_device(self, device):
        self._bound_device = device
        self._setup()

    def unbind_to_device(self):
        self._bound_device = None

    def _assert_bound_to_device(self):
        if self._bound_device is None:
            raise NoDeviceBoundError()

    def _digital_read(self, pin_no):
        self._assert_bound_to_device()
        return self._bound_device.digital_read(pin_no, force=True)

    def _digital_write(self, pin_no, state):
        self._assert_bound_to_device()
        self._bound_device.digital_write(pin_no, state, force=True)

    def _analog_read(self, pin_no):
        self._assert_bound_to_device()
        return self._bound_device.analog_read(pin_no, force=True)

    def _analog_write(self, pin_no, value):
        self._assert_bound_to_device()
        self._bound_device.analog_write(pin_no, value, force=True)

    def _pin_mode(self, pin_no, mode):
        self._assert_bound_to_device()
        self._bound_device.pin_mode(pin_no, mode, force=True)
