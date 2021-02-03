from __future__ import annotations

from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.components import BaseComponent
from rapiduino.globals.common import HIGH, LOW, OUTPUT


class LED(BaseComponent):
    @classmethod
    def create(cls, board: Arduino, anode_pin_no: int) -> LED:
        pins = (Pin(anode_pin_no),)
        return cls(board, pins)

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
