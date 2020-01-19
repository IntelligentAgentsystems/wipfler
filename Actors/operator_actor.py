import logging
from typing import Dict, List

from Actors.supervisor_actor import SupervisorActor
from Types.custom_types import UnitRoutingMap
from pykka import ThreadingActor, ActorRegistry, ActorRef
from Messages import *

from Units.functional_unit import FunctionalUnit


class OperatorActor(ThreadingActor):

    def __init__(self):
        super().__init__()

    def _register(self, unit_location: Location, attributes: Dict[str, object]):
        for supervisor in ActorRegistry().get_by_class(SupervisorActor):
            supervisor.tell(RegistrationMessage(self.actor_ref, unit_location, attributes))

    def _unregister(self):
        for supervisor in ActorRegistry().get_by_class(SupervisorActor):
            supervisor.tell(UnRegistrationMessage(self.actor_ref))

    def on_failure(self, exception_type, exception_value, traceback):
        logging.log(logging.ERROR, exception_type(exception_value))
