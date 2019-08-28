from enum import Enum
from random import randint, random

import pandas as pd

from tspvisual.solver import Solver
from tspvisual.tsp import Path


class GASolver(Solver):
    """Genetic Algorithm solver for TSP.
    """

    Crossover = Enum('Crossover', 'OX PMX NWOX')

    def __init__(self, tsp):
        super(GASolver, self).__init__(tsp)
        self.population_size = 80
        self.elite_size = 30
        self.mutation_rate = 0.05
        self.generations = 2000
        self.run_time = 0
        self.crossover_type = self.Crossover.NWOX
        self._population = []
        self._mating_pool = []

    def solve(self):
        pass

    def init_population(self):
        """Initializes population by creating specified number of random paths.
        """

        self._population.clear()
        for _ in self.population_size:
            path = Path(self.tsp.dimension + 1)
            path.set_path(list(range(self.tsp.dimension)) + [0])
            path.shuffle(1, -1)
            path.distance = self.tsp.path_dist(path)
            self._population.append(path)

        self._population.sort(key=lambda p: p.distance)

    def selection(self):
        """Fills mating pool with individuals chosen using elitism
        and Roulette Wheel Selection.
        """

        self._mating_pool.clear()
        self._mating_pool = self._population[:self.elite_size]

        # Create distances data frame, calculate cumulative sum and probability
        df = pd.DataFrame(map(lambda p: p.distance, self._population),
                          columns=['distance'])
        df['cum_sum'] = df.distance.cumsum()
        df['prob'] = df.cum_sum / df.distance.sum()

        # For each free place in mating pool
        for _ in self.population_size - self.elite_size:
            # Spin the roulette
            roulette = random()

            # Find first path with probability higher than roulette number
            for i, row in df.iterrows():
                if roulette <= row['prob']:
                    self._mating_pool.append(self._population[i])
                    break

    def crossover(self):
        # TODO: Implement
        pass

    def crossover_ox(self):
        # TODO: Implement
        pass

    def crossover_pmx(self):
        # TODO: Implement
        pass

    def crossover_nwox(self):
        # TODO: Implement
        pass

    def breeding(self):
        # TODO: Implement
        pass

    def mutation(self):
        # TODO: Implement
        pass

    def rand_subpath(self):
        """Randomly chooses two stops in path creating random subpath.

        :return: Subpath's start and end indices.
        :rtype: tuple
        """

        i = j = randint(1, self.tsp.dimension - 1)

        while i == j:
            j = randint(1, self.tsp.dimension - 1)

        return i, j
