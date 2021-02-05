from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.components.base import BaseComponent
from rapiduino.globals.common import HIGH, LOW, OUTPUT


class LED(BaseComponent):
    def __init__(self, board: Arduino, anode_pin_no: int) -> None:
        self.set_pins(Pin(pin_id=anode_pin_no))
        self.set_board(board)
        self.connect()

    def _setup(self) -> None:
        self._pin_mode(self._pins[0].pin_id, OUTPUT)
        self.turn_off()

    def is_on(self) -> bool:
        state = self._digital_read(self._pins[0].pin_id)
        return state == HIGH

    def turn_on(self) -> None:
        self._digital_write(self._pins[0].pin_id, HIGH)

    def turn_off(self) -> None:
        self._digital_write(self._pins[0].pin_id, LOW)

    def toggle(self) -> None:
        self.turn_off() if self.is_on() else self.turn_on()
