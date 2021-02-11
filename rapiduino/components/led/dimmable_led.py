from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin
from rapiduino.components.base_component import BaseComponent
from rapiduino.globals.common import OUTPUT


class DimmableLED(BaseComponent):
    def __init__(self, board: Arduino, pin_no: int) -> None:
        self._pin_no = pin_no
        self._brightness = 255
        self._current_state = 0
        self.set_pins(Pin(pin_id=pin_no, is_pwm=True))
        self.set_board(board)
        self.connect()

    def _setup(self) -> None:
        self._pin_mode(self._pin_no, OUTPUT)
        self.turn_off()

    def is_on(self) -> bool:
        return self._current_state > 0

    def turn_on(self) -> None:
        self._analog_write(self._pin_no, self._brightness)
        self._current_state = self._brightness

    def turn_off(self) -> None:
        self._analog_write(self._pin_no, 0)
        self._current_state = 0

    def toggle(self) -> None:
        self.turn_off() if self.is_on() else self.turn_on()

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: int) -> None:
        self._brightness = brightness
        if self.is_on():
            self.turn_on()
