import serial
from rapiduino.exceptions import SerialConnectionError

class SerialConnection(object):

    def __init__(self):
        pass

    def connect(self, port=None):
        if port is None:
            raise SerialConnectionError('port cannot be None')
        else:
            raise NotImplementedError


class Commands(object):

    def __init__(self):
        self._command_list = []

    @property
    def command_list(self):
        return tuple(self._command_list)

    def add_command(self, command):
        if type(command) != tuple:
            raise TypeError('Expected tuple, but received {}'.format(type(command)))
        self._command_list.append(command)

    def next_command(self):
        return self._command_list.pop(0)
