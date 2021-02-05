import uuid
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.exceptions import (
    ComponentAlreadyRegisteredWithArduinoError,
    ComponentNotRegisteredWithArduinoError,
)
from rapiduino.globals.common import PinMode, PinState


class BaseComponent(ABC):
    _board: Arduino
    _pins: Tuple[Pin, ...]
    __board: Optional[Arduino] = None
    __pins: Optional[Tuple[Pin, ...]] = None
    __token: Optional[str] = None

    def connect(self) -> None:
        if self.__board is not None and self.__pins is not None:
            raise ComponentAlreadyRegisteredWithArduinoError(
                "Device is already registered to an Arduino"
            )
        self.__token = uuid.uuid4().hex
        self.__board = self._board
        self.__pins = self._pins
        self.__board.register_component(self.__token, self.__pins)
        self._setup()

    def disconnect(self) -> None:
        if self.__token is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        self._board.deregister_component(self.__token)
        self.__token = None

    def set_pins(self, *pins: Pin) -> None:
        self._pins = pins

    def set_board(self, board: Arduino) -> None:
        self._board = board

    def _pin_mode(self, pin_no: int, mode: PinMode) -> None:
        if self.__board is None or self.__pins is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        self.__board.pin_mode(pin_no, mode, self.__token)

    def _digital_read(self, pin_no: int) -> PinState:
        if self.__board is None or self.__pins is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        return self.__board.digital_read(pin_no, self.__token)

    def _digital_write(self, pin_no: int, state: PinState) -> None:
        if self.__board is None or self.__pins is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        self.__board.digital_write(pin_no, state, self.__token)

    def _analog_read(self, pin_no: int) -> int:
        if self.__board is None or self.__pins is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        return self.__board.analog_read(pin_no, self.__token)

    def _analog_write(self, pin_no: int, value: int) -> None:
        if self.__board is None or self.__pins is None:
            raise ComponentNotRegisteredWithArduinoError(
                "Device must be registered to an Arduino"
            )
        self.__board.analog_write(pin_no, value, self.__token)

    @abstractmethod
    def _setup(self) -> None:
        """Implement this method to set the initial pin mode and state.
        Always explicitly set the state you want. Do not rely on
        Arduino defaults, as this component may be being "hotswapped",
        so may be in an unexpected state.
        """
