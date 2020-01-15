from enum import Enum

from Types.custom_types import Location
from typing import Tuple, Dict

from pykka import ActorRef


class Message:
    pass


class ObjectMessage:
    def __init__(self, body: object):
        self.body = body


class InstructionRequest:
    def __init__(self, location):
        self.location = location


class Action(Enum):
    GIVE = 0
    TAKE = 1
    GIVETAKE = 2


class InteractWithMessage:

    def __init__(self, location: Location, action: Action, wait=False):
        self.location = location
        self.action = action
        self.wait = wait


class PlotMessage:
    def __init__(self, requesting_actor: ActorRef):
        self.requesting_actor = requesting_actor


class PlotDoneMessage:
    pass


class RegistrationMessage:
    def __init__(self, actor_ref: ActorRef, location: Location, attributes: Dict[str, object] = {}):
        self.actorRef = actor_ref
        self.location = location
        self.attributes = attributes


class RequestOrderMessage:
    def __init__(self, actor_ref: ActorRef):
        self.actor_ref = actor_ref


class WaitMessage:
    pass


class ReminderMessage:
    pass
