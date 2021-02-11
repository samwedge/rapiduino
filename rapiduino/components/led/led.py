from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.components.base_component import BaseComponent
from rapiduino.globals.common import HIGH, LOW, OUTPUT


class LED(BaseComponent):
    def __init__(self, board: Arduino, pin_no: int) -> None:
        self._pin_no = pin_no
        self.set_pins(Pin(pin_id=pin_no))
        self.set_board(board)
        self.connect()

    def _setup(self) -> None:
        self._pin_mode(self._pin_no, OUTPUT)
        self.turn_off()

    def is_on(self) -> bool:
        state = self._digital_read(self._pin_no)
        return state == HIGH

    def turn_on(self) -> None:
        self._digital_write(self._pin_no, HIGH)

    def turn_off(self) -> None:
        self._digital_write(self._pin_no, LOW)

    def toggle(self) -> None:
        self.turn_off() if self.is_on() else self.turn_on()
