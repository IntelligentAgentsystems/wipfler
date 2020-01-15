from Types.custom_types import Location
from typing import Tuple, Dict

from Sheets.sheet import Sheet
from constants import Direction

class FunctionalUnit:
    """
    Basic functionality and attributes for Functional units
    """

    def __init__(self, unit_system: 'UnitSystem', location: Location):
        """
        :param location: (x, y) values of unit
        """
        self.location: Location[int, int] = location
        self.unit_sytem = unit_system

    def on_receive(self, sheet: Sheet, direction: Direction):
        pass

    def on_take(self, direction: Direction) -> Sheet:
        pass


class UnitOccupiedError(Exception):

    def __init__(self, receiver: FunctionalUnit):
        super().__init__(f'Reciever {receiver.__class__.__name__} at {receiver} already has Sheet\n')


class NoSheetError(Exception):

    def __init__(self, sender: FunctionalUnit):
        super().__init__(f'{sender.__class__.__name__} at {sender.location} has no Sheet')
