from Types.custom_types import Location


def distance(l1: Location, l2: Location) -> float:
    return abs(l1[0] - l2[0]) + abs(l1[1] - l2[1])