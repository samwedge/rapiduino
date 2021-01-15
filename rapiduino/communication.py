import struct
from typing import Tuple, Optional

from serial import Serial, SerialException

from rapiduino import CommandSpec
from rapiduino.exceptions import (
    NotConnectedSerialConnectionError,
    SerialConnectionSendDataError,
    ReceiveDataSerialConnectionError,
)


class SerialConnection:
    def __init__(self, conn: Serial) -> None:
        self.conn = conn

    @classmethod
    def build(
        cls, port: Optional[str], baudrate: int = 115200, timeout: int = 1
    ) -> "SerialConnection":
        try:
            conn = Serial(port, baudrate=baudrate, timeout=timeout)
        except SerialException:
            raise NotConnectedSerialConnectionError()
        return cls(conn)

    def close(self) -> None:
        self.conn.close()
        self.conn = None

    def process_command(self, command: CommandSpec, *args: int) -> Tuple[int, ...]:
        for arg in args:
            if type(arg) != int:
                raise TypeError(
                    "Expected args to be int, but received {}".format(type(arg))
                )
        if len(args) != command.tx_len:
            raise ValueError(
                "Expected args to be length {}, but received length {}".format(
                    command.tx_len, len(args)
                )
            )

        self._send(command, args)

        return self._recv(command)

    def _send(self, cmd_spec: CommandSpec, data: Tuple[int, ...]) -> None:
        if self.conn:
            bytes_to_send = struct.pack(
                "B{}{}".format(cmd_spec.tx_len, cmd_spec.tx_type), cmd_spec.cmd, *data
            )
            n_bytes_written = self.conn.write(bytes_to_send)
            if n_bytes_written != (len(data) + 1):
                raise SerialConnectionSendDataError()
        else:
            raise NotConnectedSerialConnectionError()

    def _recv(self, cmd_spec: CommandSpec) -> Tuple[int, ...]:
        if cmd_spec.rx_len == 0:
            return ()
        if self.conn:
            bytes_read = self.conn.read(cmd_spec.rx_len)
            if len(bytes_read) != cmd_spec.rx_len:
                raise ReceiveDataSerialConnectionError()
            return struct.unpack(
                "{}{}".format(cmd_spec.rx_len, cmd_spec.rx_type), bytes_read
            )
        else:
            raise NotConnectedSerialConnectionError()
