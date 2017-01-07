from rapiduino.base import Pin
from rapiduino.communication import Commands


class ArduinoBase(object):

    def __init__(self):
        self.commands = Commands()

    def digital_read(self, pin):
        return self.pins[pin].pin_state

    def digital_write(self, pin, value):
        self.pins[pin].pin_state = value

    def analog_read(self, pin):
        raise NotImplementedError()

    def analog_write(self, pin, value):
        raise NotImplementedError()

    def pin_mode(self, pin_no, mode):
        self.pins[pin_no].pin_mode = mode

    @property
    def pins(self):
        return self._pins


class ArduinoUno(ArduinoBase):

    def __init__(self):
        super(ArduinoUno, self).__init__()
        self._pins = (
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
        )
