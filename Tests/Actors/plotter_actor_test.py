import time
import unittest

from Actors.plotter_actor import PlotterActor
from Messages import PlotMessage
from Sheets.sheet import Sheet, Color
from Units.plotter import Plotter


class PlotterActorTest(unittest.TestCase):

    def test_simple_scenario(self):
        sheet = Sheet()
        plt = Plotter((0, 0), Color.Blue)
        actor = PlotterActor.start(plt)
        actor.tell(PlotMessage)
        time.sleep(plt.plot_duration_seconds * 1.5)
        actor.stop(timeout=0)
        self.assertIn(Color.Blue, sheet.plots.keys())
