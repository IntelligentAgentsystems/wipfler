from Sheets.abstract_sheet import *


class Sheet(AbstractSheet):

    def __init__(self):
        super().__init__()

    def plot(self, color: Color):
        self.plots[color] += 1

    def __str__(self):
        return ', '.join(str(item) for item in self.plots.items())
