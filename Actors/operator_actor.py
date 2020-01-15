from typing import Dict, List

from Actors.supervisor_actor import SupervisorActor
from Types.custom_types import UnitRoutingMap
from pykka import ThreadingActor, ActorRegistry, ActorRef
from Messages import *

from Units.functional_unit import FunctionalUnit


class OperatorActor(ThreadingActor):

    def __init__(self, functional_unit: FunctionalUnit):
        super().__init__()
        self.functional_unit = functional_unit
        self.unit_location = functional_unit.location
        self.unit_routing_info: UnitRoutingMap = {}

    def _shout_out(self, attributes: Dict[str, object]):
        supervisor = ActorRegistry().get_by_class(SupervisorActor)[0]
        supervisor.tell(RegistrationMessage(self.actor_ref, self.unit_location, attributes))
