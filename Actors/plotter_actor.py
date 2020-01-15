import time

from Actors.operator_actor import OperatorActor, PlotMessage, PlotDoneMessage
from Units.plotter import Plotter
import constants as const


class PlotterActor(OperatorActor):
    def __init__(self, plotter: Plotter):
        super().__init__(plotter)

    def on_start(self):
        self._shout_out({const.UNIT_TYPE_KEY: const.PLOTTER_TYPE, const.COLOR_KEY: self.functional_unit.color})

    def on_receive(self, message):
        if isinstance(message, PlotMessage):
            requesting_actor = message.requesting_actor
            self.functional_unit.plot()
            time.sleep(self.functional_unit.plot_duration_seconds)
            while self.functional_unit.is_plotting():
                pass
            requesting_actor.tell(PlotDoneMessage())
