from copy import deepcopy
from math import inf

from tspvisual.solver import Solver
from tspvisual.tsp import Path


class DPSolver(Solver):
    """Dynamic programming (Held-Karp algorithm) solver for TSP.
    """

    def __init__(self, tsp):
        super(DPSolver, self).__init__(tsp)
        self.sp_num = 1 << self.tsp.dimension
        self.FULL_SET = self.sp_num - 1
        self.mem = [[-1 for _ in range(self.sp_num)]
                    for _ in range(self.tsp.dimension)]
        self.pred = deepcopy(self.mem)

    def held_karp(self, city, visited):
        """Implements recursive Held-Karp algorithm.

        :param int city: Current city number.
        :param int visited: Set of visited cities.
        :return: Distance of minimal found path.
        :rtype: int
        """

        # If all nodes are already visited
        if visited == self.FULL_SET:
            return self.tsp.dist(city, 0)

        # If this combination of current and visited cities is already memoized
        if self.mem[city][visited] != -1:
            return self.mem[city][visited]

        # Current minimal distance and city
        min_dist, min_city = inf, -1

        # Iterate through all unvisited cities
        for i in range(self.tsp.dimension):
            # Current mask
            mask = 1 << i

            # If i city wasn't visited
            if not visited & mask:
                # Mask current node and enter the next recursion level
                dist = self.tsp.dist(city, i) \
                     + self.held_karp(i, visited | mask)

                # Keep the new distance if it's shorter than current minimum
                if dist < min_dist:
                    min_dist, min_city = dist, i

        self.pred[city][visited] = min_city
        self.mem[city][visited] = min_dist
        return min_dist

    def solve(self):
        # Result path
        res_path = Path(self.tsp.dimension + 1)
        # Run Held-Karp algorithm
        res_path.distance = self.held_karp(0, 1)

        # Retrace path of the recursion using predecessors array
        city, visited, i = 0, 1, 0
        while True:
            res_path.set_stop(i, city)
            city = self.pred[city][visited]
            if city == -1:
                break
            visited = visited | (1 << city)
            i = i + 1

        res_path.set_stop(i + 1, 0)
        return res_path
