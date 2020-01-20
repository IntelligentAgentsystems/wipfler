import time
from threading import Thread

import cv2
from skimage import transform

import util
from Units.functional_unit import *

model = cv2.imread(r'graphics\conveyor_empty.png', cv2.IMREAD_COLOR).astype(float)
model_sheet = cv2.imread(r'graphics\conveyor_sheet.png', cv2.IMREAD_COLOR).astype(float)
direction_to_rotation = {
    Direction.North: 0,
    Direction.East: 270,
    Direction.South: 180,
    Direction.West: 90
}


class ConveyorBelt(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Location,
                 initial_direction: Direction = Direction.North,
                 turn_duration_seconds: float = 2):
        super().__init__(unit_system, location, model)
        self.sheet = None
        self.unit_system = unit_system
        self.direction: Direction = initial_direction
        self.turn_duration_seconds = turn_duration_seconds
        self.last_turn_start_seconds = 0

    def is_turning(self) -> bool:
        return time.time() < self.last_turn_start_seconds + self.turn_duration_seconds

    def do_animation(self, image, init_direction, offset):
        rotation_degrees = direction_to_rotation[init_direction]
        steps = 2
        delay = self.turn_duration_seconds / steps
        rotation_part = int(offset / steps)
        for i in range(1, steps + 1):
            self.update_system_image(transform.rotate(image, rotation_degrees + i * rotation_part))
            time.sleep(delay)

    def turn_clockwise(self):
        if self.is_turning():
            raise ConveyorTurningError(self)
        self.last_turn_start_seconds = time.time()
        Thread(target=self.do_animation,
               args=[(model, model_sheet)[self.sheet is not None], self.direction, -90]).start()
        self.direction = Direction((self.direction.value + 1) % 4)

    def turn_counter_clockwise(self):
        if self.is_turning():
            raise ConveyorTurningError(self)
        self.last_turn_start_seconds = time.time()
        Thread(target=self.do_animation, args=[(model, model_sheet)[self.sheet is not None], self.direction, 90]).start()
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
        if self.sheet is None:
            raise NoSheetToPutError(self)
        if self.is_turning():
            raise ConveyorTurningError(self)
        loc_of_other_unit = util.move_location(self.location, self.direction)
        self.unit_sytem.drop_to_unit_at(self.sheet, loc_of_other_unit, self.location)
        self.sheet = None
        self.update_system_image(transform.rotate(model, direction_to_rotation[self.direction]))


class ConveyorFacingAwayError(Exception):
    def __init__(self, conveyor: ConveyorBelt, sheet_direction: Direction):
        super().__init__(f'{conveyor.__class__.__name__} at {conveyor.location} '
                         f'faces {conveyor.direction}, but recieving Sheet from {sheet_direction}')


class ConveyorTurningError(Exception):
    def __init__(self, conveyor: ConveyorBelt):
        super().__init__(f'{conveyor.location} is still turning')


class NoSheetToPutError(Exception):
    def __init__(self, conveyor: ConveyorBelt):
        super().__init__(f'{conveyor.location} has no sheet to put')
