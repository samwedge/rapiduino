from rapiduino.base import Pin


class ArduinoBase(object):
    pass


class ArduinoUno(ArduinoBase):

    def __init__(self):
        self._pins = [
            Pin(0),
            Pin(1),
            Pin(2),
            Pin(3, pwm=True),
            Pin(4),
            Pin(5, pwm=True),
            Pin(6, pwm=True),
            Pin(7),
            Pin(8),
            Pin(9, pwm=True),
            Pin(10, pwm=True),
            Pin(11, pwm=True),
            Pin(12),
            Pin(13),
            Pin(14, analog=True),
            Pin(15, analog=True),
            Pin(16, analog=True),
            Pin(17, analog=True),
            Pin(18, analog=True),
            Pin(19, analog=True),
        ]

    @property
    def pins(self):
        return self._pins[:]
