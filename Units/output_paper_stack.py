from threading import Thread
from typing import List, Callable

from Sheets.sheet import Sheet
from Types.custom_types import Location
from Units.functional_unit import FunctionalUnit
from constants import Direction


class OutputPaperStack(FunctionalUnit):

    def __init__(self, unit_system: 'UnitSystem', location: Location):
        super().__init__(unit_system, location)
        self.received_sheets = []
        self.callbacks: List[Callable] = []

    def on_receive(self, sheet: Sheet, direction: Direction):
        self.received_sheets.append(sheet)
        Thread(self.__fire_on_receive_event(sheet)).start()

    def register_on_receive_event(self, func: Callable):
        self.callbacks.append(func)

    def __fire_on_receive_event(self, sheet: Sheet):
        for c in self.callbacks:
            c(sheet)

    def unregister_on_receive_event(self, func: Callable):
        self.callbacks.remove(func)
