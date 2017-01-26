import struct
from serial import SerialException
from mock import patch, Mock
import unittest
from rapiduino.communication import Connection, SerialConnection
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
        self.assertIsInstance(self.serial_connection, Connection)

    def test_command_spec(self):
        self.assertIsInstance(self.serial_connection._command_spec, dict)
        for key in self.serial_connection._command_spec.keys():
            self.assertIn('cmd', self.serial_connection._command_spec[key])
            self.assertIn('nargs', self.serial_connection._command_spec[key])
            self.assertEqual(len(self.serial_connection._command_spec[key]), 2)
            self.assertIsInstance(self.serial_connection._command_spec[key]['cmd'], int)
            self.assertIsInstance(self.serial_connection._command_spec[key]['nargs'], int)

    def test_open(self):
        self.assertIsNone(self.serial_connection.conn)
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            self.serial_connection.open(self.port, self.baudrate, self.timeout)
            self.assertEqual(self.serial_connection.conn, mock_serial.return_value)
            mock_serial.assert_called_once_with(self.port, baudrate=self.baudrate, timeout=self.timeout)

    def test_open_with_error(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_serial.side_effect = SerialException('Some Error Message')
            with self.assertRaisesRegexp(SerialException, 'Some Error Message'):
                self.serial_connection.open(self.port)
            self.assertIsNone(self.serial_connection.conn)

    def test_close(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            self.serial_connection.open(self.port)

            self.assertEqual(self.serial_connection.conn, mock_conn)
            self.serial_connection.close()
            mock_conn.close.assert_called_once_with()
            self.assertIsNone(self.serial_connection.conn)

    def test_send(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.write.return_value = len(self.data)
            mock_serial.return_value = mock_conn

            self.serial_connection.open(self.port)
            self.serial_connection._send(self.data)

            mock_conn.write.assert_called_once_with(self.bytes)

    def test_send_with_error_writing_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.write.return_value = len(self.data) - 1
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes written'):
                self.serial_connection.open(self.port)
                self.serial_connection._send(self.data)

            mock_conn.write.assert_called_once_with(self.bytes)

    def test_send_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection._send(self.data)

            mock_conn.write.assert_not_called()

    def test_recv(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.bytes
            mock_serial.return_value = mock_conn

            self.serial_connection.open(self.port)
            received_data = self.serial_connection._recv(len(self.data))

            self.assertTupleEqual(received_data, self.data)
            mock_conn.read.assert_called_once_with(len(self.data))

    def test_recv_with_error_reading_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.bytes
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes read'):
                self.serial_connection.open(self.port)
                self.serial_connection._recv(len(self.data) + 1)

            mock_conn.read.assert_called_once_with(len(self.data) + 1)

    def test_recv_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection._recv(len(self.data))

            mock_conn.read.assert_not_called()

    @patch.object(SerialConnection, '_send')
    def test_process_command(self, mocked_send):
        self.serial_connection.process_command('parrot', 5)
        mocked_send.assert_called_once_with((1, 5))

    @patch.object(SerialConnection, '_send')
    def test_process_command_with_invalid_command(self, mocked_send):
        with self.assertRaises(KeyError):
            self.serial_connection.process_command('invalidCommand')
        mocked_send.assert_not_called()

    @patch.object(SerialConnection, '_send')
    def test_process_command_with_invalid_args(self, mocked_send):
        with self.assertRaises(TypeError):
            self.serial_connection.process_command('parrot', 3.7)
        mocked_send.assert_not_called()

    @patch.object(SerialConnection, '_send')
    def test_process_command_with_invalid_number_of_args(self, mocked_send):
        with self.assertRaises(ValueError):
            self.serial_connection.process_command('parrot', 0, 0)
        mocked_send.assert_not_called()


if __name__ == '__main__':
    unittest.main()
