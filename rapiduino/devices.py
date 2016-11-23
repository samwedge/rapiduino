from rapiduino.base import Pin


class ArduinoBase(object):
    pass


class ArduinoUno(ArduinoBase):

    def __init__(self):
        self._pins = [
            Pin(0),
            Pin(1),
            Pin(2),
            Pin(3, is_pwm=True),
            Pin(4),
            Pin(5, is_pwm=True),
            Pin(6, is_pwm=True),
            Pin(7),
            Pin(8),
            Pin(9, is_pwm=True),
            Pin(10, is_pwm=True),
            Pin(11, is_pwm=True),
            Pin(12),
            Pin(13),
            Pin(14, is_analog=True),
            Pin(15, is_analog=True),
            Pin(16, is_analog=True),
            Pin(17, is_analog=True),
            Pin(18, is_analog=True),
            Pin(19, is_analog=True),
        ]

    @property
    def pins(self):
        return self._pins[:]
