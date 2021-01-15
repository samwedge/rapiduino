import abc
from typing import Tuple, Optional, TYPE_CHECKING

from rapiduino import GlobalParameter
from rapiduino.exceptions import NoDeviceBoundError

if TYPE_CHECKING:
    from rapiduino.devices import Arduino
    from rapiduino.pin import Pin


class BaseComponent(metaclass=abc.ABCMeta):

    _bound_device = None
    _pins = ()  # type: Tuple[Pin, ...]

    def _setup(self) -> None:
        pass

    @property
    def pins(self) -> Tuple["Pin", ...]:
        return self._pins

    @property
    def bound_device(self) -> Optional["Arduino"]:
        return self._bound_device

    def bind_to_device(self, device: "Arduino") -> None:
        self._bound_device = device
        self._setup()

    def unbind_to_device(self) -> None:
        self._bound_device = None

    def _assert_bound_to_device(self) -> None:
        if self._bound_device is None:
            raise NoDeviceBoundError()

    def _digital_read(self, pin_no: int) -> int:
        self._assert_bound_to_device()
        return self._bound_device.digital_read(pin_no, force=True)  # type: ignore

    def _digital_write(self, pin_no: int, state: GlobalParameter) -> None:
        self._assert_bound_to_device()
        self._bound_device.digital_write(pin_no, state, force=True)  # type: ignore

    def _analog_read(self, pin_no: int) -> int:
        self._assert_bound_to_device()
        return self._bound_device.analog_read(pin_no, force=True)  # type: ignore

    def _analog_write(self, pin_no: int, value: int) -> None:
        self._assert_bound_to_device()
        self._bound_device.analog_write(pin_no, value, force=True)  # type: ignore

    def _pin_mode(self, pin_no: int, mode: GlobalParameter) -> None:
        self._assert_bound_to_device()
        self._bound_device.pin_mode(pin_no, mode, force=True)  # type: ignore
