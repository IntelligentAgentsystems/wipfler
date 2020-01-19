from collections import defaultdict
from enum import Enum
from typing import Dict


class AbstractSheet:
    def __init__(self):
        self.plots: Dict[Color, int] = defaultdict(int)

    def __eq__(self, other):
        return self.plots == other.plots

    def __ne__(self, other):
        return not self.__eq__(other)


class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2
    Yellow = 3
