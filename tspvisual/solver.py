import abc
from collections import namedtuple

Property = namedtuple('Property', 'name field type default')


class Solver(abc.ABC):
    """TSP solver base class. Defines interface for getting solver name and
    properties as well as solving TSP instances.
    """

    @abc.abstractmethod
    def name(self):
        """Returns name of the solver.

        :return: Name.
        :rtype: string
        """

        raise NotImplementedError('Solvers must have name property.')

    @property
    @abc.abstractmethod
    def properties(self):
        """Returns list of solver properties.

        :return: List of properties.
        :rtype: list
        """

        raise NotImplementedError('Solvers must implement properties method.')

    @abc.abstractmethod
    def solve(self, tsp):
        """Solves given TSP instance.

        :param TSP tsp: TSP instance to solve.
        :return: Best found path.
        :rtype: Path
        """

        raise NotImplementedError('Solvers must implement solve method.')
