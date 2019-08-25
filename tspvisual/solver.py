import abc


class Solver(abc.ABC):
    """TSP solver base class. It stores current TSP instance and defines
    abstract solve method
    """

    def __init__(self, tsp=None):
        self.tsp = tsp

    @abc.abstractmethod
    def solve(self):
        """Solve current TSP instance.

        :return: Best found path.
        :rtype: Path
        """

        raise NotImplementedError('Solvers must implement solve method.')
