import unittest

from Units.conveyor_belt import *
import time
from Sheets.sheet import Sheet

TURN_DURATION_SECONDS = .1


class ConveyorTest(unittest.TestCase):

    def test_is_turning_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_clockwise()
        self.assertTrue(c1.is_turning())

    def test_is_turning_counter_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_counter_clockwise()
        self.assertTrue(c1.is_turning())

    def test_is_turning_counter_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_counter_clockwise()
        self.assertTrue(c1.is_turning())

    def test_multiple_turn_commands_clockwise(self):
        with(self.assertRaises(ConveyorTurningError)):
            c1 = ConveyorBelt((0, 0), turn_duration_seconds=1000)
            c1.turn_clockwise()
            c1.turn_clockwise()

    def test_multiple_turn_commands_counter_clockwise(self):
        with(self.assertRaises(ConveyorTurningError)):
            c1 = ConveyorBelt((0, 0), turn_duration_seconds=1000)
            c1.turn_counter_clockwise()
            c1.turn_counter_clockwise()

    def test_await_turn_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_clockwise()
        t1 = time.time()
        while c1.is_turning():
            pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.East)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_turn_counter_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_counter_clockwise()
        t1 = time.time()
        while c1.is_turning():
            pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.West)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_full_turn_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        for i in range(0, 4):
            c1.turn_clockwise()
            t1 = time.time()
            while c1.is_turning():
                pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.North)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_full_turn_counter_clockwise(self):
        c1 = ConveyorBelt((0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        for i in range(0, 4):
            c1.turn_counter_clockwise()
            t1 = time.time()
            while c1.is_turning():
                pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.North)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_hand_to_giving_facing_away(self):
        with(self.assertRaises(GivingConveyorFacingAwayError)):
            c1 = ConveyorBelt((0, 0), initial_direction=Direction.East)
            c2 = ConveyorBelt((0, 1), initial_direction=Direction.North)
            c1.sheet = Sheet()
            c1.give_sheet_to(c2)

    def test_hand_to_recieving_facing_away(self):
        with(self.assertRaises(ReceivingConveyorFacingAwayError)):
            c1 = ConveyorBelt((0, 0), initial_direction=Direction.South)
            c2 = ConveyorBelt((0, 1), initial_direction=Direction.East)
            c1.sheet = Sheet()
            c1.give_sheet_to(c2)

    def test_hand_to_directions(self):
        c_north = ConveyorBelt((1, 0), turn_duration_seconds=TURN_DURATION_SECONDS, initial_direction=Direction.South)
        c_east = ConveyorBelt((2, 1), turn_duration_seconds=TURN_DURATION_SECONDS, initial_direction=Direction.West)
        c_south = ConveyorBelt((1, 2), turn_duration_seconds=TURN_DURATION_SECONDS, initial_direction=Direction.North)
        c_west = ConveyorBelt((0, 1), turn_duration_seconds=TURN_DURATION_SECONDS, initial_direction=Direction.East)
        c_center = ConveyorBelt((1, 1), turn_duration_seconds=TURN_DURATION_SECONDS, initial_direction=Direction.North)
        for c in [c_north, c_east, c_south, c_west]:
            c_center.sheet = Sheet()
            c_center.give_sheet_to(c)
            c_center.turn_clockwise()
            while c_center.is_turning():
                pass


if __name__ == '__main__':
    unittest.main()
