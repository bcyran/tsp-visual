from unittest import TestCase
from unittest.mock import patch

from tspvisual.solvers.ga import GASolver
from tspvisual.tsp import TSP, Path


class TestGASolver(TestCase):

    def setUp(self):
        tsp = TSP()
        self.gasolver = GASolver(tsp)

    @patch('tspvisual.solvers.ga.GASolver._rand_subpath')
    @patch('tspvisual.tsp.TSP.path_dist')
    def test_crossover_ox(self, mock_dist, mock_rand_subpath):
        data = [
            ([8, 4, 7, 3, 6, 2, 5, 1, 9, 0],
             [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], (3, 7),
             [0, 4, 7, 3, 6, 2, 5, 1, 8, 9]),

            ([1, 2, 3, 4, 5, 6, 7],
             [4, 2, 7, 1, 3, 5, 6], (1, 3),
             [7, 2, 3, 4, 1, 5, 6]),

            ([0, 2, 4, 3, 5, 1, 0],
             [0, 4, 1, 2, 3, 5, 0], (3, 5),
             [0, 4, 2, 3, 5, 1, 0])
        ]

        # No instance loaded so we cant calculate distance
        mock_dist.return_value = 0

        for p1, p2, subpath, expected in data:
            with self.subTest(p1=p1, p2=p2, subpath=subpath):
                mock_rand_subpath.return_value = subpath
                self.gasolver.tsp.dimension = len(p1) - 1
                parent1 = Path(path=p1)
                parent2 = Path(path=p2)
                child = self.gasolver._crossover_ox(parent1, parent2)
                self.assertListEqual(child.get_path(), expected)
