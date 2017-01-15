import struct
from serial import SerialException
from mock import patch, Mock
import unittest
from rapiduino.communication import Commands, SerialConnection
from rapiduino.exceptions import SerialConnectionError


class TestSerialConnection(unittest.TestCase):

    def setUp(self):
        self.serial_connection = SerialConnection()
        self.port = '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 5
        self.data = (1, 2, 3)
        self.bytes = struct.pack('BBB', *self.data)

    def test_init(self):
        self.assertIsInstance(self.serial_connection, SerialConnection)

    def test_connect(self):
        self.assertIsNone(self.serial_connection.conn)
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            self.serial_connection.connect(self.port, self.baudrate, self.timeout)
            self.assertEqual(self.serial_connection.conn, mock_serial.return_value)
            mock_serial.assert_called_once_with(self.port, baudrate=self.baudrate, timeout=self.timeout)

    def test_connect_with_error(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_serial.side_effect = SerialException('Some Error Message')
            with self.assertRaisesRegexp(SerialException, 'Some Error Message'):
                self.serial_connection.connect(self.port)
            self.assertIsNone(self.serial_connection.conn)

    def test_close(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            self.serial_connection.connect(self.port)

            self.assertEqual(self.serial_connection.conn, mock_conn)
            self.serial_connection.close()
            mock_conn.close.assert_called_once_with()
            self.assertIsNone(self.serial_connection.conn)

    def test_send(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.write.return_value = len(self.data)
            mock_serial.return_value = mock_conn

            self.serial_connection.connect(self.port)
            self.serial_connection.send(self.data)

            mock_conn.write.assert_called_once_with(self.bytes)

    def test_send_with_error_writing_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.write.return_value = len(self.data) - 1
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes written'):
                self.serial_connection.connect(self.port)
                self.serial_connection.send(self.data)

            mock_conn.write.assert_called_once_with(self.bytes)

    def test_send_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection.send(self.data)

            mock_conn.write.assert_not_called()

    def test_recv(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.bytes
            mock_serial.return_value = mock_conn

            self.serial_connection.connect(self.port)
            received_data = self.serial_connection.recv(len(self.data))

            self.assertTupleEqual(received_data, self.data)
            mock_conn.read.assert_called_once_with(len(self.data))

    def test_recv_with_error_reading_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.bytes
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes read'):
                self.serial_connection.connect(self.port)
                self.serial_connection.recv(len(self.data) + 1)

            mock_conn.read.assert_called_once_with(len(self.data) + 1)

    def test_recv_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection.recv(len(self.data))

            mock_conn.read.assert_not_called()


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()
        self.commands.add_command('poll')
        self.commands.add_command('parrot', 7)
        self.commands.add_command('pinMode', 3, 1)
        self.commands.add_command('analogRead', 5)
        self.commands.add_command('analogWrite', 17, 1)

    def test_commands_have_been_added(self):
        expected_commands = (
            (0,),
            (1, 7),
            (10, 3, 1),
            (30, 5),
            (31, 17, 1)
        )
        self.assertEqual(self.commands.command_list, expected_commands)

    def test_invalid_command_raises_error(self):
        with self.assertRaises(KeyError):
            self.commands.add_command('invalidCommand')

    def test_invalid_args_raises_error(self):
        with self.assertRaises(TypeError):
            self.commands.add_command('parrot', 3.7)

    def test_invalid_number_of_args_raises_error(self):
        with self.assertRaises(ValueError):
            self.commands.add_command('parrot', 0, 0)

    def test_commands_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.commands.command_list = []

    def test_next_command(self):
        expected_first_command = (0,)
        expected_remaining_commands = (
            (1, 7),
            (10, 3, 1),
            (30, 5),
            (31, 17, 1)
        )
        popped_command = self.commands.next_command()
        self.assertEqual(popped_command, expected_first_command)
        self.assertEqual(self.commands.command_list, expected_remaining_commands)

    def test_add_command_rejects_non_tuple(self):
        with self.assertRaises(TypeError):
            self.commands.add_command(0)

    def test_command_spec(self):
        self.assertIsInstance(self.commands.command_spec, dict)
        for key in self.commands.command_spec.keys():
            self.assertIn('cmd', self.commands.command_spec[key])
            self.assertIn('nargs', self.commands.command_spec[key])
            self.assertEqual(len(self.commands.command_spec[key]), 2)
            self.assertIsInstance(self.commands.command_spec[key]['cmd'], int)
            self.assertIsInstance(self.commands.command_spec[key]['nargs'], int)

    def test_command_spec_readonly(self):
        with self.assertRaises(AttributeError):
            self.commands.command_spec = 5


if __name__ == '__main__':
    unittest.main()
