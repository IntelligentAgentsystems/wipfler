import logging

import constants as const
from Actors.operator_actor import OperatorActor
from Units.input_paper_stack import InputPaperStack


class InputActor(OperatorActor):

    def __init__(self, input_stack: InputPaperStack):
        super().__init__()
        self.input_stack: InputPaperStack = input_stack

    def on_start(self):
        self._register(self.input_stack.location, {const.UNIT_TYPE_KEY: const.INPUTPAPERSTACK_TYPE})
        self.input_stack.register_on_take_event(self.on_sheet_taken)

    def on_sheet_taken(self):
        logging.log(logging.DEBUG, f'IPS: Sheet taken from InputPaperStack at {self.input_stack.location}')

    def on_stop(self):
        self.input_stack.unregister_on_take_event(self.on_sheet_taken)
