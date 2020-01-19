from enum import Enum
from typing import Dict

from pykka import ActorRef

from Sheets.sheet_order import SheetOrder
from Types.custom_types import Location


class InstructionRequest:
    def __init__(self, actor_ref: ActorRef):
        self.actor_ref = actor_ref


class Action(Enum):
    GIVE = 0
    TAKE = 1


class BaseInteractionMessage:

    def __init__(self, location: Location):
        self.location = location


class InteractWithMessage(BaseInteractionMessage):

    def __init__(self, location: Location, action: Action):
        super().__init__(location)
        self.action = action


class InteractWithPlotterMessage(BaseInteractionMessage):

    def __init__(self, location: Location, actor_ref: ActorRef):
        super().__init__(location)
        self.actor_ref = actor_ref


class InteractWithConveyorMessage(BaseInteractionMessage):

    def __init__(self, location: Location, actor_ref: ActorRef):
        super().__init__(location)
        self.actor_ref = actor_ref


class TurnTowardsMessage(BaseInteractionMessage):
    pass


class PlotMessage:
    pass


class RegistrationMessage:
    def __init__(self, actor_ref: ActorRef, location: Location, attributes: Dict[str, object] = {}):
        self.actorRef = actor_ref
        self.location = location
        self.attributes = attributes


class UnRegistrationMessage:
    def __init__(self, actor_ref: ActorRef):
        self.actorRef = actor_ref


class RequestOrderMessage:
    def __init__(self, actor_ref: ActorRef):
        self.actor_ref = actor_ref


class SheetOrderMessage:
    def __init__(self, order: SheetOrder):
        self.order = order
