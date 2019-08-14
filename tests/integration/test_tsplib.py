import unittest

from tspvisual.tsplib import TSPLib


class TestTSPLib(unittest.TestCase):

    def setUp(self):
        self.tsplib = TSPLib()

    def test_specification(self):
        expected = {
            'NAME': 'gr17',
            'TYPE': 'TSP',
            'COMMENT': '17-city problem (Groetschel)',
            'DIMENSION': 17,
            'EDGE_WEIGHT_TYPE': 'EXPLICIT',
            'EDGE_WEIGHT_FORMAT': 'LOWER_DIAG_ROW'
        }

        self.tsplib.load('tests/fixtures/gr17.tsp')
        self.assertDictEqual(self.tsplib.specification, expected)

    def test_coords(self):
        expected = [
            (16.47, 96.10),
            (16.47, 94.44),
            (20.09, 92.54),
            (22.39, 93.37),
            (25.23, 97.24),
            (22.00, 96.05),
            (20.47, 97.02),
            (17.20, 96.29),
            (16.30, 97.38),
            (14.05, 98.12),
            (16.53, 97.38),
            (21.52, 95.59),
            (19.41, 97.13),
            (20.09, 94.55)
        ]

        self.tsplib.load('tests/fixtures/burma14.tsp')
        self.assertListEqual(self.tsplib.coords, expected)

    def test_weights(self):
        expected = [
            [0, -1, -1, -1, -1, -1],
            [4,  0, -1, -1, -1, -1],
            [9,  4,  0, -1, -1, -1],
            [7,  4,  2,  0, -1, -1],
            [12, 9,  5,  5,  0, -1],
            [7,  6,  7,  5,  7,  0]
        ]

        self.tsplib.load('tests/fixtures/test6.tsp')
        self.assertListEqual(self.tsplib.weights, expected)

    def test_weight_explicit(self):
        data = [
            (9, 6, 444),
            (12, 1, 567),
            (1, 12, 567),
            (0, 0, 0),
            (16, 16, 0),
            (0, 15, 246)
        ]

        self.tsplib.load('tests/fixtures/gr17.tsp')

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                result = self.tsplib.weight(i, j)
                self.assertEqual(result, expected)

    def test_weight_euc_2d(self):
        data = [
            (3, 2, 2),
            (2, 3, 2),
            (0, 0, 0),
            (5, 5, 0),
            (4, 0, 12),
            (3, 1, 4)
        ]

        self.tsplib.load('tests/fixtures/test6.tsp')

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                result = self.tsplib.weight(i, j)
                self.assertEqual(result, expected)
