from copy import deepcopy
from itertools import permutations

from tspvisual.solver import Solver
from tspvisual.tsp import TSP, Path


class BFSolver(Solver):
    """Brute force solver for TSP.
    """

    name = 'Brute Force'
    properties = []

    def solve(self, tsp):
        # Make sure given argument is of correct type
        if not isinstance(tsp, TSP):
            raise TypeError('solve() argument has to be of type \'TSP\'')
        self.tsp = tsp

        # Create starting path: 0, 1, 2, ..., 0, this path will be permuted
        path = Path(self.tsp.dimension + 1)
        path.path = list(range(len(path) - 1)) + [0]
        path.distance = self.tsp.path_dist(path)
        # Best path
        min_path = deepcopy(path)
        # Create permutations skipping the last stop (return to 0)
        perms = permutations(path.path[1:-1])

        # Loop through all permutations to find the shortest path
        for perm in perms:
            path.path = [0] + list(perm) + [0]
            path.distance = self.tsp.path_dist(path)

            if path.distance < min_path.distance:
                min_path = deepcopy(path)

        return min_path
