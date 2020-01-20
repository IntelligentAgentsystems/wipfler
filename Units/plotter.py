import time
from threading import Thread

import cv2

from Sheets.abstract_sheet import Color
from Sheets.sheet import Sheet
from Types.custom_types import Location
from Units.functional_unit import FunctionalUnit, UnitOccupiedError, NoSheetError
from constants import Direction

color_code = cv2.COLOR_BGR2RGB

models = [
    cv2.normalize(cv2.imread(r'graphics\printer_red.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 1.0, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_green.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 1.0, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_blue.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 1.0, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_yellow.png', cv2.IMREAD_COLOR).astype(float),  None, 0.0, 1.0, cv2.NORM_MINMAX)
]

models2 = [
    cv2.normalize(cv2.imread(r'graphics\printer_red_2.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 0.5, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_green_2.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 0.5, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_blue_2.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 0.5, cv2.NORM_MINMAX),
    cv2.normalize(cv2.imread(r'graphics\printer_yellow_2.png', cv2.IMREAD_COLOR).astype(float), None, 0.0, 0.5, cv2.NORM_MINMAX)
]


class Plotter(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Location, color: Color,
                 plot_duration_seconds: float = 2):
        super().__init__(unit_system, location, models2[color.value])
        self.sheet: Sheet = None
        self.color = color
        self.plot_duration_seconds = plot_duration_seconds
        self.last_plot_start_seconds = 0

    def plot(self):
        Thread(target=self.do_animation).start()
        if self.sheet is None:
            raise NoSheetToPlotError(self)
        if self.is_plotting():
            raise PlotterBusyError(self)
        self.last_plot_start_seconds = time.time()
        self.sheet.plot(self.color)

    def do_animation(self):
        self.update_system_image(models[self.color.value])
        time.sleep(self.plot_duration_seconds * 4)
        self.update_system_image(models2[self.color.value])

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
