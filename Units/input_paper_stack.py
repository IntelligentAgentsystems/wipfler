from threading import Thread
from typing import Tuple, List, Callable

import cv2

from Sheets.sheet import Sheet
from Types.custom_types import Location
from Units.functional_unit import FunctionalUnit
from constants import Direction
import constants as const


model = cv2.imread(r'graphics\paper_stack.png', cv2.IMREAD_COLOR)

class InputPaperStack(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Location):
        super().__init__(unit_system, location, model)
        self.callbacks: List[Callable] = []

    def on_take(self, direction: Direction) -> Sheet:
        Thread(self.__fire_on_take_event()).start()
        return Sheet()

    def register_on_take_event(self, func: Callable):
        self.callbacks.append(func)

    def __fire_on_take_event(self):
        for c in self.callbacks:
            c()

    def unregister_on_take_event(self, func: Callable):
        self.callbacks.remove(func)
