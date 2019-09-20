from math import inf

from tspvisual.solver import Solver
from tspvisual.tsp import TSP, Path


class GreedySolver(Solver):
    """Greedy solver for TSP.
    """

    name = 'Greedy'
    properties = []

    def solve(self, tsp):
        # Make sure given argument is of correct type
        if not isinstance(tsp, TSP):
            raise TypeError('solve() argument has to be of type \'TSP\'')
        self.tsp = tsp

        # Path will always start and end in 0
        path = Path(self.tsp.dimension + 1)
        path[0] = path[-1] = 0

        # For each stop except the first and last one
        for i in range(1, len(path) - 1):
            prev = path[i - 1]
            min_dist = inf

            # Check all connections to different cities
            for j in range(self.tsp.dimension):
                # Skip cities that already are in path
                if path.in_path(j, i):
                    continue

                # Keep the new distance if it's lower than current minimum
                new_dist = self.tsp.dist(prev, j)
                if new_dist < min_dist:
                    min_dist = new_dist
                    path[i] = j

        path.distance = self.tsp.path_dist(path)
        return path
