from tspvisual.tsplib import TSPLib


class TSP:
    """Internal representation of a Travelling Salesman Problem instance.

    Contains a few properties (name, type, comment, dimension), coordinates
    of cities and distance matrix.
    """

    def __init__(self, file):
        self.tsplib = None
        self.name = None
        self.comment = None
        self.dimension = 0
        self.coords = []
        self.distances = []

        if file is not None:
            self.load(file)

    def load(self, file):
        """Load TSPLIB file  and read necessary data.

        :param string file: File to load.
        """

        self.tsplib = TSPLib(file)

        if self.tsplib.specification['TYPE'] not in ['TSP', 'ATSP']:
            raise TypeError('Unsupported problem. Only TSP and ATSP instances '
                            'are supported.')

        self.name = self.tsplib.specification['NAME']
        self.comment = self.tsplib.specification['COMMENT']
        self.dimension = self.tsplib.specification['DIMENSION']
        self.coords = self.tsplib.coords

        self.calc_distances()
        del self.tsplib

    def calc_distances(self):
        """Calculate distance matrix using TSPLib weight function.
        """

        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append(self.tsplib.weight(i, j))
            self.distances.append(row)

    def dist(self, i, j):
        """Returns the distance between two cities.

        :param int i: Index of the first city.
        :param int j: Index of the second city.
        :return: The distance.
        :rtype: int
        """

        return self.distances[i][j]


class Path:
    """Representation of a path in TSP.

    Contains length of the path (number of visited cities), list of
    a consecutive city numbers and optionally path distance.
    """

    def __init__(self, length=0):
        self.length = length
        self.path = [-1 for _ in range(length)]
        self.distance = -1

    def set_stop(self, index, city):
        """Sets specified stop in the path to given city number.

        :param int index: Index of the stop.
        :param int city: City number.
        """

        self.path[index] = city

    def get_stop(self, index):
        """Returns city number in the specified stop.

        :param int index: Index of the stop.
        :return: City number.
        :rtype: int
        """

        return self.path[index]

    def in_path(self, city, limit=None):
        """Checks whether specified city is in the first n elements of the path.

        :param int city: City to look for.
        :param int limit: Number of path stops to search.
        :return: True if the city was found.
        :rtype: bool
        """

        limit = self.length if limit is None else limit
        for stop in self.path[:limit]:
            if stop == city:
                return True

        return False

    def __str__(self):
        string = ''
        for stop in self.path:
            string += f'{stop}, '

        return string[:-2]
