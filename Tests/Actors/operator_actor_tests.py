import unittest

from Actors.operator_actor import OperatorActor
from Units.functional_unit import FunctionalUnit

import time
from pykka import ActorRegistry


class FunctionalUnitTest(unittest.TestCase):

    def test_registration(self):
        f1 = FunctionalUnit((0, 0))
        f2 = FunctionalUnit((0, 1))
        f3 = FunctionalUnit((0, 2))

        a1 = OperatorActor.start(f1)
        time.sleep(.1)
        a2 = OperatorActor.start(f2)
        time.sleep(.1)
        a3 = OperatorActor.start(f3)
        time.sleep(.1)

        registry = ActorRegistry()
        for ref in [registry.get_by_urn(ref.actor_urn) for ref in [a1, a2, a3]]:
            a = ref._actor
            # print(f'Actor at {a.unit_location} has neighbour at { [f[0].unit_location for f in a.actor_dist_map.items()]}')
