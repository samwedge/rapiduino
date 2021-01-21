from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.components import BaseComponent
from rapiduino.globals.common import HIGH, LOW, OUTPUT


class LED(BaseComponent):
    def __init__(self, board: Arduino, anode_pin_no: int) -> None:
        self.board = board
        self.pin_no = anode_pin_no
        self._register_component(board, (Pin(anode_pin_no),))
        board.pin_mode(self.pin_no, OUTPUT)
        self.turn_off()

    def is_on(self) -> bool:
        state = self.board.digital_read(self.pin_no)
        return state == HIGH

    def turn_on(self) -> None:
        self.board.digital_write(self.pin_no, HIGH)

    def turn_off(self) -> None:
        self.board.digital_write(self.pin_no, LOW)

    def toggle(self) -> None:
        self.turn_off() if self.is_on() else self.turn_on()
