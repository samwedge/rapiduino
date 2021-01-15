from rapiduino.pin import Pin
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.components.base import BaseComponent


class TxRx(BaseComponent):
    def __init__(self) -> None:
        self._pins = (
            Pin(0),
            Pin(1),
        )


class LED(BaseComponent):
    def __init__(self) -> None:
        self._pins = (Pin(0),)

    def _setup(self) -> None:
        self._pin_mode(self.pins[0].bound_pin_num, OUTPUT)  # type: ignore
        self._digital_write(self.pins[0].bound_pin_num, LOW)  # type: ignore

    def turn_on(self) -> None:
        self._digital_write(self.pins[0].bound_pin_num, HIGH)  # type: ignore

    def turn_off(self) -> None:
        self._digital_write(self.pins[0].bound_pin_num, LOW)  # type: ignore

    def toggle(self) -> None:
        state = self._digital_read(self.pins[0].bound_pin_num)  # type: ignore
        if state == HIGH:
            self._digital_write(self.pins[0].bound_pin_num, LOW)  # type: ignore
        elif state == LOW:
            self._digital_write(self.pins[0].bound_pin_num, HIGH)  # type: ignore


class DimmableLED(LED):
    def __init__(self) -> None:
        super(DimmableLED, self).__init__()

        self._pins = (Pin(0, pwm=True),)

    def set_brightness(self, brightness: int) -> None:
        self._analog_write(self.pins[0].bound_pin_num, brightness)  # type: ignore
