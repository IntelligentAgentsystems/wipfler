from typing import Tuple

from Units.functional_unit import FunctionalUnit
from Sheets.sheet import Sheet
from constants import Direction


class InputPaperStack(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Tuple[int, int]):
        super().__init__(unit_system, location)

    def on_take(self, direction: Direction) -> Sheet:
        return Sheet()
