import logging

import constants as const
from Actors.operator_actor import OperatorActor
from Sheets.sheet import Sheet
from Units.output_paper_stack import OutputPaperStack


class OutputActor(OperatorActor):

    def __init__(self, output_stack: OutputPaperStack):
        super().__init__()
        self.output_stack: OutputPaperStack = output_stack

    def on_start(self):
        self._register(self.output_stack.location, {const.UNIT_TYPE_KEY: const.OUTPUTPAPERSTACK_TYPE})
        self.output_stack.callbacks.append(self.on_sheet_received)

    def on_sheet_received(self, sheet: Sheet):
        logging.log(logging.DEBUG, f'OPS: OutputPaperStack at {self.output_stack.location} received Sheet {sheet}')

    def on_stop(self):
        self.output_stack.callbacks.remove(self.on_sheet_received)
