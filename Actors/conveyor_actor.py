from Actors.operator_actor import OperatorActor
from Messages import InteractWithMessage, Action
from Types.custom_types import Location
from Units.conveyor_belt import ConveyorBelt
from Units.functional_unit import unit_at, FunctionalUnit
import constants as const
from Units.plotter import Plotter


class ConveyorActor(OperatorActor):

    def __init__(self, conveyor: ConveyorBelt):
        super().__init__(conveyor)
        self.is_waiting = False
        self.backlog = []

    def on_start(self):
        self._shout_out({const.UNIT_TYPE_KEY: const.CONVEYOR_TYPE})

    def on_receive(self, message):
        if self.is_waiting:
            self.backlog.append(message)
        if isinstance(message, InteractWithMessage):
            other_unit = unit_at(message.location)
            self.turn_towards(other_unit)
            if message.action == Action.GIVE:
                self.functional_unit.give_sheet_to(other_unit)
                if message.wait:
                    self.is_waiting = True
            elif message.action == Action.TAKE:
                other_unit.give_sheet_to(self.functional_unit)
            else: # message.action == Action.GIVETAKE
                self.functional_unit.give_sheet_to(other_unit)
                other
                other_unit.give_sheet_to(self.functional_unit)


    def turn_towards(self, other_unit: FunctionalUnit):
        while self.functional_unit.relative_direction_of_unit(other_unit) != self.functional_unit.direction:
            self.functional_unit.turn_clockwise()
            while self.functional_unit.is_turning():
                pass
