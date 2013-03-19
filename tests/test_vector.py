import unittest

from rushsimulation.vector import Vector


class TestVector(unittest.TestCase):
    def setUp(self):
        self.vector = Vector(4, 3)

    def test_truncate(self):
        truncated_vector = self.vector.truncate(6)
        self.assertEqual(truncated_vector.length(), self.vector.length())
        truncated_vector = truncated_vector.truncate(4)
        self.assertEqual(truncated_vector.length(), 4)

if __name__ == '__main__':
    unittest.main()
