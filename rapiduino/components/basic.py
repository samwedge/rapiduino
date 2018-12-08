from rapiduino.pin import ComponentPin
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.components.base import BaseComponent


class LED(BaseComponent):

    def __init__(self):
        self._pins = (
            ComponentPin(0),
        )

    def _setup(self):
        self._pin_mode(self.pins[0].bound_pin_num, OUTPUT)
        self._digital_write(self.pins[0].bound_pin_num, LOW)

    def turn_on(self):
        self._digital_write(self.pins[0].bound_pin_num, HIGH)

    def turn_off(self):
        self._digital_write(self.pins[0].bound_pin_num, LOW)

    def toggle(self):
        state = self._digital_read(self.pins[0].bound_pin_num)
        if state == HIGH:
            self._digital_write(self.pins[0].bound_pin_num, LOW)
        elif state == LOW:
            self._digital_write(self.pins[0].bound_pin_num, HIGH)


class DimmableLED(LED):
    def __init__(self):
        super(DimmableLED, self).__init__()

        self._pins = (
            ComponentPin(0, pwm=True),
        )

    def set_brightness(self, brightness):
        self._analog_write(self.pins[0].bound_pin_num, brightness)
