import unittest

from kivy.core.window import Window

from rushsimulation.vector import Vector
from rushsimulation.vehicle import Vehicle

from .test_base import TestBase


class TestVehicle(TestBase):

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
        self.vehicle.pos = Vector(
            300,
            Window.height + 2
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
        self.assertTrue(self.vehicle.max_speed >= 4)
        self.assertTrue(
            self.vehicle.max_speed <= self.user_configs['Vehicle']['maxSpeed']
        )

    def test_get_nearby_vehicles(self):
        self.assertEqual(self.vehicle.get_nearby_vehicles(50), [])
        another_vehicle = Vehicle(
            self.user_configs,
            target_vector=Vector(400, 600)
        )
        self.simulation.add_vehicle(another_vehicle)
        self.assertEqual(
            self.vehicle.get_nearby_vehicles(50),
            [another_vehicle]
        )
        self.simulation.remove_vehicle(another_vehicle)

    def test_validate_pos(self):
        self.vehicle.pos = (0, 0)
        another_vehicle = Vehicle(
            self.user_configs,
            target_vector=Vector(400, 600)
        )
        self.simulation.add_vehicle(another_vehicle)
        another_vehicle.pos = (0, 25)
        self.assertEqual(another_vehicle.validate_pos((0, 3)), Vector(0, 15))

    def test_get_separation_force(self):
        self.vehicle.pos = Vector(10, 30)
        self.assertEqual(self.vehicle.get_separation_force(), Vector(0, 0))
        another_vehicle = Vehicle(
            self.user_configs,
            target_vector=Vector(400, 600)
        )
        another_vehicle.pos = Vector(10, 10)
        self.simulation.add_vehicle(another_vehicle)
        self.assertEqual(
            self.vehicle.get_separation_force(),
            Vector(0, 0.05)
        )
        self.simulation.remove_vehicle(another_vehicle)


if __name__ == '__main__':
    unittest.main()
