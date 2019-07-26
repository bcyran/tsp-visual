from tspvisual.tsp import Path


class Solver:
    """TSP solver base class. It stores current TSP instance and defines
    abstract solve method
    """

    def __init__(self, tsp=None):
        self.tsp = tsp

    def solve(self):
        """Solve current TSP instance.

        :return: Best found path.
        :rtype: Path
        """

        raise NotImplementedError()
