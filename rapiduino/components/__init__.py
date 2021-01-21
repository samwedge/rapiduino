import uuid
from abc import ABC
from typing import Tuple

from rapiduino.boards.arduino import Arduino
from rapiduino.boards.pins import Pin


class BaseComponent(ABC):
    def _register_component(self, board: Arduino, pins: Tuple[Pin, ...]) -> None:
        self.token = uuid.uuid4().hex
        board.register_component(self.token, pins)
