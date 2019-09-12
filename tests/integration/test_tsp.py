import unittest

from tspvisual.tsp import TSP, Path


class TestTSP(unittest.TestCase):

    def setUp(self):
        self.tsp = TSP()

    def test_display(self):
        expected = [
            (0.5, 0.765),
            (0.273, 0.721),
            (0.017, 0.908),
            (0.326, 0.478),
            (0.326, 0.882),
            (0.447, 0.9),
            (0.717, 0.282),
            (0.647, 0.708),
            (0.343, 0.982),
            (0.308, 0.569)
        ]

        self.tsp.load('tests/fixtures/bayg29.tsp')

        for result, expected in (zip(self.tsp.display, expected)):
            self.assertAlmostEqual(result[0], expected[0], 2)
            self.assertAlmostEqual(result[1], expected[1], 2)

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
                path = Path(path=p)
                result = self.tsp.path_dist(path)
                self.assertEqual(result, expected)
