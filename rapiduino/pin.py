from typing import Tuple, Optional, TYPE_CHECKING, Union

from rapiduino.exceptions import AlreadyBoundPinError
from rapiduino.globals.common import INPUT, LOW

if TYPE_CHECKING:
    from rapiduino.devices import Arduino
    from rapiduino.components.base import BaseComponent


class Pin:

    def __init__(self, pin_id: int, pwm: bool = False, analog: bool = False) -> None:
        self._pin_mode = INPUT
        self._pwm = pwm
        self._analog = analog
        self._pin_state = LOW
        self._pin_id = pin_id
        self._bound_to = None  # type: Optional[Tuple[Union['Arduino', 'BaseComponent'], int]]

    @property
    def pin_id(self) -> int:
        return self._pin_id

    @property
    def is_pwm(self) -> int:
        return self._pwm

    @property
    def is_analog(self) -> bool:
        return self._analog

    @property
    def bound_to(self) -> Optional[Tuple[Union['Arduino', 'BaseComponent'], int]]:
        return self._bound_to

    @property
    def bound_instance(self) -> Optional[Union['Arduino', 'BaseComponent']]:
        if self._bound_to is None:
            return None
        else:
            return self._bound_to[0]

    @property
    def bound_pin_num(self) -> Optional[int]:
        if self._bound_to is None:
            return None
        else:
            return self._bound_to[1]

    def bind(self, instance: Union['Arduino', 'BaseComponent'], pin_no: int) -> None:
        if self._bound_to is not None:
            raise AlreadyBoundPinError('Cannot bind pin - already bound')
        self._bound_to = (instance, pin_no)

    def unbind(self) -> None:
        self._bound_to = None

    def is_bound(self) -> bool:
        return self.bound_to is not None
