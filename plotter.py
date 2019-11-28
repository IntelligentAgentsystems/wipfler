from typing import Tuple
from abstract_sheet import Color
from functional_unit import FunctionalUnit
import time


class Plotter(FunctionalUnit):

    def __init__(self, location: Tuple[int, int], color: Color, plot_duration_seconds: float = 2):
        super().__init__(location)
        self.color = color
        self.plot_duration_seconds = plot_duration_seconds
        self.last_plot_start_seconds = 0

    def plot(self):
        if self.sheet is None:
            raise NoSheetToPlotError(self)
        if self.is_plotting():
            raise PlotterBusyError(self)
        self.last_plot_start_seconds = time.time()
        self.sheet.plot(self.color)

    def is_plotting(self) -> bool:
        return time.time() < self.last_plot_start_seconds + self.plot_duration_seconds


class NoSheetToPlotError(Exception):
    def __init__(self, plotter: Plotter):
        super().__init__(f'Plotter at {plotter.location} has no sheet to plot on')


class PlotterBusyError(Exception):
    def __init__(self, plotter: Plotter):
        super().__init__(f'Plotter at {plotter.location} is still plotting')
