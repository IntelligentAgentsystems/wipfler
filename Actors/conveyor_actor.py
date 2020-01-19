import logging

from pykka import ActorRef, ActorRegistry

import constants as const
import util
from Actors.operator_actor import OperatorActor
from Actors.reminder_actor import ReminderActor
from Actors.supervisor_actor import SupervisorActor
from Messages import InteractWithMessage, Action, PerformActionMessage, ReminderMessage, InstructionRequest
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

    def _handle_interact_with_message(self, message: InteractWithMessage):
        location = message.location
        self.turn_towards(location)
        if message.action == Action.GIVE:
            self.conveyor.put()
            logging.log(logging.DEBUG,
                        f'CVB: Conveyor at {self.conveyor.location} gave sheet to Actor at {message.location}')
        elif message.action == Action.TAKE:
            self.conveyor.take()
            logging.log(logging.DEBUG,
                        f'CVB: Conveyor at {self.conveyor.location} took sheet from Actor at {message.location}')
        else:  # message.action == Action.GIVETAKE
            other_actor = message.actor_ref
            self.conveyor.put()
            other_actor.ask(PerformActionMessage(), block=True)
            self.conveyor.take()

    def on_receive(self, message):
        if isinstance(message, InteractWithMessage):
            self._handle_interact_with_message(message)
        self.supervisor.tell(InstructionRequest(self.actor_ref))



    def turn_towards(self, location: Location):
        target_direction = util.relative_direction_of(location, self.conveyor.location)
        while self.conveyor.direction != target_direction:
            self.conveyor.turn_clockwise()
            while self.conveyor.is_turning():
                pass
        logging.log(logging.DEBUG, f'CVB: Conveyor at {self.conveyor.location} now facing {self.conveyor.direction}')
