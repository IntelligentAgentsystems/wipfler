import time
import unittest

from Sheets.abstract_sheet import Color
from Sheets.sheet import Sheet
from Units.unit_system import UnitSystem


class FunctionalUnitTest(unittest.TestCase):

    def test_unit_creation(self):
        sys = UnitSystem()
        ips = sys.create_input_paper_stack((0, 0))
        self.assertIsNotNone(ips)
        self.assertEqual(sys, ips.unit_sytem)
        ops = sys.create_output_paper_stack((0, 0))
        self.assertIsNotNone(ops)
        self.assertEqual(sys, ops.unit_sytem)
        plt = sys.create_plotter((0, 0), Color.Red)
        self.assertIsNotNone(plt)
        self.assertEqual(sys, plt.unit_sytem)
        con = sys.create_conveyor((0, 0))
        self.assertIsNotNone(con)

    def test_take_from(self):
        sys = UnitSystem()
        location = (0, 0)
        plt = sys.create_plotter(location, Color.Red)
        sheet = Sheet()
        plt.sheet = sheet
        plt.plot()
        time.sleep(plt.plot_duration_seconds * 1.5)
        self.assertIn(Color.Red, sheet.plots.keys())
        sheet2 = sys.take_from_unit_at(location, (0, 1))
        self.assertEqual(sheet, sheet2)

    def test_drop_to(self):
        sys = UnitSystem()
        location = (0, 0)
        ops = sys.create_output_paper_stack(location)
        sheet = Sheet()
        sheet.plots[Color.Red] = 42
        sys.drop_to_unit_at(sheet, location, (0, 1))
        self.assertIn(sheet, ops.received_sheets)


