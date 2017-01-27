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
        self.version_tx_data = (2,)
        self.version_tx_bytes = struct.pack('B', *self.version_tx_data)
        self.version_rx_data = (1, 2, 3)
        self.version_rx_bytes = struct.pack('BBB', *self.version_rx_data)
        self.version_cmd_spec = {
                'cmd': 2,
                'tx_len': 0,
                'tx_type': 'B',
                'rx_len': 3,
                'rx_type': 'B'
            }
        self.digital_write_tx_data = (21, 1, 2)
        self.digital_write_tx_bytes = struct.pack('BBB', *self.digital_write_tx_data)
        self.digital_write_cmd_spec = {
                'cmd': 21,
                'tx_len': 2,
                'tx_type': 'B',
                'rx_len': 0,
                'rx_type': ''
            }

    def test_init(self):
        self.assertIsInstance(self.serial_connection, SerialConnection)
        self.assertIsInstance(self.serial_connection, Connection)

    def test_command_spec(self):
        self.assertIsInstance(self.serial_connection._command_spec, dict)
        schema_keys = ['cmd', 'tx_len', 'tx_type', 'rx_len', 'rx_type']
        schema_types = [int, int, str, int, str]
        for key in self.serial_connection._command_spec.keys():
            self.assertEqual(len(self.serial_connection._command_spec[key]), len(schema_keys))
            for schema_key, schema_type in zip(schema_keys, schema_types):
                self.assertIn(schema_key, self.serial_connection._command_spec[key])
                self.assertIsInstance(self.serial_connection._command_spec[key][schema_key], schema_type)

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
            mock_conn.write.return_value = len(self.digital_write_tx_data)
            mock_serial.return_value = mock_conn

            self.serial_connection.open(self.port)
            self.serial_connection._send(self.digital_write_cmd_spec, self.digital_write_tx_data[1::])

            mock_conn.write.assert_called_once_with(self.digital_write_tx_bytes)

    def test_send_with_error_writing_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.write.return_value = len(self.digital_write_tx_data) + 1
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes written'):
                self.serial_connection.open(self.port)
                self.serial_connection._send(self.digital_write_cmd_spec, self.digital_write_tx_data[1::])

            mock_conn.write.assert_called_once_with(self.digital_write_tx_bytes)

    def test_send_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection._send(self.digital_write_cmd_spec, self.digital_write_tx_data[1::])

            mock_conn.write.assert_not_called()

    def test_recv(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.version_rx_bytes
            mock_serial.return_value = mock_conn

            self.serial_connection.open(self.port)
            received_data = self.serial_connection._recv(self.version_cmd_spec)

            self.assertTupleEqual(received_data, self.version_rx_data)
            mock_conn.read.assert_called_once_with(len(self.version_rx_data))

    def test_recv_with_no_data_to_recv(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn
            self.serial_connection.open(self.port)
            received_data = self.serial_connection._recv(self.digital_write_cmd_spec)

            self.assertIsNone(received_data)
            mock_conn.read.assert_not_called()

    def test_recv_with_error_reading_bytes(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_conn.read.return_value = self.version_rx_bytes
            mock_serial.return_value = mock_conn
            self.version_cmd_spec['rx_len'] += 1
            with self.assertRaisesRegexp(SerialConnectionError, 'not all bytes read'):
                self.serial_connection.open(self.port)
                self.serial_connection._recv(self.version_cmd_spec)

            mock_conn.read.assert_called_once_with(len(self.version_rx_data) + 1)

    def test_recv_without_connecting(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_conn = Mock()
            mock_serial.return_value = mock_conn

            with self.assertRaisesRegexp(SerialConnectionError, 'not connected'):
                self.serial_connection._recv(self.version_cmd_spec)

            mock_conn.read.assert_not_called()

    @patch.object(SerialConnection, '_recv')
    @patch.object(SerialConnection, '_send')
    def test_process_command(self, mocked_send, mocked_recv):
        mocked_recv.return_value = self.version_rx_data

        received = self.serial_connection.process_command('version')

        mocked_send.assert_called_once_with(self.version_cmd_spec, self.version_tx_data[1::])
        mocked_recv.assert_called_once_with(self.version_cmd_spec)
        self.assertEqual(received, self.version_rx_data)

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
