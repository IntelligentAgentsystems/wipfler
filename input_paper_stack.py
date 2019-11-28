from typing import Tuple

from functional_unit import FunctionalUnit
from sheet import Sheet


class InputPaperStack(FunctionalUnit):

    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)

    def give_sheet_to(self, other_unit: FunctionalUnit):
        self.sheet = Sheet()
        super().give_sheet_to(other_unit)
