import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseComponent(object):

    def __init__(self):
        self.device = None

    @property
    def pins(self):
        return self._pins

    def bind_to_device(self, device):
        self.device = device
