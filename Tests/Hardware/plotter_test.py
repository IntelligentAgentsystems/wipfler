import time
import unittest

from Sheets.sheet import Sheet
from Sheets.sheet_order import SheetOrder
from Units.plotter import *

PLOT_DURATION_SECONDS = .1


class PlotterTest(unittest.TestCase):

    def test_plot(self):
        plotter = Plotter(None, (0, 0), Color.Red, plot_duration_seconds=PLOT_DURATION_SECONDS)
        plotter.sheet = Sheet()
        plotter.plot()
        sheet_order = SheetOrder({
            Color.Red: 1
        })
        self.assertEqual(plotter.sheet, sheet_order)

    def test_plot_twice_immediately(self):
        with self.assertRaises(PlotterBusyError):
            plotter = Plotter(None, (0, 0), Color.Red, plot_duration_seconds=999)
            plotter.sheet = Sheet()
            plotter.plot()
            plotter.plot()

    def test_plot_no_sheet(self):
        with self.assertRaises(NoSheetToPlotError):
            plotter = Plotter(None, (0, 0), Color.Red, plot_duration_seconds=PLOT_DURATION_SECONDS)
            plotter.plot()

    def test_plot_twice_but_wait(self):
        plotter = Plotter(None, (0, 0), Color.Red, plot_duration_seconds=PLOT_DURATION_SECONDS)
        plotter.sheet = Sheet()
        plotter.plot()
        time.sleep(PLOT_DURATION_SECONDS)
        plotter.plot()
        sheet_order = SheetOrder({
            Color.Red: 2
        })
        self.assertEqual(plotter.sheet, sheet_order)
