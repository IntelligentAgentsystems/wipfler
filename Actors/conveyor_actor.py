import logging

from pykka import ActorRef, ActorRegistry

import constants as const
import util
from Actors.operator_actor import OperatorActor
from Actors.supervisor_actor import SupervisorActor
from Messages import InteractWithMessage, Action, PlotMessage, InstructionRequest, \
    InteractWithPlotterMessage, InteractWithConveyorMessage, TurnTowardsMessage, BaseInteractionMessage
from Types.custom_types import Location
from Units.conveyor_belt import ConveyorBelt


class ConveyorActor(OperatorActor):

    def __init__(self, conveyor: ConveyorBelt):
        super().__init__()
        self.conveyor = conveyor
        self.supervisor: ActorRef = None
        self.reminder_actor: ActorRef = None
        self.reminder_interval_seconds = .5

    def on_start(self):
        self._register(self.conveyor.location, {const.UNIT_TYPE_KEY: const.CONVEYOR_TYPE})
        self.supervisor = ActorRegistry().get_by_class(SupervisorActor)[0]

    def _handle_interact_with_plotter_message(self, message: InteractWithPlotterMessage):
        other_actor = message.actor_ref
        self.conveyor.put()
        other_actor.ask(PlotMessage(), block=True)
        self.conveyor.take()

    def _handle_interact_with_conveyor_message(self, message: InteractWithConveyorMessage):
        logging.log(logging.DEBUG,
                    f'CVB: Conveyor at {self.conveyor.location} gives sheet to Covneyor at {message.location}')
        other_actor = message.actor_ref
        other_actor.ask(TurnTowardsMessage(self.conveyor.location), block=True)
        self.conveyor.put()
        self.supervisor.tell(InstructionRequest(other_actor))

    def _handle_turn_towards_message(self, message: TurnTowardsMessage):
        location = message.location
        self.turn_towards(location)
        return

    def _handle_interact_with_message(self, message: InteractWithMessage):
        if message.action == Action.GIVE:
            self.conveyor.put()
            logging.log(logging.DEBUG,
                        f'CVB: Conveyor at {self.conveyor.location} gave sheet to Actor at {message.location}')
        elif message.action == Action.TAKE:
            self.conveyor.take()
            logging.log(logging.DEBUG,
                        f'CVB: Conveyor at {self.conveyor.location} took sheet from Actor at {message.location}')

    def on_receive(self, message):
        if isinstance(message, BaseInteractionMessage):
            location = message.location
            self.turn_towards(location)
            if isinstance(message, InteractWithPlotterMessage):
                self._handle_interact_with_plotter_message(message)
            elif isinstance(message, InteractWithConveyorMessage):
                self._handle_interact_with_conveyor_message(message)
            elif isinstance(message, InteractWithMessage):
                self._handle_interact_with_message(message)
            elif isinstance(message, TurnTowardsMessage):
                self._handle_turn_towards_message(message)
            # ask for further instructions
            if not isinstance(message, TurnTowardsMessage):
                self.supervisor.tell(InstructionRequest(self.actor_ref))

    def turn_towards(self, location: Location):
        target_direction = util.relative_direction_of(location, self.conveyor.location)
        steps_over_cw = 0
        tmp_dir = self.conveyor.direction
        while tmp_dir != target_direction:
            steps_over_cw += 1
            tmp_dir = const.Direction((tmp_dir.value + 1) % 4)
        turn_cmd = (self.conveyor.turn_clockwise, self.conveyor.turn_counter_clockwise)[steps_over_cw > 2]
        while self.conveyor.direction != target_direction:
            turn_cmd()
            while self.conveyor.is_turning():
                pass
        logging.log(logging.DEBUG, f'CVB: Conveyor at {self.conveyor.location} now facing {self.conveyor.direction}')
