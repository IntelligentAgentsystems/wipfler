from threading import Thread
from typing import Tuple, List, Callable

from Units.functional_unit import FunctionalUnit
from Sheets.sheet import Sheet
from constants import Direction


class InputPaperStack(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Tuple[int, int]):
        super().__init__(unit_system, location)
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

