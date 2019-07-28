from math import inf

from tspvisual.solver import Solver
from tspvisual.tsp import Path


class GreedySolver(Solver):
    """Greedy solver for TSP.
    """

    def solve(self):
        # Path will always start and end in 0
        path = Path(self.tsp.dimension + 1)
        path.set_stop(0, 0)
        path.set_stop(-1, 0)

        # For each stop except the first and last one
        for i in range(1, path.length - 1):
            prev = path.get_stop(i - 1)
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
                    path.set_stop(i, j)

        path.distance = self.tsp.path_dist(path)
        return path
