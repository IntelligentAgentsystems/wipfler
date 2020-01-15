from typing import Tuple

from Sheets.sheet import Sheet
from Units.functional_unit import FunctionalUnit
from constants import Direction


class OutputPaperStack(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Tuple[int, int]):
        super().__init__(unit_system, location)
        self.received_sheets = []

    def on_receive(self, sheet: Sheet, direction: Direction):
        self.received_sheets.append(sheet)
