from typing import List, Dict

from pykka import ThreadingActor, ActorRef

from Messages import RegistrationMessage, RequestOrderMessage, InteractWithMessage, Action, WaitMessage
from Sheets.sheet_order import SheetOrder
from Types.custom_types import Location
from util import distance
import constants as const


class SupervisorActor(ThreadingActor):

    def __init__(self):
        super().__init__()
        self.open_orders: List[SheetOrder] = []
        self.active_orders: Dict[ActorRef, SheetOrder] = {}
        self.closed_orders: List[SheetOrder] = []
        self.actor_locations: Dict[ActorRef, (Location, Dict[str, object])] = {}

    def reachable_actor_where(self, actor_ref: ActorRef, requirements: Dict[str, object]):
        location, _ = self.actor_locations[actor_ref]
        for entry in self.actor_locations:
            (other_actor_ref, (other_loc, attributes)) = entry
            if distance(location, other_loc) == 1 and requirements <= attributes:
                return other_actor_ref
        return None

    def on_receive(self, message):
        if isinstance(message, RegistrationMessage):
            self.actor_locations[message.actorRef] = (message.location, message.attributes)
        elif isinstance(message, RequestOrderMessage):
            actor_ref = message.actor_ref
            # actor_ref must be a ConveyorActor
            if actor_ref in self.active_orders.keys():
                # conveyor has sheet, doesn't know what to do
                missing_colors = self.active_orders[actor_ref].plots.keys()
                for c in missing_colors:
                    possible_plotter = self.reachable_actor_where(actor_ref, {const.UNIT_TYPE_KEY: const.PLOTTER_TYPE,
                                                                              const.COLOR_KEY: c})
                    if possible_plotter is not None:
                        actor_ref.tell(InteractWithMessage(self.actor_locations[possible_plotter], Action.GIVE))
                        return
                possible_output_stack = self.reachable_actor_where(actor_ref,
                                                                   {const.UNIT_TYPE_KEY: const.OUTPUTPAPERSTACK_TYPE})
                if possible_output_stack is not None:
                    actor_ref.tell(InteractWithMessage(self.actor_locations[possible_output_stack], Action.GIVE))
                    return
                possible_conveyor = self.reachable_actor_where(actor_ref, {const.UNIT_TYPE_KEY: const.CONVEYOR_TYPE})
                if possible_conveyor is not None:
                    actor_ref.tell(InteractWithMessage(self.actor_locations[possible_conveyor], Action.GIVE))
                    return
                raise NotImplementedError("Souldn't reach this")
            else:
                # conveyor needs sheet
                possible_input_stack = self.reachable_actor_where(actor_ref,
                                                                  {const.UNIT_TYPE_KEY: const.INPUTPAPERSTACK_TYPE})
                if possible_input_stack is not None:
                    actor_ref.tell(InteractWithMessage(self.actor_locations[possible_input_stack], Action.TAKE))
                else:  # Nothing actor can do, maybe other actor fell out
                    actor_ref.tell(WaitMessage())
