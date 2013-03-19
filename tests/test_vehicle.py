import unittest

from rushsimulation.vector import Vector
from rushsimulation.vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vehicle = Vehicle()

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


if __name__ == '__main__':
    unittest.main()
