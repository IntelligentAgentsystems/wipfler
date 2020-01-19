from Sheets.abstract_sheet import *


class SheetOrder(AbstractSheet):

    def __init__(self, plot_order: Dict[Color, int]):
        super().__init__()
        self.plots = plot_order
        self.open_plots = plot_order.copy()

    def color_was_plotted(self, c: Color):
        self.open_plots[c] -= 1
        if self.open_plots[c] == 0:
            del self.open_plots[c]

    def is_completed(self) -> bool:
        return not self.open_plots
