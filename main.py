import time
from typing import List

from Units.functional_unit import FunctionalUnit
from Sheets.abstract_sheet import Color
from Units.conveyor_belt import ConveyorBelt
from Units.plotter import Plotter
from Units.input_paper_stack import InputPaperStack
from Units.output_paper_stack import OutputPaperStack
from Actors.supervisor_actor import SupervisorActor
from Actors.conveyor_actor import ConveyorActor
from Actors.plotter_actor import PlotterActor
from Actors.input_actor import InputActor
from Actors.output_actor import OutputActor
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pykka').setLevel(logging.DEBUG)



def create_functional_units_and_actors() -> List[FunctionalUnit]:
    return [
        InputActor.start(InputPaperStack((0, 1))),
        OutputActor.start(OutputPaperStack((3, 1))),
        ConveyorActor.start(ConveyorBelt((1, 1))),
        ConveyorActor.start(ConveyorBelt((2, 1))),
        PlotterActor.start(Plotter((1, 0), color=Color.Red)),
        PlotterActor.start(Plotter((2, 0), color=Color.Green)),
        PlotterActor.start(Plotter((1, 3), color=Color.Yellow)),
        PlotterActor.start(Plotter((2, 3), color=Color.Blue))]


supervisor = SupervisorActor.start()
create_functional_units_and_actors()
time.sleep(20)

