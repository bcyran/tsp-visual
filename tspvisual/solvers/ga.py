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

    def _init_population(self):
        """Initializes population by creating specified number of random paths.
        """

        self._population.clear()
        for _ in range(self.population_size):
            path = Path(self.tsp.dimension + 1)
            path.path = list(range(self.tsp.dimension)) + [0]
            path.shuffle(1, -1)
            path.distance = self.tsp.path_dist(path)
            self._population.append(path)

        self._population.sort(key=lambda p: p.distance)

    def _selection(self):
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
        for _ in range(self.population_size - self.elite_size):
            # Spin the roulette
            roulette = random()

            # Find first path with probability higher than roulette number
            for i, row in df.iterrows():
                if roulette <= row['prob']:
                    self._mating_pool.append(self._population[i])
                    break

    def _crossover(self, parent1, parent2):
        # TODO: Implement
        pass

    def _crossover_ox(self, parent1, parent2):
        """Performs order crossover to create a child path from two given
        parent paths.

        :param Path parent1: First parent path.
        :param Path parent2: Second parent path.
        :return: Child path.
        :rtype: Path
        """

        # Initial child path
        child = Path(len(parent1))

        # Copy random subpath from parent 1 to child
        start, end = self._rand_subpath()
        subpath = parent1.path[start:end+1]
        child[start:end+1] = subpath

        # Fill in rest of the cities from parent2 starting after the end
        # of copied subpath
        child_pos = parent_pos = end + 1
        while child_pos != start:
            # Look for city that is not in copied subpath, wrap search
            # to the beginning after reaching end
            while parent2[parent_pos] in subpath:
                parent_pos = (parent_pos + 1) % len(parent1)

            # Set stop in child path
            child[child_pos] = parent2[parent_pos]
            # Increment child position and wrap to the beginning if necessary
            child_pos = (child_pos + 1) % len(parent1)
            parent_pos = (parent_pos + 1) % len(parent1)

        child.distance = self.tsp.path_dist(child)
        return child

    def _crossover_pmx(self, parent1, parent2):
        """Performs partially matched crossover to create a child path from two
        given parent paths.

        :param Path parent1: First parent path.
        :param Path parent2: Second parent path.
        :return: Child path.
        :rtype: Path
        """

        # Starting path
        child = Path(len(parent1))

        # Copy random subpath from parent 1 to child and create mapping
        start, end = self._rand_subpath()
        child[start:end+1] = parent1[start:end+1]

        # Create mapping
        mapping = dict(zip(parent1[start:end+1], parent2[start:end+1]))

        # Copy stops from parent 2 to child using mapping if necessary
        child_pos = 0
        while child_pos < self.tsp.dimension + 1:
            # Skip already filled subpath
            if start <= child_pos <= end:
                child_pos = end + 1
                continue

            # Get city at current stop in parent 2
            city = parent2[child_pos]

            # Trace mapping if it exists
            while city in mapping:
                city = mapping[city]

            # Set stop in the child path
            child[child_pos] = city
            child_pos += 1

        child.distance = self.tsp.path_dist(child)
        return child

    def _crossover_nwox(self, parent1, parent2):
        """Performs non wrapping order crossover to create a child path from
        two given parents paths.

        :param Path parent1: First parent path.
        :param Path parent2: Second parent path.
        :return: Child path.
        :rtype: Path
        """

        # Initial child path
        child = Path(self.tsp.dimension + 1)

        # Copy random subpath from parent 1 to child
        start, end = self._rand_subpath()
        child[start:end+1] = parent1[start:end+1]

        # Fill in child's empty slots with cities from parent 2 in order
        parent_pos = child_pos = 0
        while parent_pos < self.tsp.dimension + 1:
            # Skip already filled subpath
            if start <= child_pos <= end:
                child_pos = end + 1
                continue

            # Get city from parent path
            city = parent2[parent_pos]

            if child.in_path(city):
                # If this city is already in child path then go to next one
                parent_pos += 1
                continue
            else:
                # Otherwise add it to child path and go to next
                child[child_pos] = city
                child_pos += 1
                parent_pos += 1

        # Add return to 0 if last stop is empty
        child[-1] = child[-1] if child[-1] != -1 else 0

        child.distance = self.tsp.path_dist(child)
        return child

    def _breeding(self):
        # TODO: Implement
        pass

    def _mutation(self):
        # TODO: Implement
        pass

    def _rand_subpath(self):
        """Randomly chooses two stops in path creating random subpath.

        :return: Subpath's start and end indices.
        :rtype: tuple
        """

        i = j = randint(1, self.tsp.dimension - 1)

        while i == j:
            j = randint(1, self.tsp.dimension - 1)

        return min(i, j), max(i, j)
