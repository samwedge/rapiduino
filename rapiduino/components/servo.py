from rapiduino.pin import ComponentPin
from rapiduino.components.base import BaseComponent


class Servo(BaseComponent):

    def __init__(self, angle_min=0, angle_max=180, pwm_min=0, pwm_max=1023):
        self._pins = (
            ComponentPin(0, pwm=True),
        )
        self._min_allowed_angle = 0
        self._max_allowed_angle = 180
        self._min_allowed_pwm = 0
        self._max_allowed_pwm = 1023

        self._angle_min = self._min_allowed_angle
        self._angle_max = self._max_allowed_angle
        self._pwm_min = self._min_allowed_pwm
        self._pwm_max = self._max_allowed_pwm

        self.angle_min = angle_min
        self.angle_max = angle_max
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max

    @property
    def angle_min(self):
        return self._angle_min

    @angle_min.setter
    def angle_min(self, value):
        if value < self._min_allowed_angle:
            raise ValueError('Minimum value allowed is {}'.format(self._min_allowed_angle))
        if value >= self._angle_max:
            raise ValueError('Minimum cannot be >= to the maximum')
        self._angle_min = value

    @property
    def angle_max(self):
        return self._angle_max

    @angle_max.setter
    def angle_max(self, value):
        if value > self._max_allowed_angle:
            raise ValueError('Maximium value allowed is {}'.format(self._max_allowed_angle))
        if value <= self._angle_min:
            raise ValueError('Maximum cannot be <= to the minimum')
        self._angle_max = value

    @property
    def pwm_min(self):
        return self._pwm_min

    @pwm_min.setter
    def pwm_min(self, value):
        if value < self._min_allowed_pwm:
            raise ValueError('Minimum value allowed is {}'.format(self._min_allowed_pwm))
        if value >= self._pwm_max:
            raise ValueError('Minimum cannot be >= to the maximum')
        self._pwm_min = value

    @property
    def pwm_max(self):
        return self._pwm_max

    @pwm_max.setter
    def pwm_max(self, value):
        if value > self._max_allowed_pwm:
            raise ValueError('Maximium value allowed is {}'.format(self._max_allowed_pwm))
        if value <= self._pwm_min:
            raise ValueError('Maximum cannot be <= to the minimum')
        self._pwm_max = value
