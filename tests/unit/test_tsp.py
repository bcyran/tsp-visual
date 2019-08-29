import unittest
from copy import deepcopy
from unittest.mock import patch

from tspvisual.tsp import TSP, Path, TSPLib


class TestPath(unittest.TestCase):

    def test_init(self):
        for i in range(10):
            result = Path(i)
            self.assertListEqual(result._path, [-1 for _ in range(i)])
            self.assertEqual(result.length, i)
            self.assertEqual(result.distance, -1)

    def test_set_stop(self):
        data = [
            (1, 5, [-1, 5, -1, -1, -1, -1]),
            (0, 0, [0, 5, -1, -1, -1, -1]),
            (5, 9, [0, 5, -1, -1, -1, 9]),
            (2, 3, [0, 5, 3, -1, -1, 9]),
            (3, 7, [0, 5, 3, 7, -1, 9]),
            (4, 6, [0, 5, 3, 7, 6, 9]),
            (0, 4, [4, 5, 3, 7, 6, 9]),
            (-1, 8, [4, 5, 3, 7, 6, 8])
        ]

        path = Path(6)

        for index, city, expected in data:
            with self.subTest(index=index, city=city):
                path.set_stop(index, city)
                self.assertListEqual(path._path, expected)

    def test_set_stop_exception(self):
        data = [6, 7, 20, -7]

        path = Path(6)

        for index in data:
            with self.subTest(index=index, length=path.length):
                self.assertRaises(IndexError, path.set_stop, index, 0)

    def test_get_stop(self):
        data = [2, 7, 4, 3, 5, 1]

        path = Path(path=data)

        for index, value in enumerate(data):
            with self.subTest(index=index):
                result = path.get_stop(index)
                self.assertEqual(result, value)

    def test_get_stop_exception(self):
        data = [6, 7, 20, -7]

        path = Path(6)

        for index in data:
            with self.subTest(index=index, length=path.length):
                self.assertRaises(IndexError, path.get_stop, index)

    def test_set_path(self):
        data = [
            [1, 2, 3, 4, 5, 6],
            [9, 20, 1, 5, 55, 7],
            [0, 0, 0, 0, 0, 0]
        ]

        path = Path(6)

        for p in data:
            with self.subTest(path=p):
                path.set_path(p)
                self.assertListEqual(path._path, p)

    def test_set_path_exception(self):
        data = [
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 6, 7],
            [1],
            []
        ]

        path = Path(6)

        for p in data:
            with self.subTest(path=p):
                self.assertRaises(ValueError, path.set_path, p)

    def test_get_path(self):
        data = [
            [1, 2, 3, 4, 5, 6],
            [9, 20, 1, 5, 55, 7],
            [0, 0, 0, 0, 0, 0]
        ]

        path = Path(6)

        for p in data:
            with self.subTest(path=p):
                path._path = p
                result = path.get_path()
                self.assertListEqual(result, p)

    def test_shuffle(self):
        data = [
            ([0, 1, 2, 3, 4, 5, 6, 7], 2, 5),
            ([0, 1, 2, 3, 3, 5, 6, 0], 1, -1),
            ([5, 4, 3, 2, 1], 0, 4),
            ([1, 2, 3], 0, 2),
            ([], 0, 0)
        ]

        for p, i, j in data:
            with self.subTest(path=p, i=i, j=j):
                path = Path(path=deepcopy(p))
                path.shuffle(i, j)

                # Make sure no elements are lost or added
                for n in p:
                    self.assertEqual(path.get_path().count(n), p.count(n))

                # Compare slices that shouldn't be shuffled
                self.assertListEqual(path.get_path()[0:i], p[0:i])
                self.assertListEqual(path.get_path()[j:-1], p[j:-1])

    def test_in_path(self):
        data = [
            (4, None, True),
            (2, None, True),
            (7, None, True),
            (3, None, False),
            (7, 6, True),
            (4, 1, True),
            (8, 3, True),
            (4, 0, False),
            (7, 5, False),
            (10, 3, False)
        ]

        path = Path(path=[4, 1, 8, 2, 9, 7])

        for city, limit, expected in data:
            with self.subTest(city=city, limit=limit):
                result = path.in_path(city, limit)
                self.assertEqual(result, expected)

    def test_swap(self):
        data = [
            (1, 3, [1, 4, 3, 2, 5, 6]),
            (0, 4, [5, 4, 3, 2, 1, 6]),
            (2, 5, [5, 4, 6, 2, 1, 3]),
            (5, 0, [3, 4, 6, 2, 1, 5]),
            (2, 3, [3, 4, 2, 6, 1, 5]),
            (4, 4, [3, 4, 2, 6, 1, 5])
        ]

        path = Path(path=[1, 2, 3, 4, 5, 6])

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                path.swap(i, j)
                result = path.get_path()
                self.assertListEqual(result, expected)

    def test_insert(self):
        data = [
            (1, 3, [1, 3, 4, 2, 5, 6]),
            (0, 4, [3, 4, 2, 5, 1, 6]),
            (2, 5, [3, 4, 5, 1, 6, 2]),
            (5, 0, [2, 3, 4, 5, 1, 6]),
            (2, 3, [2, 3, 5, 4, 1, 6]),
            (4, 4, [2, 3, 5, 4, 1, 6])
        ]

        path = Path(path=[1, 2, 3, 4, 5, 6])

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                path.insert(i, j)
                result = path.get_path()
                self.assertListEqual(result, expected)

    def test_invert(self):
        data = [
            (1, 3, [1, 4, 3, 2, 5, 6]),
            (0, 4, [5, 2, 3, 4, 1, 6]),
            (2, 5, [5, 2, 6, 1, 4, 3]),
            (5, 0, [3, 4, 1, 6, 2, 5]),
            (2, 3, [3, 4, 6, 1, 2, 5]),
            (4, 4, [3, 4, 6, 1, 2, 5])
        ]

        path = Path(path=[1, 2, 3, 4, 5, 6])

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                path.invert(i, j)
                result = path.get_path()
                self.assertListEqual(result, expected)

    def test_move(self):
        data = [
            (Path.Neighbourhood.SWAP, 1, 4, [1, 5, 3, 4, 2, 6]),
            (Path.Neighbourhood.INSERT, 1, 4, [1, 3, 4, 2, 5, 6]),
            (Path.Neighbourhood.INVERT, 1, 4, [1, 5, 2, 4, 3, 6])
        ]

        path = Path(path=[1, 2, 3, 4, 5, 6])

        for neigh, i, j, expected in data:
            with self.subTest(neigh=neigh, i=i, j=j):
                path.move(neigh, i, j)
                result = path.get_path()
                self.assertListEqual(result, expected)


class TestTSP(unittest.TestCase):

    def setUp(self):
        self.tsp = TSP()
        self.tsp._tsplib = TSPLib()
        self.distances = [
            [0,   2,  3, 4],
            [5,   0,  7, 8],
            [9,  10,  0, 12],
            [13, 14, 15, 0]
        ]

    @patch('tspvisual.tsp.TSPLib.weight')
    def test_calc_distances(self, mock_tsplib):
        self.tsp.dimension = len(self.distances)
        mock_tsplib.side_effect = lambda i, j: self.distances[i][j]

        self.tsp._calc_distances()

        self.assertListEqual(self.tsp.distances, self.distances)

    def test_dist(self):
        data = [
            (1, 3, 8),
            (3, 3, 0),
            (3, 2, 15),
            (1, 2, 7)
        ]

        self.tsp.distances = self.distances

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                result = self.tsp.dist(i, j)
                self.assertEqual(result, expected)

    def test_path_dist(self):
        data = [
            ([0, 1, 2, 3], 2 + 7 + 12),
            ([2, 0, 1, 3], 9 + 2 + 8),
            ([0, 3, 1, 0], 4 + 14 + 5),
            ([1, 1, 1, 1], 0),
            ([-1, -1, -1, -1], 0)
        ]

        self.tsp.distances = self.distances

        for p, expected in data:
            with self.subTest(p=p):
                path = Path(4)
                path.set_path(p)
                result = self.tsp.path_dist(path)
                self.assertEqual(result, expected)
