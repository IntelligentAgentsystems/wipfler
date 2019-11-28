from Units.functional_unit import *
from enum import Enum
from typing import Tuple
import time


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class ConveyorBelt(FunctionalUnit):

    def __init__(self, location: Tuple[int, int], initial_direction: Direction = Direction.North,
                 turn_duration_seconds: float = 2):
        super().__init__(location)
        self.direction: Direction = initial_direction
        self.turn_duration_seconds = turn_duration_seconds
        self.last_turn_start_seconds = 0

    def is_turning(self) -> bool:
        return time.time() < self.last_turn_start_seconds + self.turn_duration_seconds

    def turn_clockwise(self):
        if self.is_turning():
            raise ConveyorTurningError(self)
        self.last_turn_start_seconds = time.time()
        self.direction = Direction((self.direction.value + 1) % 4)

    def turn_counter_clockwise(self):
        if self.is_turning():
            raise ConveyorTurningError(self)
        self.last_turn_start_seconds = time.time()
        self.direction = Direction((self.direction.value + 3) % 4)

    def relative_direction_of_unit(self, other_unit: FunctionalUnit) -> Direction:
        location_diff = (other_unit.location[0] - self.location[0], other_unit.location[1] - self.location[1])
        if location_diff[1] < 0:
            return Direction.North
        if location_diff[1] > 0:
            return Direction.South
        elif location_diff[0] < 0:
            return Direction.West
        else:
            return Direction.East

    def give_sheet_to(self, other_unit: FunctionalUnit):
        if self.direction != self.relative_direction_of_unit(other_unit):
            raise GivingConveyorFacingAwayError(giving_conveyor=self, recieving_unit=other_unit)
        super().give_sheet_to(other_unit)

    def receive_sheet_from(self, other_unit: 'FunctionalUnit'):
        if self.relative_direction_of_unit(other_unit) != self.direction:
            raise ReceivingConveyorFacingAwayError(giving_unit=other_unit, recieving_conveyor=self)
        if self.is_turning():
            raise ConveyorTurningError(self)
        super().receive_sheet_from(other_unit)


class GivingConveyorFacingAwayError(Exception):
    def __init__(self, giving_conveyor: ConveyorBelt, recieving_unit: FunctionalUnit):
        super().__init__(f'{ConveyorBelt.__class__.__name__} at {giving_conveyor.location} '
                         f'faces {giving_conveyor.direction}, but recieving unit at {recieving_unit.location} '
                         f'is {giving_conveyor.relative_direction_of_unit(recieving_unit)}')


class ReceivingConveyorFacingAwayError(Exception):
    def __init__(self, giving_unit: FunctionalUnit, recieving_conveyor: ConveyorBelt):
        super().__init__(f'{ConveyorBelt.__class__.__name__} at {recieving_conveyor.location} '
                         f'faces {recieving_conveyor.direction}, but recieves sheet'
                         f'from {recieving_conveyor.relative_direction_of_unit(giving_unit)} ({giving_unit.location})')


class ConveyorTurningError(Exception):
    def __init__(self, conveyor: ConveyorBelt):
        super().__init__(f'{conveyor.location} is still turning')
