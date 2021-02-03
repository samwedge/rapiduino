from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Tuple

from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.globals.common import PinMode, PinState


class BaseComponent(ABC):
    def __init__(self, board: Arduino, pins: Tuple[Pin, ...]) -> None:
        self._pins = pins
        self.__board = board
        self.__token = uuid.uuid4().hex
        self.__register_component()
        self._setup()

    def _pin_mode(self, pin_no: int, mode: PinMode) -> None:
        self.__board.pin_mode(pin_no, mode)

    def _digital_read(self, pin_no: int) -> PinState:
        return self.__board.digital_read(pin_no)

    def _digital_write(self, pin_no: int, state: PinState) -> None:
        self.__board.digital_write(pin_no, state)

    @abstractmethod
    def _setup(self) -> None:
        """Implement this method to set initial pin mode and state"""

    def __register_component(self) -> None:
        self.__board.register_component(self.__token, self._pins)
