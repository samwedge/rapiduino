__version__ = '1.0.0'

from dataclasses import dataclass


@dataclass
class GlobalParameter:
    name: str
    value: int


@dataclass
class CommandSpec:
    cmd: int
    tx_len: int
    tx_type: str
    rx_len: int
    rx_type: str
