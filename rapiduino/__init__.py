__version__ = "1.0.0"

from dataclasses import dataclass


@dataclass
class GlobalParameter:
    name: str
    value: int
