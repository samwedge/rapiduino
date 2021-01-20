from typing import Tuple

from rapiduino.boards.arduino import Arduino
from rapiduino.components import BaseComponent
from rapiduino.globals.common import HIGH, LOW, OUTPUT


class LED(BaseComponent):
    def __init__(self, board: Arduino, anode_pin: int) -> None:
        self.board = board
        self.anode_pin = anode_pin
        self._register_component(board, (anode_pin,))
        board.pin_mode(self.anode_pin, OUTPUT)
        self.turn_off()

    def is_on(self) -> bool:
        state = self.board.digital_read(self.anode_pin)
        if state == HIGH:
            return True
        else:
            return False

    def turn_on(self) -> None:
        self.board.digital_write(self.anode_pin, HIGH)

    def turn_off(self) -> None:
        self.board.digital_write(self.anode_pin, LOW)

    def toggle(self) -> None:
        self.turn_off() if self.is_on() else self.turn_on()

    def _register_component(self, board: Arduino, pins: Tuple[int]) -> None:
        board.register_component(self, pins)
