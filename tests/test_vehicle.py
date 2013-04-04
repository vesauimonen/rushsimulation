import unittest

from rushsimulation.vector import Vector
from rushsimulation.simulation import RushSimulation
from rushsimulation.vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.simulation = RushSimulation()
        self.vehicle = Vehicle()
        self.simulation.add_vehicle(self.vehicle)

    def tearDown(self):
        self.simulation.remove_vehicle(self.vehicle)
        self.simulation = None

    def test_is_in_target(self):
        self.vehicle.target = Vector(100, 100)
        self.vehicle.pos = Vector(100, 100)
        self.assertTrue(self.vehicle.is_in_target())
        self.vehicle.pos = Vector(
            100 - self.vehicle.TARGET_OFFSET,
            100 - self.vehicle.TARGET_OFFSET
        )
        self.assertTrue(self.vehicle.is_in_target())
        self.vehicle.pos = Vector(
            100 + self.vehicle.TARGET_OFFSET,
            100 + self.vehicle.TARGET_OFFSET
        )
        self.assertTrue(self.vehicle.is_in_target())

    def test_is_not_in_target(self):
        self.vehicle.target = Vector(100, 100)
        self.vehicle.pos = Vector(0, 0)
        self.assertFalse(self.vehicle.is_in_target())
        self.vehicle.pos = Vector(
            100 - self.vehicle.TARGET_OFFSET - 1,
            100 - self.vehicle.TARGET_OFFSET
        )
        self.assertFalse(self.vehicle.is_in_target())
        self.vehicle.pos = Vector(
            100 + self.vehicle.TARGET_OFFSET,
            100 + self.vehicle.TARGET_OFFSET + 1
        )
        self.assertFalse(self.vehicle.is_in_target())

    def test_set_to_start_position(self):
        self.vehicle.set_to_start_position()
        self.assertEqual(self.vehicle.y, 0)
        self.assertTrue(self.vehicle.x >= 0)
        self.assertTrue(self.vehicle.x < 800)
        self.assertEqual(self.vehicle.velocity, [0, 0])
        self.assertEqual(self.vehicle.acceleration, [0, 0])
        self.assertEqual(self.vehicle.steering_force, [0, 0])

    def test_get_nearby_vehicles(self):
        self.assertEqual(self.vehicle.get_nearby_vehicles(), [])
        another_vehicle = Vehicle()
        self.simulation.add_vehicle(another_vehicle)
        self.assertEqual(
            self.vehicle.get_nearby_vehicles(),
            [another_vehicle]
        )
        self.simulation.remove_vehicle(another_vehicle)

    def test_get_separation_force(self):
        self.vehicle.pos = Vector(10, 10)
        self.assertEqual(self.vehicle.get_separation_force(), Vector(0, 0))
        another_vehicle = Vehicle()
        another_vehicle.pos = Vector(6, 7)
        self.simulation.add_vehicle(another_vehicle)
        self.assertEqual(
            self.vehicle.get_separation_force(),
            Vector(4, 3)
        )
        self.simulation.remove_vehicle(another_vehicle)


if __name__ == '__main__':
    unittest.main()
