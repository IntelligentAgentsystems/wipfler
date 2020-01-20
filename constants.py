from enum import Enum

UNIT_TYPE_KEY = "unit_type"
COLOR_KEY = "color"
PLOTTER_TYPE = "plotter"
CONVEYOR_TYPE = "conveyor"
INPUTPAPERSTACK_TYPE = "inputpaperstack"
OUTPUTPAPERSTACK_TYPE = "outpaperstack"

IMAGE_SIZE = 200


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
