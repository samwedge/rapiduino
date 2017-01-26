import struct
import abc
import six
from serial import Serial, SerialException

from rapiduino.exceptions import SerialConnectionError


@six.add_metaclass(abc.ABCMeta)
class Connection(object):

    def process_command(self, command, *args):
        command_spec = self._command_spec
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
        self._send(tuple(command_sequence))

    @abc.abstractmethod
    def open(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def close(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _send(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _recv(self, *args, **kwargs):
        pass

    @property
    def _command_spec(self):
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


class SerialConnection(Connection):

    def __init__(self, conn=None):
        self.conn = conn

    def open(self, port, baudrate=9600, timeout=1):
        if not self.conn:
            try:
                self.conn = Serial(port, baudrate=baudrate, timeout=timeout)
            except SerialException:
                raise

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def _send(self, data):
        if self.conn:
            bytes = struct.pack('{}B'.format(len(data)), *data)
            n_bytes_written = self.conn.write(bytes)
            if n_bytes_written != len(data):
                raise SerialConnectionError('Error sending data - not all bytes written')
        else:
            raise SerialConnectionError('Error sending data - not connected')

    def _recv(self, n_bytes):
        if self.conn:
            bytes = self.conn.read(n_bytes)
            if len(bytes) != n_bytes:
                raise SerialConnectionError('Error sending data - not all bytes read')
            data = struct.unpack('{}B'.format(n_bytes), bytes)
            return data
        else:
            raise SerialConnectionError('Error receiving data - not connected')
