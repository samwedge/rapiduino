import serial

from rapiduino.exceptions import SerialConnectionError


class SerialConnection(object):

    def __init__(self):
        self.conn = None

    def connect(self, port, baudrate=9600, timeout=1):
        try:
            self.conn = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        except Exception as e:
            raise SerialConnectionError(e)


class Commands(object):

    def __init__(self):
        self._command_list = []

    @property
    def command_list(self):
        return tuple(self._command_list)

    def add_command(self, command, *args):
        command_spec = self._get_command_spec()
        if type(command) != str:
            raise TypeError('Expected command to be str, but received {}'.format(type(command)))
        if command not in command_spec.keys():
            raise KeyError('{} not in command specification'.format(command))
        for arg in args:
            if type(arg) != int:
                raise TypeError('Expected args to be int, but received {}'.format(type(arg)))
        if len(args) != command_spec[command]['nargs']:
            raise ValueError(
                'Expected args to be length {}, but received length {}'.format(
                    command_spec[command]['nargs'], len(args)
                )
            )

        command_sequence = list(args)
        command_sequence.insert(0, command_spec[command]['cmd'])
        self._command_list.append(tuple(command_sequence))

    def next_command(self):
        return self._command_list.pop(0)

    @property
    def command_spec(self):
        return self._get_command_spec()

    @staticmethod
    def _get_command_spec():
        return {
            'poll': {
                'cmd': 0,
                'nargs': 0
            },
            'parrot': {
                'cmd': 1,
                'nargs': 1
            },
            'version': {
                'cmd': 2,
                'nargs': 0
            },
            'pinMode': {
                'cmd': 10,
                'nargs': 2
            },
            'digitalRead': {
                'cmd': 20,
                'nargs': 1
            },
            'digitalWrite': {
                'cmd': 21,
                'nargs': 2
            },
            'analogRead': {
                'cmd': 30,
                'nargs': 1
            },
            'analogWrite': {
                'cmd': 31,
                'nargs': 2
            },
        }
