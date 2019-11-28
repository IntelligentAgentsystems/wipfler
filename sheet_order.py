from abstract_sheet import *


class SheetOrder(AbstractSheet):

    def __init__(self, plot_order: Dict[Color, int]):
        super().__init__()
        self.plots = plot_order
