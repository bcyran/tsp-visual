import time
from copy import deepcopy
from itertools import product
from math import inf

from tspvisual.solver import Property, Solver
from tspvisual.solvers.greedy import GreedySolver
from tspvisual.tsp import TSP, Path


class TSSolver(Solver):
    """Tabu Search solver for TSP.
    """

    name = "Tabu Search"
    properties = [
        Property('Iterations', 'iterations', int, 1000),
        Property('Cadence', 'cadence', int, 18),
        Property('Neighbourhood', 'neighbourhood', Path.Neighbourhood,
                 'INVERT'),
        Property('Reset threshold', 'reset_threshold', int, 45),
        Property('Stop threshold', 'stop_threshold', int, 450),
        Property('Run time', 'run_time', int, 0)
    ]

    def __init__(self):
        self.iterations = 1000
        self.cadence = 18
        self.neighbourhood = Path.Neighbourhood.INVERT
        self.reset_threshold = 45
        self.stop_threshold = 450
        self.run_time = 0

    def _setup(self):
        """Sets up instance-specific data structures.
        """

        self._tabu = [[0 for _ in range(self.tsp.dimension)]
                      for _ in range(self.tsp.dimension)]

    def solve(self, tsp):
        # Make sure given argument is of correct type
        if not isinstance(tsp, TSP):
            raise TypeError('solve() argument has to be of type \'TSP\'')
        self.tsp = tsp
        self._setup()

        # Starting path from a greedy solver
        greedy_solver = GreedySolver(self.tsp)
        cur_path = greedy_solver.solve()
        # Current minimum path
        min_path = deepcopy(cur_path)

        # Counter of non-improving iterations since last reset
        reset_counter = 0
        # Counter of iterations since last improvement
        stop_counter = 0
        # Timestamp when search should be ended
        end_time = self._millis() + self.run_time

        for _ in range(self.iterations):
            # Find best neighbour of the current path
            cur_path = self._min_neighbour(cur_path)

            if cur_path.distance < min_path.distance:
                # Keep this neighbour if it's better than current minimum
                min_path = deepcopy(cur_path)
                reset_counter, stop_counter = 0, 0
            else:
                # Otherwise increment reset and stop counters
                reset_counter += 1
                stop_counter += 1

                # Terminate search if threshold of iterations is exceeded
                if not self.run_time and self.stop_threshold and \
                        stop_counter >= self.stop_threshold:
                    break

            self._update_tabu()

            # Terminate search after exceeding specified runtime
            if self.run_time and self._millis() > end_time:
                break

        return min_path

    def _min_neighbour(self, path):
        """Finds shortest neighbour of the given path.

        :param Path path: Path whose neighbourhood will be searched.
        """

        min_neigh = Path(self.tsp.dimension + 1)
        min_neigh.distance = inf
        best_move = ()

        # Iterate through all possible 2-city moves
        for i, j in product(range(1, self.tsp.dimension), repeat=2):
            # Skip redundant moves
            if self.neighbourhood == path.Neighbourhood.SWAP or \
                    self.neighbourhood == path.Neighbourhood.INVERT:
                if j <= i:
                    continue
            if self.neighbourhood == path.Neighbourhood.INSERT:
                if j == i + 1 or j == i - 1:
                    continue

            # Skip tabu moves
            if self._tabu[i][j]:
                continue

            # Perform the move
            cur_neigh = deepcopy(path)
            cur_neigh.move(self.neighbourhood, i, j)
            cur_neigh.distance = self.tsp.path_dist(cur_neigh)

            # If resulting path is better than current minimum keep its
            # length and move indexed
            if cur_neigh.distance < min_neigh.distance:
                min_neigh, best_move = cur_neigh, (i, j)

        # Tabu found move
        if best_move:
            self._tabu[best_move[0]][best_move[1]] = self.cadence
            self._tabu[best_move[1]][best_move[0]] = self.cadence

        # In small instances it can happen all neighbours are already on tabu
        # list, if that happens we cannot return an empty path
        return min_neigh if min_neigh.distance != inf else path

    def _update_tabu(self):
        """Updates tabu list by decrementing all non-zero entries.
        """

        for i, j in product(range(self.tsp.dimension), repeat=2):
            if self._tabu[i][j] > 0:
                self._tabu[i][j] -= 1

    def _millis(self):
        """Returns current timestamp in milliseconds.

        :return: Time since epoch in milliseconds.
        :rtype: int
        """

        return int(round(time.time() * 1000))
