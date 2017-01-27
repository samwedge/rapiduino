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
        if len(args) != command_spec[command]['tx_len']:
            raise ValueError(
                'Expected args to be length {}, but received length {}'.format(
                    command_spec[command]['tx_len'], len(args)
                )
            )

        command_sequence = list(args)
        command_sequence.insert(0, command_spec[command]['cmd'])
        self._send(command_spec[command], args)

        return self._recv(command_spec[command])

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
                'tx_len': 0,
                'tx_type': 'B',
                'rx_len': 1,
                'rx_type': 'B'
            },
            'parrot': {
                'cmd': 1,
                'tx_len': 1,
                'tx_type': 'B',
                'rx_len': 1,
                'rx_type': 'B'
            },
            'version': {
                'cmd': 2,
                'tx_len': 0,
                'tx_type': 'B',
                'rx_len': 3,
                'rx_type': 'B'
            },
            'pinMode': {
                'cmd': 10,
                'tx_len': 2,
                'tx_type': 'B',
                'rx_len': 0,
                'rx_type': ''
            },
            'digitalRead': {
                'cmd': 20,
                'tx_len': 1,
                'tx_type': 'B',
                'rx_len': 1,
                'rx_type': 'B'
            },
            'digitalWrite': {
                'cmd': 21,
                'tx_len': 2,
                'tx_type': 'B',
                'rx_len': 0,
                'rx_type': ''
            },
            'analogRead': {
                'cmd': 30,
                'tx_len': 1,
                'tx_type': 'B',
                'rx_len': 1,
                'rx_type': 'H'
            },
            'analogWrite': {
                'cmd': 31,
                'tx_len': 2,
                'tx_type': 'B',
                'rx_len': 0,
                'rx_type': ''
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

    def _send(self, cmd_spec, data):
        if self.conn:
            bytes_to_send = struct.pack('B{}{}'.format(cmd_spec['tx_len'], cmd_spec['tx_type']), cmd_spec['cmd'], *data)
            n_bytes_written = self.conn.write(bytes_to_send)
            if n_bytes_written != (len(data) + 1):
                raise SerialConnectionError('Error sending data - not all bytes written')
        else:
            raise SerialConnectionError('Error sending data - not connected')

    def _recv(self, cmd_spec):
        if cmd_spec['rx_len'] == 0:
            return
        if self.conn:
            bytes_read = self.conn.read(cmd_spec['rx_len'])
            if len(bytes_read) != cmd_spec['rx_len']:
                raise SerialConnectionError('Error sending data - not all bytes read')
            return struct.unpack('{}{}'.format(cmd_spec['rx_len'], cmd_spec['rx_type']), bytes_read)
        else:
            raise SerialConnectionError('Error receiving data - not connected')
