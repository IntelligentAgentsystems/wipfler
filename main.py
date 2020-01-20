import logging
from typing import List

import cv2

from Actors.conveyor_actor import ConveyorActor
from Actors.input_actor import InputActor
from Actors.output_actor import OutputActor
from Actors.plotter_actor import PlotterActor
from Actors.sleepy_actor import SleepyActor
from Actors.supervisor_actor import SupervisorActor
from Messages import SheetOrderMessage
from Sheets.abstract_sheet import Color
from Sheets.sheet_order import SheetOrder
from Units.functional_unit import FunctionalUnit
from Units.unit_system import UnitSystem

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pykka').setLevel(logging.DEBUG)


def create_functional_units_and_actors(sys: UnitSystem) -> List[FunctionalUnit]:
    return [
        InputActor.start(sys.create_input_paper_stack((0, 1))),
        OutputActor.start(sys.create_output_paper_stack((3, 1))),
        ConveyorActor.start(sys.create_conveyor((1, 1))),
        ConveyorActor.start(sys.create_conveyor((2, 1))),
        PlotterActor.start(sys.create_plotter((1, 0), color=Color.Red)),
        PlotterActor.start(sys.create_plotter((2, 0), color=Color.Green)),
        PlotterActor.start(sys.create_plotter((1, 2), color=Color.Yellow)),
        PlotterActor.start(sys.create_plotter((2, 2), color=Color.Blue))]


def main():
    unit_system = UnitSystem()
    supervisor = SupervisorActor.start()
    worker_actors = create_functional_units_and_actors(unit_system)
    for sheet_order in [
        SheetOrder({Color.Red: 1}),
        SheetOrder({Color.Blue: 1}),
        SheetOrder({Color.Green: 1}),
        SheetOrder({Color.Yellow: 1}),
        SheetOrder({Color.Red: 1, Color.Yellow: 1}),
        SheetOrder({Color.Yellow: 1, Color.Green: 1})
    ]:
        supervisor.tell(SheetOrderMessage(sheet_order))
    key = 0
    while key != 27:
        unit_system.update_image()
        key = cv2.waitKey()
    for w_actor in worker_actors:
        w_actor.stop()
    supervisor.stop()


if __name__ == '__main__':
    main()
