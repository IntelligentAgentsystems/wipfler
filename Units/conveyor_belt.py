import time

import util
from Units.functional_unit import *


class ConveyorBelt(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Tuple[int, int],
                 initial_direction: Direction = Direction.North,
                 turn_duration_seconds: float = 2):
        super().__init__(unit_system, location)
        self.sheet = None
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

    def on_receive(self, sheet: Sheet, direction: Direction):
        if self.direction != util.opposite_direction(direction):
            raise ConveyorFacingAwayError(self, direction)
        if self.sheet is not None:
            raise UnitOccupiedError(self)
        self.sheet = sheet

    def on_take(self, direction: Direction) -> Sheet:
        if self.is_turning():
            raise ConveyorTurningError(self)
        if self.direction != util.opposite_direction(direction):
            raise ConveyorFacingAwayError(self, direction)
        tmp = self.sheet
        self.sheet = None
        return tmp

    def take(self):
        if self.sheet is not None:
            raise UnitOccupiedError(self)
        loc_of_other_unit = util.move_location(self.location, self.direction)
        sheet = self.unit_system.take_from_unit_at(loc_of_other_unit, self.location)
        self.sheet = sheet

    def put(self):
        if self.is_turning():
            raise ConveyorTurningError(self)
        loc_of_other_unit = util.move_location(self.location, self.direction)
        self.unit_sytem.drop_to_unit_at(self.sheet, loc_of_other_unit, self.location)
        self.sheet = None


class ConveyorFacingAwayError(Exception):
    def __init__(self, conveyor: ConveyorBelt, sheet_direction: Direction):
        super().__init__(f'{conveyor.__class__.__name__} at {conveyor.location} '
                         f'faces {conveyor.direction}, but recieving Sheet from {sheet_direction}')


class ConveyorTurningError(Exception):
    def __init__(self, conveyor: ConveyorBelt):
        super().__init__(f'{conveyor.location} is still turning')
