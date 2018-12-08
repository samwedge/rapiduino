import struct
from serial import SerialException, Serial
from mock import patch, Mock, call
import unittest2

from rapiduino.commands import CMD_VERSION, CMD_DIGITALWRITE, CMD_PARROT
from rapiduino.communication import SerialConnection
from rapiduino.exceptions import (NotConnectedSerialConnectionError, ReceiveDataSerialConnectionError,
                                  SerialConnectionSendDataError)


class TestSerialConnection(unittest2.TestCase):

    def setUp(self):
        self.mock_conn = Mock(spec=Serial)
        self.serial_connection = SerialConnection(self.mock_conn)
        self.port = '/dev/ttyACM0'
        self.version_tx_data = (2,)
        self.version_tx_bytes = struct.pack('B', *self.version_tx_data)
        self.version_rx_data = (1, 2, 3)
        self.version_rx_bytes = struct.pack('BBB', *self.version_rx_data)
        self.digital_write_tx_data = (21, 1, 2)
        self.digital_write_tx_bytes = struct.pack('BBB', *self.digital_write_tx_data)

    def test_open_with_valid_connection_parameters(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_serial.return_value = self.mock_conn
            SerialConnection.build(self.port, 115200, 5)
            self.assertEqual(self.serial_connection.conn, mock_serial.return_value)
            self.assertEqual(mock_serial.call_args, call(self.port, baudrate=115200, timeout=5))

    def test_open_with_error(self):
        with patch('rapiduino.communication.Serial', autospec=True) as mock_serial:
            mock_serial.side_effect = SerialException()
            with self.assertRaises(NotConnectedSerialConnectionError):
                self.serial_connection.build(self.port)

    def test_close_when_connection_open(self):
        self.serial_connection.close()
        self.mock_conn.close.assert_called_once_with()

    def test_process_command_with_valid_command_returning_bytes(self):
        self.mock_conn.write.return_value = 1
        self.mock_conn.read.return_value = self.version_rx_bytes
        received = self.serial_connection.process_command(CMD_VERSION)
        self.assertEqual(received, self.version_rx_data)

    def test_process_command_with_valid_command_returning_zero_bytes(self):
        self.mock_conn.write.return_value = 3
        self.mock_conn.read.return_value = self.version_rx_bytes
        received = self.serial_connection.process_command(CMD_DIGITALWRITE, 1, 1)
        self.assertEqual(received, ())
        self.assertEqual(self.mock_conn.read.call_count, 0)

    def test_process_command_with_invalid_args(self):
        with self.assertRaises(TypeError):
            self.serial_connection.process_command(CMD_PARROT, 3.7)
        self.assertEqual(self.mock_conn.write.call_count, 0)

    def test_process_command_with_invalid_number_of_args(self):
        with self.assertRaises(ValueError):
            self.serial_connection.process_command(CMD_PARROT, 0, 0)
        self.assertEqual(self.mock_conn.write.call_count, 0)

    def test_process_command_when_connection_closed(self):
        self.serial_connection.close()
        with self.assertRaises(NotConnectedSerialConnectionError):
            self.serial_connection.process_command(CMD_VERSION)
        self.assertEqual(self.mock_conn.write.call_count, 0)

    def test_process_command_when_error_reading_bytes(self):
        self.mock_conn.write.return_value = 1
        self.mock_conn.read.return_value = struct.pack('BBBB', 1, 2, 3, 4)
        with self.assertRaises(ReceiveDataSerialConnectionError):
            self.serial_connection.process_command(CMD_VERSION)

    def test_process_command_when_error_writing_bytes(self):
        self.mock_conn.write.return_value = 2
        self.mock_conn.read.return_value = self.version_rx_bytes
        with self.assertRaises(SerialConnectionSendDataError):
            self.serial_connection.process_command(CMD_VERSION)
