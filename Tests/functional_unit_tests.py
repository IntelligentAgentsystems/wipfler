import unittest

from Units.functional_unit import *
from Sheets.sheet import Sheet


class FunctionalUnitTest(unittest.TestCase):

    def test_hand_to(self):
        fu1 = FunctionalUnit((0, 0))
        fu2 = FunctionalUnit((0, 1))
        fu1.sheet = Sheet()

        fu1.give_sheet_to(fu2)

    def test_hand_to_out_of_range(self):
        with self.assertRaises(UnitOutOfRangeError):
            fu1 = FunctionalUnit((0, 0))
            fu2 = FunctionalUnit((0, 2))
            fu1.sheet = Sheet()

            fu1.give_sheet_to(fu2)

    def test_hand_to_no_sheet(self):
        with self.assertRaises(NoSheetError):
            fu1 = FunctionalUnit((0, 0))
            fu2 = FunctionalUnit((0, 1))

            fu1.give_sheet_to(fu2)

    def test_hand_to_no_uccupied(self):
        with self.assertRaises(UnitOccupiedError):
            fu1 = FunctionalUnit((0, 0))
            fu2 = FunctionalUnit((0, 1))
            fu1.sheet = Sheet()
            fu2.sheet = Sheet()

            fu1.give_sheet_to(fu2)


if __name__ == '__main__':
    unittest.main()
