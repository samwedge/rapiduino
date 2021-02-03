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
        self.__board.pin_mode(pin_no, mode, self.__token)

    def _digital_read(self, pin_no: int) -> PinState:
        return self.__board.digital_read(pin_no, self.__token)

    def _digital_write(self, pin_no: int, state: PinState) -> None:
        self.__board.digital_write(pin_no, state, self.__token)

    def _analog_read(self, pin_no: int) -> int:
        return self.__board.analog_read(pin_no, self.__token)

    def _analog_write(self, pin_no: int, value: int) -> None:
        self.__board.analog_write(pin_no, value, self.__token)

    @abstractmethod
    def _setup(self) -> None:
        """Implement this method to set the initial pin mode and state.
        Always explicitly set the state you want. Do not rely on
        Arduino defaults, as this component may be being "hotswapped",
        so may be in an unexpected state.
        """

    def __register_component(self) -> None:
        self.__board.register_component(self.__token, self._pins)
