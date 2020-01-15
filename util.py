from Types.custom_types import Location
from constants import Direction


def distance(l1: Location, l2: Location) -> float:
    return abs(l1[0] - l2[0]) + abs(l1[1] - l2[1])


def relative_direction_of(location: Location, sender_location: Location) -> Direction:
    location_diff = (location[0] - sender_location[0], location[1] - sender_location[1])
    if location_diff[1] < 0:
        return Direction.North
    if location_diff[1] > 0:
        return Direction.South
    elif location_diff[0] < 0:
        return Direction.West
    else:
        return Direction.East


def opposite_direction(direction: Direction):
    return Direction((direction.value + 2) % 4)


def move_location(location: Location, direction: Direction) -> Location:
    dir_to_loc = {
        Direction.North: (0, -1),
        Direction.East: (1, 0),
        Direction.South: (0, 1),
        Direction.West: (-1, 0)
    }
    offset = dir_to_loc[direction]
    return (location[0] + offset[0], location[1] + offset[1])
