from rapiduino.pin import ComponentPin
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.components.base import BaseComponent


class LED(BaseComponent):

    def __init__(self):
        super(LED, self).__init__()

        self._pins = (
            ComponentPin(0),
        )

    def setup(self):
        self._pin_mode(self.pins[0].bound_pin, OUTPUT)
        self._digital_write(self.pins[0].bound_pin, LOW)

    def turn_on(self):
        self._digital_write(self.pins[0].bound_pin, HIGH)

    def turn_off(self):
        self._digital_write(self.pins[0].bound_pin, LOW)

    def toggle(self):
        state = self._digital_read(self.pins[0].bound_pin)
        if state == HIGH:
            self._digital_write(self.pins[0].bound_pin, LOW)
        elif state == LOW:
            self._digital_write(self.pins[0].bound_pin, HIGH)


class DimmableLED(LED):
    def __init__(self):
        super(DimmableLED, self).__init__()

        self._pins = (
            ComponentPin(0, pwm=True),
        )

    def set_brightness(self, brightness):
        self._analog_write(self.pins[0].bound_pin, brightness)
