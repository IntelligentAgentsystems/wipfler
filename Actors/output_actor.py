from Actors.operator_actor import OperatorActor
import constants as const


class OutputActor(OperatorActor):

    def on_start(self):
        self._shout_out({const.UNIT_TYPE_KEY, const.OUTPUTPAPERSTACK_TYPE})