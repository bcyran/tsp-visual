import time
from copy import deepcopy
from math import exp, log
from random import randint, random

from tspvisual.solver import Property, Solver, SolverState
from tspvisual.tsp import TSP, Path


class SASolver(Solver):
    """Simulated annealing solver for TSP.
    """

    name = 'Simulated Annealing'
    properties = [
        Property('Initial temperature', 'init_temp', float, 100),
        Property('End temperature', 'end_temp', float, 0.1),
        Property('Cooling rate', 'cooling_rate', float, 0.01),
        Property('Neighbourhood', 'neighbourhood', Path.Neighbourhood,
                 'INVERT'),
        Property('Run time [ms]', 'run_time', int, 0)
    ]

    def __init__(self):
        self.init_temp = 100
        self.end_temp = 0.1
        self.cooling_rate = 0.01
        self.neighbourhood = Path.Neighbourhood.INVERT
        self.run_time = 0

    def solve(self, tsp, steps=True):
        # Make sure given argument is of correct type
        if not isinstance(tsp, TSP):
            raise TypeError('solve() argument has to be of type \'TSP\'')
        self.tsp = tsp

        # Total number of iterations or time for calculating progress
        if steps:
            if not self.run_time:
                total = log(self.end_temp / self.init_temp,
                            1 - self.cooling_rate)
            else:
                total = self.run_time
            current = 0

        # Start with random path
        cur_path = Path(self.tsp.dimension + 1)
        cur_path.path = list(range(len(cur_path) - 1)) + [0]
        cur_path.shuffle(1, -1)
        cur_path.distance = self.tsp.path_dist(cur_path)

        # And set it as current minimum
        min_path = deepcopy(cur_path)

        # Timestamp when search should be ended
        end_time = self._millis() + self.run_time

        # Init temperature
        temp = self.init_temp
        # Repeat as long as system temperature is higher than minimum
        while True:
            # Update iteration counter ro time counterif running in step mode
            if steps:
                if not self.run_time:
                    current += 1
                else:
                    current = self.run_time - (end_time - self._millis())

            # Get random neighbour of current path
            new_path = self._rand_neigh(cur_path)

            # Difference between current and new path
            delta_dist = new_path.distance - cur_path.distance

            # If it's shorter or equal
            if delta_dist <= 0:
                # If it's shorter set it as current minimum
                if delta_dist < 0:
                    min_path = deepcopy(new_path)
                # Set new path as current path
                cur_path = deepcopy(new_path)
            elif exp(-delta_dist / temp) > random():
                # If path is longer accept it with random probability
                cur_path = deepcopy(new_path)

            # Cooling down
            temp *= 1 - self.cooling_rate

            # Terminate search after reaching end temperature
            if not self.run_time and temp < self.end_temp:
                break

            # Terminate search after exceeding specified runtime
            if self.run_time and self._millis() > end_time:
                break

            # Report current solver state
            if steps:
                yield SolverState(current / total * 100, deepcopy(new_path),
                                  deepcopy(min_path), False, None)

        yield SolverState(100, None, deepcopy(min_path), True, None)

    def _rand_neigh(self, path):
        """Generates random neighbour of a given path.

        :param Path path: Path to generate neighbour of.
        :return: Random neighbour.
        :rtype: Path
        """

        i = j = randint(1, self.tsp.dimension - 1)

        while i == j:
            j = randint(1, self.tsp.dimension - 1)

        neighbour = deepcopy(path)
        neighbour.move(self.neighbourhood, i, j)
        neighbour.distance = self.tsp.path_dist(neighbour)

        return neighbour

    def _millis(self):
        """Returns current timestamp in milliseconds.

        :return: Time since epoch in milliseconds.
        :rtype: int
        """

        return int(round(time.time() * 1000))
