import unittest

from rushsimulation.vector import Vector
from rushsimulation.wall import Wall

from .test_base import TestBase


class TestWall(TestBase):
    def setUp(self):
        super(TestWall, self).setUp()
        self.wall = Wall(self.user_configs, (0, 500), (375, 100))

    def test_returns_x_collision_point(self):
        pos = Vector(100, 450)
        tip = Vector(300, 550)
        point = self.wall.get_collision_point(tip, pos)
        self.assertEqual(point, Vector(200, 500))

    def test_returns_y_collision_point(self):
        pos = Vector(400, 550)
        tip = Vector(300, 550)
        point = self.wall.get_collision_point(tip, pos)
        expected_point = Vector(
            400 - self.user_configs['Simulation']['doorSize'] / 2,
            550
        )
        self.assertEqual(point, expected_point)

    def test_returns_x_collision_point_before_y(self):
        pos = Vector(300, 495)
        tip = Vector(400, 600)
        point = self.wall.get_collision_point(tip, pos)
        self.assertEqual(point[1], 500)

    def test_returns_none_collision_point(self):
        pos = Vector(400, 550)
        tip = Vector(410, 550)
        point = self.wall.get_collision_point(tip, pos)
        self.assertEqual(point, None)

if __name__ == '__main__':
    unittest.main()
