import abc
from collections import namedtuple

Property = namedtuple('Property', 'name field type default')


class Solver(abc.ABC):
    """TSP solver base class. It stores current TSP instance and defines
    abstract solve method
    """

    def __init__(self, tsp=None):
        self.tsp = tsp

    @property
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
    def solve(self):
        """Solves current TSP instance.

        :return: Best found path.
        :rtype: Path
        """

        raise NotImplementedError('Solvers must implement solve method.')
