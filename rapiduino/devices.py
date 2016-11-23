from rapiduino.base import Pin


class ArduinoBase(object):
    pass


class ArduinoUno(ArduinoBase):

    def __init__(self):
        self._pins = [
            Pin(),
            Pin(),
            Pin(),
            Pin(is_pwm=True),
            Pin(),
            Pin(is_pwm=True),
            Pin(is_pwm=True),
            Pin(),
            Pin(),
            Pin(is_pwm=True),
            Pin(is_pwm=True),
            Pin(is_pwm=True),
            Pin(),
            Pin(),
            Pin(is_analog=True),
            Pin(is_analog=True),
            Pin(is_analog=True),
            Pin(is_analog=True),
            Pin(is_analog=True),
            Pin(is_analog=True),
        ]

    @property
    def pins(self):
        return self._pins[:]
