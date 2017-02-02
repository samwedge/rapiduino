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



