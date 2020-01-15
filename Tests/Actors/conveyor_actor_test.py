import time
import unittest

from Actors.plotter_actor import PlotterActor
from Messages import InteractWithMessage, Action, PlotMessage
from Sheets.abstract_sheet import Color
from Units.input_paper_stack import InputPaperStack
from Units.output_paper_stack import OutputPaperStack
from Units.conveyor_belt import ConveyorBelt
from Actors.conveyor_actor import ConveyorActor
from Units.plotter import Plotter


class ConveyorActorTest(unittest.TestCase):

    def test_simple_scenario(self):
        ips = InputPaperStack((0, 0))
        ops = OutputPaperStack((2, 0))
        cvb = ConveyorBelt((1, 0))
        actor = ConveyorActor.start(cvb)
        actor.tell(InteractWithMessage(ips.location, Action.TAKE))
        actor.tell(InteractWithMessage(ops.location, Action.GIVE))
        time.sleep(cvb.turn_duration_seconds * 4.5)
        self.assertGreater(len(ops.received_sheets), 0)

    def test_complex_scenario(self):
        ips = InputPaperStack((0, 0))
        ops = OutputPaperStack((2, 0))
        cvb = ConveyorBelt((1, 0), turn_duration_seconds=.1)
        plt = Plotter((1, 1), Color.Blue)
        cvb_actor = ConveyorActor.start(cvb)
        plt_actor = PlotterActor.start(plt)
        cvb_actor.tell(InteractWithMessage(ips.location, Action.TAKE))
        time.sleep(cvb.turn_duration_seconds * 4.5)
        cvb_actor.tell(InteractWithMessage(plt.location, Action.GIVE))
        time.sleep(cvb.turn_duration_seconds * 4.5)
        time.sleep(0.1)
        plt_actor.tell(PlotMessage())
        time.sleep(plt.plot_duration_seconds * 1.5)
        cvb_actor.tell(InteractWithMessage(plt.location, Action.TAKE))
        time.sleep(cvb.turn_duration_seconds * 4.5)
        cvb_actor.tell(InteractWithMessage(ops.location, Action.GIVE))
        time.sleep(cvb.turn_duration_seconds * 4.5)

        self.assertGreater(len(ops.received_sheets), 0)
