from typing import Dict

import util
from Sheets.abstract_sheet import Color
from Sheets.sheet import Sheet
from Types.custom_types import Location
from Units.conveyor_belt import ConveyorBelt
from Units.functional_unit import FunctionalUnit
from Units.input_paper_stack import InputPaperStack
from Units.output_paper_stack import OutputPaperStack
from Units.plotter import Plotter


class UnitSystem:
    def __init__(self):
        self.unit_locations: Dict[Location, FunctionalUnit] = {}

    def drop_to_unit_at(self, sheet: Sheet, location: Location, source_location: Location):
        if location not in self.unit_locations:
            raise NoUnitAtLocationError(location)
        elif util.distance(location, source_location) > 1:
            raise UnitsToFarApartError(location, source_location)
        else:
            return self.unit_locations[location].on_receive(sheet,
                                                            util.relative_direction_of(location, source_location))

    def take_from_unit_at(self, location: Location, source_location: Location) -> Sheet:
        if location not in self.unit_locations:
            raise NoUnitAtLocationError(location)
        elif util.distance(location, source_location) > 1:
            raise UnitsToFarApartError(location, source_location)
        else:
            return self.unit_locations[location].on_take(util.relative_direction_of(location, source_location))

    def create_plotter(self, location: Location, color: Color) -> Plotter:
        plt = Plotter(self, location, color)
        self.unit_locations[location] = plt
        return plt

    def create_input_paper_stack(self, location: Location) -> InputPaperStack:
        ips = InputPaperStack(self, location)
        self.unit_locations[location] = ips
        return ips

    def create_output_paper_stack(self, location: Location) -> OutputPaperStack:
        ops = OutputPaperStack(self, location)
        self.unit_locations[location] = ops
        return ops

    def create_conveyor(self, location: Location) -> ConveyorBelt:
        cvb = ConveyorBelt(self, location)
        self.unit_locations[location] = cvb
        return cvb


class NoUnitAtLocationError(Exception):

    def __init__(self, location: Location):
        super().__init__(f'UnitSystem has no Unit at {location}')


class UnitsToFarApartError(Exception):

    def __init__(self, to_location: Location, from_location: Location):
        super().__init__(f'Cannot give Sheet from {to_location} to {from_location}, because they are '
                         f'{util.distance(to_location, from_location)} distance units apart.')
