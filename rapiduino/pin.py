from dataclasses import dataclass


@dataclass(frozen=True)
class Pin:
    pin_id: int
    is_pwm: int = False
    is_analog: bool = False
