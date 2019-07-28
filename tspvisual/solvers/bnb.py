from copy import deepcopy
from math import inf

from tspvisual.solver import Solver
from tspvisual.tsp import Path


class BnBSolver(Solver):
    """Branch-and-bound solver for TSP
    """

    def solve(self):
        # Working path
        path = Path(self.tsp.dimension + 1)
        path.set_stop(-1, 0)
        # Minimal path and distance
        min_path, min_dist = Path(self.tsp.dimension + 1), inf
        # Nodes list (used as a stack)
        stack = []

        # Add starting city (0) to the stack
        stack.append((0, 0, 0))

        while len(stack) > 0:
            # Get node from the top of the stack
            cur_node = stack.pop()
            city, dist, level = cur_node
            # Update current path with this node
            path.set_stop(level, city)
            # This is the level of all children of this node
            next_level = level + 1

            # If it's the last level of the tree
            if level == self.tsp.dimension - 1:
                # Distance of full path with return to 0
                new_dist = dist + self.tsp.dist(city, 0)
                # Keep it if it's better than the current minimum
                if new_dist < min_dist:
                    min_path, min_dist = deepcopy(path), new_dist
                else:
                    continue

            # Iterate through all cities
            for i in range(self.tsp.dimension):
                # Skip current city itself, its predecessors and starting city
                if i == city or path.in_path(i, next_level) or i == 0:
                    continue

                # Skip this node if its distance is greater than min path
                next_dist = dist + self.tsp.dist(city, i)
                if next_dist >= min_dist:
                    continue

                # If it's valid node push it onto stack
                stack.append((i, next_dist, next_level))

        min_path.distance = self.tsp.path_dist(min_path)
        return min_path
