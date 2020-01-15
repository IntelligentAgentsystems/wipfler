import unittest

from Sheets.sheet import *
from Sheets.sheet_order import *


class SheetTest(unittest.TestCase):

    def sheet_comparison_test(self):
        sheet_order = SheetOrder({
            Color.Red: 1
        })
        actual_sheet = Sheet()
        self.assertNotEqual(sheet_order, actual_sheet)

    def sheet_comparison_test_2(self):
        sheet_order = SheetOrder({
            Color.Red: 1
        })
        actual_sheet = Sheet()
        actual_sheet.plot(Color.Red)
        self.assertEqual(sheet_order, actual_sheet)

    def sheet_comparison_test_3(self):
        sheet_order = SheetOrder({
            Color.Red: 1
        })
        actual_sheet = Sheet()
        actual_sheet.plot(Color.Red)
        self.assertTrue(sheet_order == actual_sheet)

    def sheet_comparison_test_4(self):
        orders = []
        actuals = []

        for color in [Color.Red, Color.Green, Color.Blue, Color.Yellow]:
            orders.append(SheetOrder({
                color: 1
            }))
            actual_sheet = Sheet()
            actual_sheet.plot(color)
            actuals.append(actual_sheet)
        for actual_sheet in actuals:
            self.assertIn(actual_sheet, orders)
