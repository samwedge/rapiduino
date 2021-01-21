__all__ = ["LOW", "HIGH", "INPUT", "OUTPUT", "INPUT_PULLUP"]

from dataclasses import dataclass


@dataclass(frozen=True)
class PinMode:
    name: str
    value: int


@dataclass(frozen=True)
class PinState:
    name: str
    value: int


LOW = PinState("LOW", 0)
HIGH = PinState("HIGH", 1)

INPUT = PinMode("INPUT", 0)
OUTPUT = PinMode("OUTPUT", 1)
INPUT_PULLUP = PinMode("INPUT_PULLUP", 2)
