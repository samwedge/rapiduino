import struct
from typing import Tuple

from serial import Serial

from rapiduino.communication.command_spec import CommandSpec
from rapiduino.exceptions import (
    SerialConnectionReceiveDataError,
    SerialConnectionSendDataError,
)


class SerialConnection:
    def __init__(self, conn: Serial) -> None:
        self.conn = conn

    @classmethod
    def build(
        cls, port: str, baudrate: int = 115200, timeout: int = 1
    ) -> "SerialConnection":
        conn = Serial(port, baudrate=baudrate, timeout=timeout)
        return cls(conn)

    def process_command(self, command: CommandSpec, *args: int) -> Tuple[int, ...]:
        if len(args) != command.tx_len:
            raise ValueError(
                f"Expected args to be length {command.tx_len}, "
                f"but received length {len(args)}"
            )

        self._send(command, args)

        return self._recv(command)

    def _send(self, cmd_spec: CommandSpec, data: Tuple[int, ...]) -> None:
        bytes_to_send = struct.pack(
            f"B{cmd_spec.tx_len}{cmd_spec.tx_type}", cmd_spec.cmd, *data
        )
        n_bytes_written = self.conn.write(bytes_to_send)
        if n_bytes_written != len(bytes_to_send):
            raise SerialConnectionSendDataError(
                n_bytes_intended=len(bytes_to_send), n_bytes_actual=n_bytes_written
            )

    def _recv(self, cmd_spec: CommandSpec) -> Tuple[int, ...]:
        if cmd_spec.rx_len == 0:
            return ()
        bytes_read = self.conn.read(cmd_spec.rx_len)
        if len(bytes_read) != cmd_spec.rx_len:
            raise SerialConnectionReceiveDataError(
                n_bytes_intended=cmd_spec.rx_len,
                n_bytes_actual=len(bytes_read),
            )
        return struct.unpack(f"{cmd_spec.rx_len}{cmd_spec.rx_type}", bytes_read)
