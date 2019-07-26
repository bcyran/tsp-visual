from math import sqrt

int_properties = ['DIMENSION', 'CAPACITY']


class TSPLib:
    """Simple parser for TSPLIB files.

    This parser currently supports only TSP instances which EDGE_WEIGHT_TYPE
    equal to EUC_2D.
    """

    def __init__(self, file):
        self.lines = []
        self.specification = {}
        self.coords = []

        if file:
            self.load(file)

    def load(self, file):
        """Loads lines from file for parsing.

        :param string file: File to load.
        """
        with open(file, 'r') as f:
            self.lines = f.read().splitlines()

        self.parse()

    def parse(self):
        """Parse lines from loaded file.
        """

        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            if ':' in line:
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                value = int(value) if key in int_properties else value
                self.specification[key] = value
            elif line.startswith('NODE_COORD_SECTION'):
                i = self.parse_coords(i + 1)
            i = i + 1

        del self.lines

    def parse_coords(self, i):
        """Parse contents of NODE_COORD_SECTION.

        :param int i: Index of first line containing coordinates.
        :return: Index of first line after coordinates section.
        :rtype: int
        """

        coords_end = i + self.specification['DIMENSION']
        while i < coords_end:
            line = self.lines[i]
            _, x, y = line.split()
            self.coords.append((float(x), float(y)))
            i = i + 1

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
            return self.w_euc_2d(i, j)
        else:
            raise TypeError('Unsupported edge weight type.')

    def w_euc_2d(self, i, j):
        """Calculates euclidean distance between nodes.
        """

        xd = self.coords[i][0] - self.coords[j][0]
        yd = self.coords[i][1] - self.coords[j][1]
        return int(sqrt(xd ** 2 + yd ** 2))
