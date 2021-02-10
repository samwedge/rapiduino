import struct
from unittest.mock import Mock

import pytest
from serial import Serial

from rapiduino.communication.command_spec import CMD_DIGITALWRITE, CMD_VERSION
from rapiduino.communication.serial import SerialConnection
from rapiduino.exceptions import (
    SerialConnectionReceiveDataError,
    SerialConnectionSendDataError,
)


def get_mock_serial(
    num_bytes_to_report_on_write: int, bytes_to_return_on_read: bytes
) -> Serial:
    mock_serial = Mock(spec=Serial)
    mock_serial.write.return_value = num_bytes_to_report_on_write
    mock_serial.read.return_value = bytes_to_return_on_read
    return mock_serial


PORT = "/dev/test_port"
CMD_VERSION_RX_DATA = (1, 2, 3)
CMD_VERSION_RX_BYTES = struct.pack("BBB", *CMD_VERSION_RX_DATA)


# def test_close_when_connection_open(serial_connection: SerialConnection) -> None:
#     serial_connection.close()
#     serial_connection.close.assert_called_once_with()


def test_process_command_with_valid_command_returning_bytes() -> None:
    mock_serial = get_mock_serial(1, CMD_VERSION_RX_BYTES)

    serial_connection = SerialConnection(mock_serial)
    received = serial_connection.process_command(CMD_VERSION)

    assert received == CMD_VERSION_RX_DATA


def test_process_command_with_valid_command_returning_zero_bytes() -> None:
    mock_serial = get_mock_serial(3, bytes())

    serial_connection = SerialConnection(mock_serial)
    received = serial_connection.process_command(CMD_DIGITALWRITE, 1, 1)

    assert received == ()


def test_process_command_with_invalid_arg_length() -> None:
    mock_serial = get_mock_serial(3, bytes())

    serial_connection = SerialConnection(mock_serial)
    with pytest.raises(ValueError):
        serial_connection.process_command(CMD_DIGITALWRITE, 1, 1, 1)


def test_process_command_with_invalid_number_of_bytes_reported_by_send() -> None:
    mock_serial = get_mock_serial(2, CMD_VERSION_RX_BYTES)

    serial_connection = SerialConnection(mock_serial)

    with pytest.raises(SerialConnectionSendDataError):
        serial_connection.process_command(CMD_VERSION)


def test_process_command_with_invalid_number_of_bytes_return_from_recv() -> None:
    mock_serial = get_mock_serial(1, bytes())

    serial_connection = SerialConnection(mock_serial)

    with pytest.raises(SerialConnectionReceiveDataError):
        serial_connection.process_command(CMD_VERSION)
