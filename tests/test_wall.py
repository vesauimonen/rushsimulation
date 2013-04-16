import unittest

from rushsimulation.vector import Vector
from rushsimulation.wall import Wall


class TestWall(unittest.TestCase):
    def setUp(self):
        self.wall = Wall((0, 500), (375, 100))

    def test_collision_point(self):
        pos = Vector(100, 450)
        velocity = Vector(300, 550)
        point = self.wall.get_collision_point(velocity, pos)
        self.assertEqual(point, Vector(200, 500))

if __name__ == '__main__':
    unittest.main()
