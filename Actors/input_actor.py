from Actors.operator_actor import OperatorActor
import constants as const
from Units.input_paper_stack import InputPaperStack


class InputActor(OperatorActor):

    def __init__(self, input_stack: InputPaperStack):
        super().__init__(input_stack)

    def on_start(self):
        self._shout_out({const.UNIT_TYPE_KEY, const.INPUTPAPERSTACK_TYPE})
