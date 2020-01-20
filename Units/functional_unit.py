import constants as const
from Sheets.sheet import Sheet
from Types.custom_types import Location
from constants import Direction


class FunctionalUnit:
    """
    Basic functionality and attributes for Functional units
    """

    def __init__(self, unit_system: 'UnitSystem', location: Location, icon=None):
        """
        :param location: (x, y) values of unit
        """
        self.location: Location[int, int] = location
        self.unit_sytem = unit_system
        if icon is not None:
            self.update_system_image(icon)

    def update_system_image(self, icon):
        self.unit_sytem.image[self.location[1] * const.IMAGE_SIZE: (self.location[1] + 1) * const.IMAGE_SIZE,
        self.location[0] * const.IMAGE_SIZE: (self.location[0] + 1) * const.IMAGE_SIZE, :] = icon
        self.unit_sytem.update_image()

    def on_receive(self, sheet: Sheet, direction: Direction):
        pass

    def on_take(self, direction: Direction) -> Sheet:
        pass


class UnitOccupiedError(Exception):

    def __init__(self, receiver: FunctionalUnit):
        super().__init__(f'Reciever {receiver.__class__.__name__} at {receiver} already has Sheet\n')


class NoSheetError(Exception):

    def __init__(self, sender: FunctionalUnit):
        super().__init__(f'{sender.__class__.__name__} at {sender.location} has no Sheet')
