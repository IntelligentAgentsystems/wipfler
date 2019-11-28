from typing import Tuple

from sheet import Sheet


class FunctionalUnit:
    """
    Basic functionality and attributes for Functional units
    """

    def __init__(self, location: Tuple[int, int]):
        """
        :param location: (x, y) values of unit
        """
        self.location: Tuple[int, int] = location
        self.sheet: Sheet = None

    def distance_to(self, other_unit: 'FunctionalUnit') -> int:
        return abs(self.location[0] - other_unit.location[0]) + abs(self.location[1] - other_unit.location[1])

    def is_occupied(self) -> bool:
        return self.sheet is not None

    def give_sheet_to(self, other_unit: 'FunctionalUnit'):
        if self.sheet is None:
            raise NoSheetError(sender=self, reciever=other_unit)
        if self.distance_to(other_unit) > 1:
            raise UnitOutOfRangeError(sender=self, receiver=other_unit)
        other_unit.receive_sheet_from(self)
        self.sheet = None

    def receive_sheet_from(self, other_unit: 'FunctionalUnit'):
        if self.is_occupied():
            raise UnitOccupiedError(sender=other_unit, receiver=self)
        other_unit.sheet = self.sheet


class UnitOccupiedError(Exception):

    def __init__(self, sender: FunctionalUnit, receiver: FunctionalUnit):
        super().__init__(
            f'Reciever {receiver.__class__.__name__} at {receiver} is busy\n'
            f'Sender {sender.__class__.__name__} at {sender.location}')


class UnitOutOfRangeError(Exception):

    def __init__(self, sender: FunctionalUnit, receiver: FunctionalUnit):
        super().__init__(
            f'Reciever {receiver.__class__.__name__} at {receiver.location} is too far away\n'
            f'Sender {sender.__class__.__name__} at {sender.location}'
            f'Distance is {sender.distance_to(receiver)}')


class NoSheetError(Exception):

    def __init__(self, sender: FunctionalUnit, reciever:FunctionalUnit):
        super().__init__(f'{sender.__class__.__name__} at {sender.location} has no sheet to hand to'
              f'{reciever.__class__.__name__} at {reciever.location}')
