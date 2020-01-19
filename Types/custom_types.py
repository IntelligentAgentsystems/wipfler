from typing import NewType, Tuple, Dict

from pykka import ActorRef

# name of machine and attributes

FunctionalUnitInfo = NewType('FunctionalUnitInfo', Tuple[int, Tuple[object]])

RoutingInfo = NewType('RoutingInfo', Tuple[ActorRef, int])

Location = NewType('Location', Tuple[int, int])

UnitRoutingMap = NewType('UnitRoutingMap', Dict['FunctionalUnit', RoutingInfo])
