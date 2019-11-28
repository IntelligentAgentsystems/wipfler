from typing import Tuple
from functional_unit import FunctionalUnit


class OutputPaperStack(FunctionalUnit):

    def __init__(self, location: Tuple[int, int]):
        super().__init__(location)
        self.received_sheets = []

    def receive_sheet_from(self, other_unit: FunctionalUnit):
        super().receive_sheet_from(other_unit)
        self.received_sheets.append(self.sheet)
