import logging
import time
import unittest

from pykka import ActorRegistry

from Actors.conveyor_actor import ConveyorActor
from Actors.input_actor import InputActor
from Actors.output_actor import OutputActor
from Actors.plotter_actor import PlotterActor
from Actors.sleepy_actor import SleepyActor
from Actors.supervisor_actor import SupervisorActor
from Messages import SheetOrderMessage
from Sheets.abstract_sheet import Color
from Sheets.sheet_order import SheetOrder
from Units.unit_system import UnitSystem

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pykka').setLevel(logging.DEBUG)


class IntegrationTest(unittest.TestCase):

    def test_setup_1(self):  # check nothing crashes
        sys = UnitSystem()
        supervisor = SupervisorActor.start()
        InputActor.start(sys.create_input_paper_stack((0, 1))),
        OutputActor.start(sys.create_output_paper_stack((3, 1))),
        ConveyorActor.start(sys.create_conveyor((1, 1))),
        ConveyorActor.start(sys.create_conveyor((2, 1))),
        PlotterActor.start(sys.create_plotter((1, 0), color=Color.Red)),
        PlotterActor.start(sys.create_plotter((2, 0), color=Color.Green)),
        PlotterActor.start(sys.create_plotter((1, 3), color=Color.Yellow)),
        PlotterActor.start(sys.create_plotter((2, 3), color=Color.Blue))
        time.sleep(10)
        ActorRegistry().stop_all(block=True)

    def test_setup_2(self):  # smaller setup
        sys = UnitSystem()
        supervisor = SupervisorActor.start()
        InputActor.start(sys.create_input_paper_stack((0, 1))),
        ops = sys.create_output_paper_stack((2, 1))
        OutputActor.start(ops),
        ConveyorActor.start(sys.create_conveyor((1, 1))),
        PlotterActor.start(sys.create_plotter((1, 0), color=Color.Red)),
        PlotterActor.start(sys.create_plotter((1, 2), color=Color.Blue)),
        sheet_orders = [SheetOrder({Color.Red: 1})]
        for order in sheet_orders:
            supervisor.tell(SheetOrderMessage(order))
        SleepyActor.start(20).stop(True)
        for order in sheet_orders:
            self.assertIn(order, ops.received_sheets)
        ActorRegistry().stop_all(block=True)

    def test_setup_3(self):  # smaller setup
        sys = UnitSystem()
        supervisor = SupervisorActor.start()
        InputActor.start(sys.create_input_paper_stack((0, 1))),
        ops = sys.create_output_paper_stack((2, 1))
        OutputActor.start(ops),
        ConveyorActor.start(sys.create_conveyor((1, 1))),
        PlotterActor.start(sys.create_plotter((1, 0), color=Color.Red)),
        PlotterActor.start(sys.create_plotter((1, 2), color=Color.Blue)),
        sheet_orders = [SheetOrder({Color.Red: 1}), SheetOrder({Color.Blue: 1})]
        for order in sheet_orders:
            supervisor.tell(SheetOrderMessage(order))
        SleepyActor.start(30).stop(True)
        for order in sheet_orders:
            self.assertIn(order, ops.received_sheets)
        ActorRegistry().stop_all(block=True)

    def test_setup_4(self):  # smaller setup
        sys = UnitSystem()
        supervisor = SupervisorActor.start()
        InputActor.start(sys.create_input_paper_stack((0, 1))),
        ConveyorActor.start(sys.create_conveyor((1, 1))),
        ConveyorActor.start(sys.create_conveyor((2, 1))),
        PlotterActor.start(sys.create_plotter((1, 0), color=Color.Red)),
        PlotterActor.start(sys.create_plotter((2, 0), color=Color.Blue)),
        ops = sys.create_output_paper_stack((3, 1))
        OutputActor.start(ops),
        sheet_orders = [SheetOrder({Color.Red: 1}), SheetOrder({Color.Blue: 1})]
        for order in sheet_orders:
            supervisor.tell(SheetOrderMessage(order))

        SleepyActor.start(60).stop(True)
        for order in sheet_orders:
            self.assertIn(order, ops.received_sheets)
        ActorRegistry().stop_all(block=True)
