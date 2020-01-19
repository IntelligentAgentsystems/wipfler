from enum import Enum
from typing import Dict

from pykka import ActorRef

from Sheets.sheet_order import SheetOrder
from Types.custom_types import Location


# class Message:
#     pass
#
#
# class ObjectMessage:
#     def __init__(self, body: object):
#         self.body = body


class InstructionRequest:
    def __init__(self, actor_ref: ActorRef):
        self.actor_ref = actor_ref


class Action(Enum):
    GIVE = 0
    TAKE = 1
    GIVETAKE = 2


class InteractWithMessage:

    def __init__(self, location: Location, action: Action, actor_ref: ActorRef = None):
        self.location = location
        self.action = action
        self.actor_ref = actor_ref


# class PlotMessage:
#     def __init__(self, requesting_actor: ActorRef):
#         self.requesting_actor = requesting_actor
#
#
# class PlotDoneMessage:
#     pass

class PerformActionMessage:
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


#
# class WaitMessage:
#     pass

class SheetOrderMessage:
    def __init__(self, order: SheetOrder):
        self.order = order


class ReminderMessage:
    pass
