import os
import unittest
import json


from rushsimulation.config_handler import ConfigHandler
from rushsimulation.simulation import RushSimulation
from rushsimulation.vector import Vector
from rushsimulation.vehicle import Vehicle


class TestBase(unittest.TestCase):
    path = os.path.join(os.path.curdir, 'tests/test_config.json')
    config_handler = ConfigHandler(json.load(open(path)))
    user_configs = config_handler.handle()

    def setUp(self):
        self.simulation = RushSimulation(user_configs=self.user_configs)
        self.vehicle = Vehicle(
            self.user_configs,
            target_vector=Vector(400, 600)
        )
        self.simulation.add_vehicle(self.vehicle)

    def tearDown(self):
        self.simulation.remove_vehicle(self.vehicle)
        self.simulation = None
