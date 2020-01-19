import time

import constants as const
from Actors.operator_actor import OperatorActor
from Messages import PerformActionMessage
from Units.plotter import Plotter


class PlotterActor(OperatorActor):
    def __init__(self, plotter: Plotter):
        super().__init__()
        self.plotter = plotter

    def on_start(self):
        self._register(self.plotter.location, {const.UNIT_TYPE_KEY: const.PLOTTER_TYPE, const.COLOR_KEY: self.plotter.color})

    def on_receive(self, message):
        if isinstance(message, PerformActionMessage):  # Blocking Request
            self.plotter.plot()
            time.sleep(self.plotter.plot_duration_seconds)
            while self.plotter.is_plotting():
                pass  # Make shure plotting Done
            return
