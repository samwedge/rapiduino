from collections import namedtuple

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


CommandSpec = namedtuple('CommandSpec', ['command', 'nvars', 'description'])


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

    @property
    def command_spec(self):
        return self._get_command_spec()

    @staticmethod
    def _get_command_spec():
        return (
            CommandSpec(0, 0, 'poll'),
            CommandSpec(1, 1, 'parrot'),
            CommandSpec(2, 0, 'version'),
            CommandSpec(10, 2, 'pinMode'),
            CommandSpec(20, 1, 'digitalRead'),
            CommandSpec(21, 2, 'digitalWrite'),
            CommandSpec(30, 1, 'analogRead'),
            CommandSpec(31, 2, 'analogWrite')
        )
