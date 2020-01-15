import unittest

from Units.conveyor_belt import *
from Units.unit_system import UnitSystem, NoUnitAtLocationError

TURN_DURATION_SECONDS = .1


class ConveyorTest(unittest.TestCase):

    def test_is_turning_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=1000)
        c1.turn_clockwise()
        self.assertTrue(c1.is_turning())

    def test_is_turning_counter_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=1000)
        c1.turn_counter_clockwise()
        self.assertTrue(c1.is_turning())

    def test_multiple_turn_commands_clockwise(self):
        with(self.assertRaises(ConveyorTurningError)):
            c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=1000)
            c1.turn_clockwise()
            c1.turn_clockwise()

    def test_multiple_turn_commands_counter_clockwise(self):
        with(self.assertRaises(ConveyorTurningError)):
            c1 = ConveyorBelt((0, 0), turn_duration_seconds=1000)
            c1.turn_counter_clockwise()
            c1.turn_counter_clockwise()

    def test_await_turn_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_clockwise()
        t1 = time.time()
        while c1.is_turning():
            pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.East)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_turn_counter_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        c1.turn_counter_clockwise()
        t1 = time.time()
        while c1.is_turning():
            pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.West)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_full_turn_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        for i in range(0, 4):
            c1.turn_clockwise()
            t1 = time.time()
            while c1.is_turning():
                pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.North)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_await_full_turn_counter_clockwise(self):
        c1 = ConveyorBelt(None, (0, 0), turn_duration_seconds=TURN_DURATION_SECONDS)
        for i in range(0, 4):
            c1.turn_counter_clockwise()
            t1 = time.time()
            while c1.is_turning():
                pass
        t2 = time.time()
        self.assertEqual(c1.direction, Direction.North)
        self.assertGreaterEqual(t2 - t1, c1.turn_duration_seconds)

    def test_hand_to_giving_facing_away(self):
        with(self.assertRaises(ConveyorFacingAwayError)):
            sys = UnitSystem()
            c1 = sys.create_conveyor((0, 0))
            c2 = sys.create_conveyor((1, 0))
            c1.direction = Direction.East
            c2.direction = Direction.North
            c1.sheet = Sheet()
            c1.put()

    def test_hand_to_recieving_facing_away(self):
        with(self.assertRaises(NoUnitAtLocationError)):
            sys = UnitSystem()
            c1 = sys.create_conveyor((0, 0))
            c2 = sys.create_conveyor((1, 0))
            c1.direction = Direction.North
            c2.direction = Direction.North
            c1.sheet = Sheet()
            c1.put()

    def test_hand_to_directions(self):
        sys = UnitSystem()
        c_north = sys.create_conveyor((1, 0))
        c_east = sys.create_conveyor((2, 1))
        c_south = sys.create_conveyor((1, 2))
        c_west = sys.create_conveyor((0, 1))
        c_center = sys.create_conveyor((1, 1))

        c_north.direction = Direction.South
        c_east.direction = Direction.West
        c_south.direction = Direction.North
        c_west.direction = Direction.East
        c_center.direction = Direction.North
        for _ in [c_north, c_east, c_south, c_west]:
            c_center.sheet = Sheet()
            c_center.put()
            c_center.turn_clockwise()
            while c_center.is_turning():
                pass


if __name__ == '__main__':
    unittest.main()
