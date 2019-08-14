import unittest

from tspvisual.tsp import TSP, Path


class TestTSP(unittest.TestCase):

    def setUp(self):
        self.tsp = TSP()

    def test_dist(self):
        data = [
            (3, 13, 182),
            (9, 5, 360),
            (5, 9, 360),
            (14, 0, 268),
            (0, 0, 0),
            (16, 16, 0),
            (0, 16, 121)
        ]

        self.tsp.load('tests/fixtures/gr17.tsp')

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                result = self.tsp.dist(i, j)
                self.assertEqual(result, expected)

    def test_path_dist(self):
        data = [
            ([0, 1, 2, 3, 4, 5], 22),
            ([5, 4, 3, 2, 1, 0], 22),
            ([5, 2, 0, 1, 4, 2], 34),
            ([0, 1, 2, 3, 4, 0], 27),
            ([5, 4, 3], 12),
            ([0, 0, 0, 0, 0, 0], 0),
            ([-1, -1, -1, -1, -1, -1], 0)
        ]

        self.tsp.load('tests/fixtures/test6.tsp')

        for p, expected in data:
            with self.subTest(path=p):
                path = Path(len(p))
                path.set_path(p)
                result = self.tsp.path_dist(path)
                self.assertEqual(result, expected)
