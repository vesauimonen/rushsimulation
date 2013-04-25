import os
import unittest
import json

from rushsimulation.config_handler import ConfigHandler
from rushsimulation.simulation import RushSimulation


class TestConfigHandler(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.curdir, 'tests/test_config.json')
        config_handler = ConfigHandler(json.load(open(path)))
        user_configs = config_handler.handle()
        self.simulation = RushSimulation(user_configs=user_configs)

    def test_initializing(self):
        path = os.path.join(os.path.curdir, 'tests/test_config.json')
        config_handler = ConfigHandler(json.load(open(path)))
        user_configs = config_handler.handle()
        simulation = RushSimulation(user_configs=user_configs)
        self.assertEqual(len(simulation.children), 2)

    def test_set_up(self):
        self.simulation.set_up()
        self.assertEqual(
            len(self.simulation.children),
            self.simulation.vehicle_amount + 2
        )
        self.assertEqual(
            len(self.simulation.vehicles),
            self.simulation.vehicle_amount
        )

    def test_start_pause(self):
        self.assertFalse(self.simulation.simulation_on)
        self.simulation.start()
        self.assertTrue(self.simulation.simulation_on)
        self.simulation.pause()
        self.assertFalse(self.simulation.simulation_on)

    def test_stop(self):
        self.assertFalse(self.simulation.simulation_on)
        self.simulation.start()
        self.assertTrue(self.simulation.simulation_on)
        self.simulation.stop()
        self.assertFalse(self.simulation.simulation_on)


if __name__ == '__main__':
    unittest.main()
