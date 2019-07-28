from math import sqrt


class TSPLib:
    """Simple parser for TSPLIB files.

    This parser currently supports only TSP instances which EDGE_WEIGHT_TYPE
    equal to EUC_2D.
    """

    _INT_PROPERTIES = ['DIMENSION', 'CAPACITY']

    def __init__(self, file):
        self._lines = []
        self.specification = {}
        self.coords = []

        if file:
            self.load(file)

    def load(self, file):
        """Loads lines from file for parsing.

        :param string file: File to load.
        """
        with open(file, 'r') as f:
            self._lines = f.read().splitlines()

        self._parse()

    def _parse(self):
        """Parse lines from loaded file.
        """

        for i in range(len(self._lines)):
            line = self._lines[i]
            if ':' in line:
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                value = int(value) if key in self._INT_PROPERTIES else value
                self.specification[key] = value
            elif line.startswith('NODE_COORD_SECTION'):
                i = self._parse_coords(i + 1)

        del self._lines

    def _parse_coords(self, i):
        """Parse contents of NODE_COORD_SECTION.

        :param int i: Index of first line containing coordinates.
        :return: Index of first line after coordinates section.
        :rtype: int
        """

        coords_end = i + self.specification['DIMENSION']
        for i in range(i, coords_end):
            line = self._lines[i]
            _, x, y = line.split()
            self.coords.append((float(x), float(y)))

        return i

    def weight(self, i, j):
        """Calculates weight of the edge between specified nodes basing on
        EDGE_WEIGHT_TYPE property.

        :param int i: Index of the first node.
        :param int j: Index of the second node.
        :return: Weight of the edge.
        :rtype: int
        """

        if self.specification['EDGE_WEIGHT_TYPE'] == 'EUC_2D':
            return self._w_euc_2d(i, j)
        else:
            raise TypeError('Unsupported edge weight type.')

    def _w_euc_2d(self, i, j):
        """Calculates euclidean distance between nodes.
        """

        xd = self.coords[i][0] - self.coords[j][0]
        yd = self.coords[i][1] - self.coords[j][1]
        return int(sqrt(xd ** 2 + yd ** 2))
