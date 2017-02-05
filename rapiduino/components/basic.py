from rapiduino.pin import Pin
from rapiduino.globals.common import HIGH, LOW, OUTPUT
from rapiduino.components.base import BaseComponent


class LED(BaseComponent):

    def __init__(self):
        super(LED, self).__init__()

        self._pins = (
            Pin(0),
        )

    def setup(self):
        self.bound_device.pin_mode(self.pins[0].bound_pin, OUTPUT)
        self.bound_device.digital_write(self.pins[0].bound_pin, LOW)

    def turn_on(self):
        self.bound_device.digital_write(self.pins[0].bound_pin, HIGH)

    def turn_off(self):
        self.bound_device.digital_write(self.pins[0].bound_pin, LOW)

    def toggle(self):
        state = self.bound_device.digital_read(self.pins[0].bound_pin)
        if state == HIGH:
            self.bound_device.digital_write(self.pins[0].bound_pin, LOW)
        else:
            self.bound_device.digital_write(self.pins[0].bound_pin, HIGH)
