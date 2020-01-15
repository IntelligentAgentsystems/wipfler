from typing import Tuple
from Sheets.abstract_sheet import Color
from Sheets.sheet import Sheet
from Units.functional_unit import FunctionalUnit, UnitOccupiedError, NoSheetError
import time

from constants import Direction


class Plotter(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Tuple[int, int], color: Color, plot_duration_seconds: float = 2):
        super().__init__(unit_system, location)
        self.sheet: Sheet = None
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

    def on_receive(self, sheet: Sheet, direction: Direction):
        if self.sheet is not None:
            raise UnitOccupiedError(self)
        self.sheet = sheet

    def on_take(self, direction: Direction) -> Sheet:
        if self.sheet is None:
            raise NoSheetError(self)
        if self.is_plotting():
            raise UnitOccupiedError(self)
        tmp = self.sheet
        self.sheet = None
        return tmp


class NoSheetToPlotError(Exception):
    def __init__(self, plotter: Plotter):
        super().__init__(f'Plotter at {plotter.location} has no sheet to plot on')


class PlotterBusyError(Exception):
    def __init__(self, plotter: Plotter):
        super().__init__(f'Plotter at {plotter.location} is still plotting')
