import logging
from typing import List, Dict

from pykka import ThreadingActor, ActorRef

import constants as const
from Messages import RegistrationMessage, InteractWithMessage, Action, InstructionRequest, SheetOrderMessage
from Sheets.sheet_order import SheetOrder
from Types.custom_types import Location
from util import distance

logging.getLogger('pykka').setLevel(logging.DEBUG)


class SupervisorActor(ThreadingActor):

    def __init__(self):
        super().__init__()
        self.open_orders: List[SheetOrder] = []
        self.active_orders: Dict[ActorRef, SheetOrder] = {}
        self.closed_orders: List[SheetOrder] = []
        self.actor_locations: Dict[ActorRef, (Location, Dict[str, object])] = {}

    def _reachable_actor_where(self, actor_ref: ActorRef, requirements: Dict[str, object]):
        location, _ = self.actor_locations[actor_ref]
        for entry in self.actor_locations.items():
            (other_actor_ref, (other_loc, attributes)) = entry
            if distance(location, other_loc) == 1 and all(req in attributes.items() for req in requirements.items()):
                return other_actor_ref
        return None

    def _handle_registration_message(self, message: RegistrationMessage):
        self.actor_locations[message.actorRef] = (message.location, message.attributes)
        logging.log(logging.DEBUG, f'SPV: Registered Actor at {message.location} with attributes {message.attributes}')
        conveyor_attribute = (const.UNIT_TYPE_KEY, const.CONVEYOR_TYPE)
        for entry in self.actor_locations.items():
            (other_actor_ref, (other_loc, attributes)) = entry
            if conveyor_attribute in attributes.items() and other_actor_ref not in self.active_orders.keys():
                self.actor_ref.tell(InstructionRequest(other_actor_ref))
                logging.log(logging.DEBUG, f'SPV: Reactivated Conveyor Actor at {other_loc} because of new Actor')

    def _handle_instruction_request(self, message: InstructionRequest):
        logging.log(logging.DEBUG, f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} requested Instruction')
        actor_ref = message.actor_ref  # actor_ref must be a ConveyorActor
        if actor_ref in self.active_orders.keys():
            logging.log(logging.DEBUG, f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} has open order')
            # conveyor has sheet, doesn't know what to do
            missing_colors = self.active_orders[actor_ref].open_plots.keys()
            for c in missing_colors:
                possible_plotter = self._reachable_actor_where(actor_ref, {const.UNIT_TYPE_KEY: const.PLOTTER_TYPE,
                                                                           const.COLOR_KEY: c})
                if possible_plotter is not None:
                    actor_ref.tell(InteractWithMessage(self.actor_locations[possible_plotter][0], Action.GIVETAKE,
                                                       possible_plotter))
                    logging.log(logging.DEBUG,
                                f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} instructed to give and take with Actor at {self.actor_locations[possible_plotter]}')
                    self.active_orders[actor_ref].color_was_plotted(c)
                    return
            possible_output_stack = self._reachable_actor_where(actor_ref,
                                                                {const.UNIT_TYPE_KEY: const.OUTPUTPAPERSTACK_TYPE})
            if possible_output_stack is not None and self.active_orders[actor_ref].is_completed():
                actor_ref.tell(InteractWithMessage(self.actor_locations[possible_output_stack][0], Action.GIVE))
                logging.log(logging.DEBUG,
                            f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} instructed to give sheet to Actor at {self.actor_locations[possible_output_stack]}')
                completed_order = self.active_orders[actor_ref]
                del self.active_orders[actor_ref]
                self.closed_orders.append(completed_order)
                return
            possible_conveyor = self._reachable_actor_where(actor_ref, {const.UNIT_TYPE_KEY: const.CONVEYOR_TYPE})
            if possible_conveyor is not None:
                actor_ref.tell(InteractWithMessage(self.actor_locations[possible_conveyor], Action.GIVE))
                logging.log(logging.DEBUG,
                            f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} instructed to give sheet to Actor at {self.actor_locations[possible_conveyor]}')
                return
            raise NotImplementedError("Souldn't reach this")
        else:  # conveyor needs sheet
            possible_input_stack = self._reachable_actor_where(actor_ref,
                                                               {const.UNIT_TYPE_KEY: const.INPUTPAPERSTACK_TYPE})
            if possible_input_stack is not None:
                if (self.open_orders):
                    actor_ref.tell(InteractWithMessage(self.actor_locations[possible_input_stack][0], Action.TAKE))
                    logging.log(logging.DEBUG,
                                f'SPV: Actor at {self.actor_locations[message.actor_ref][0]} instructed to take sheet from Actor at {self.actor_locations[possible_input_stack][0]}')
                    order = self.open_orders.pop(0)
                    self.active_orders[actor_ref] = order
                else:
                    logging.log(logging.DEBUG, f'SPV: Nothing to do for Actor at {self.actor_locations[actor_ref]}')

            else:
                raise Exception()
            # else:  # Nothing actor can do, maybe other actor fell out
            #     actor_ref.tell(WaitMessage())

    def _handle_sheet_order_message(self, message: SheetOrderMessage):
        self.open_orders.append(message.order)
        conveyor_attribute = (const.UNIT_TYPE_KEY, const.CONVEYOR_TYPE)
        for entry in self.actor_locations.items():
            (other_actor_ref, (other_loc, attributes)) = entry
            if conveyor_attribute in attributes.items() and other_actor_ref not in self.active_orders.keys():
                self.actor_ref.tell(InstructionRequest(other_actor_ref))
                logging.log(logging.DEBUG, f'SPV: Reactivated Conveyor Actor at {other_loc} because of new Sheet')

    def on_receive(self, message):
        if isinstance(message, RegistrationMessage):
            self._handle_registration_message(message)
        elif isinstance(message, InstructionRequest):
            self._handle_instruction_request(message)
        elif isinstance(message, SheetOrderMessage):
            self._handle_sheet_order_message(message)

    def on_failure(self, exception_type, exception_value, traceback):
        logging.log(logging.ERROR, exception_type(exception_value))
