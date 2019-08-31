from enum import Enum
from random import shuffle

from tspvisual.tsplib import TSPLib


class TSP:
    """Internal representation of a Travelling Salesman Problem instance.

    Contains a few properties (name, type, comment, dimension), coordinates
    of cities and distance matrix.
    """

    def __init__(self, file=None):
        self._tsplib = None
        self.name = None
        self.comment = None
        self.dimension = 0
        self.coords = []
        self.distances = []

        if file is not None:
            self.load(file)

    def load(self, file):
        """Load TSPLIB file and read necessary data.

        :param string file: File to load.
        """

        self._tsplib = TSPLib(file)

        if self._tsplib.specification['TYPE'] not in ['TSP', 'ATSP']:
            raise TypeError('Unsupported problem. Only TSP and ATSP instances '
                            'are supported.')

        self.name = self._tsplib.specification['NAME']
        self.comment = self._tsplib.specification['COMMENT']
        self.dimension = self._tsplib.specification['DIMENSION']
        self.coords = self._tsplib.coords

        self._calc_distances()
        del self._tsplib

    def _calc_distances(self):
        """Calculate distance matrix using TSPLib weight function.
        """

        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append(self._tsplib.weight(i, j))
            self.distances.append(row)

    def dist(self, i, j):
        """Returns the distance between two cities.

        :param int i: Index of the first city.
        :param int j: Index of the second city.
        :return: The distance.
        :rtype: int
        """

        return self.distances[i][j]

    def path_dist(self, path):
        """Calculates total distance of a given path.

        :param Path path: Path to calculate distance of.
        :return: The distance of a path.
        :rtype: int
        """

        total = 0

        for i in range(path.length - 1):
            total += self.dist(path.get_stop(i), path.get_stop(i + 1))

        return total


class Path:
    """Representation of a path in TSP.

    Contains length of the path (number of visited cities), list of
    a consecutive city numbers and optionally path distance.

    List of stops should be accessed only using `set_stop`, `get_stop`,
    `set_path` and `get_path` methods to avoid incorrect path length due to
    off-by-one errors.
    """

    # Available path neighbourhood types
    Neighbourhood = Enum('Neighbourhood', 'SWAP INSERT INVERT')

    def __init__(self, length=0, path=None):
        self._path = [-1] * length if path is None else path
        self.length = length if path is None else len(path)
        self.distance = -1

    def set_stop(self, index, city):
        """Sets specified stop in the path to given city number.

        :param int index: Index of the stop.
        :param int city: City number.
        """

        self._path[index] = city

    def get_stop(self, index):
        """Returns city number in the specified stop.

        :param int index: Index of the stop.
        :return: City number.
        :rtype: int
        """

        return self._path[index]

    def set_path(self, path):
        """Sets the entire path to given sequence.

        :param list path: List of consecutive stops.
        """

        if len(path) != self.length:
            raise ValueError('Incorrect path length.')

        self._path = path

    def get_path(self):
        """Returns city number sequence.
        """

        return self._path

    def shuffle(self, i, j):
        """Shuffles specified slice of the path.

        :param int i: Index of the first stop in the slice.
        :param int j: Index of the last stop in the slice.
        """

        part = self._path[i:j]
        shuffle(part)
        self._path[i:j] = part

    def in_path(self, city, limit=None):
        """Checks whether specified city is in the first n elements of the path.

        :param int city: City to look for.
        :param int limit: Number of path stops to search.
        :return: True if the city was found.
        :rtype: bool
        """

        limit = self.length if limit is None else limit
        for stop in self._path[:limit]:
            if stop == city:
                return True

        return False

    def swap(self, i, j):
        """Swaps cities at a specified path stops.

        :param int i: Index of the first stop.
        :param int j: Index of the second stop.
        """

        self._path[i], self._path[j] = self._path[j], self._path[i]

    def insert(self, i, j):
        """Inserts one stop in the place of the other, shifts other stops.

        :param int i: Index of the first stop.
        :param int j: Index of the second stop.
        """

        new_j = self._path[i]

        while i > j:
            self._path[i] = self._path[i - 1]
            i = i - 1

        while i < j:
            self._path[i] = self._path[i + 1]
            i = i + 1

        self._path[j] = new_j

    def invert(self, i, j):
        """Reverses order of stops of specified slice of the path.

        :param int i: Index of the first stop.
        :param int j: Index of the second stop.
        """

        if i > j:
            i, j = j, i

        while i < j:
            self.swap(i, j)
            i = i + 1
            j = j - 1

    def move(self, neigh, i, j):
        """Performs move specified by a given neighbourhood type on i, j stops
        in this path.

        :param Neighbourhood neigh: Neighbourhood type.
        :param int i: Index of the first stop.
        :param int j: Index of the second stop.
        """

        moves = {
            self.Neighbourhood.SWAP: self.swap,
            self.Neighbourhood.INSERT: self.insert,
            self.Neighbourhood.INVERT: self.invert
        }

        moves[neigh](i, j)

    def __str__(self):
        string = ''
        for stop in self._path:
            string += f'{stop}, '

        string = string[:-2] + f' ({self.distance})'

        return string
