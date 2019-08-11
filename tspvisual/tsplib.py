from math import sqrt


class TSPLib:
    """Simple parser for TSPLIB files.

    This parser currently supports only TSP instances which EDGE_WEIGHT_TYPE
    equal to EUC_2D.
    """

    # Names of properties of integer type (all others are strings)
    _INT_PROPERTIES = ['DIMENSION', 'CAPACITY']

    def __init__(self, file):
        self._lines = []
        self.specification = {}
        self.coords = []
        self.weights = None

        if file:
            self.load(file)

    def load(self, file):
        """Loads lines from file, creates an iterator and starts parsing.

        :param string file: File to load.
        """

        with open(file, 'r') as f:
            self._lines = iter(f.read().splitlines())

        self._parse()

    def _parse(self):
        """Parses lines from loaded file.
        """

        for line in self._lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                value = int(value) if key in self._INT_PROPERTIES else value
                self.specification[key] = value
            elif line.startswith('NODE_COORD_SECTION'):
                self._parse_coords()
            elif line.startswith('EDGE_WEIGHT_SECTION'):
                self._parse_weights()

        del self._lines

    def _parse_coords(self):
        """Parses contents of NODE_COORD_SECTION.
        """

        for line in self._lines:
            try:
                _, x, y = line.split()
            except ValueError:
                break

            try:
                self.coords.append((float(x), float(y)))
            except ValueError:
                raise ValueError('Incorrect node coordinates')

    def _parse_weights(self):
        """Parses contents of EDGE_WEIGHT_SECTION.
        """

        # Initialize weights matrix
        self.weights = [[-1 for _ in range(self.specification['DIMENSION'])]
                        for _ in range(self.specification['DIMENSION'])]

        for (row, col), weight in zip(self._cells(), self._weights()):
            self.weights[row][col] = weight

    def _weights(self):
        """Generates consecutive edge weights read from the file.
        """

        for line in self._lines:
            for value in line.split():
                try:
                    yield int(value)
                except ValueError:
                    break

    def _cells(self):
        """Generates consecutive matrix cells coordinates.
        """

        # Matrix size
        size = self.specification['DIMENSION']
        # Edge weight format
        edge_format = self.specification['EDGE_WEIGHT_FORMAT'].split('_')
        # Matrix type: FULL, UPPER, LOWER
        matrix = edge_format[0]

        # Data direction: ROW, COL; diagonal offset
        offset = 0
        if matrix != 'FULL':
            if edge_format[1] in ['ROW', 'COL']:
                direction = edge_format[1]
                # No diagonal entries, matrix needs to be offseted by 1
                offset = 1
            else:
                direction = edge_format[2]

        # Initial position in the matrix
        row = col = -1

        # Increments `b`. If `b` is larger than `bound` increments `a` and
        # sets `b` to `ret`.
        def calc(a, b, bound, ret):
            a = max(a, 0)
            b += 1
            if b > bound:
                a += 1
                b = ret
            return a, max(b, ret)

        # Generate the coordinates
        while True:
            if matrix == 'FULL':
                row, col = calc(row, col, size - 1, 0)
            elif matrix == 'UPPER' and direction == 'ROW':
                row, col = calc(row, col, size - 1, row + 1 + offset)
            elif matrix == 'LOWER' and direction == 'COL':
                col, row = calc(col, row, size - 1, col + 1 + offset)
            elif matrix == 'LOWER' and direction == 'ROW':
                row, col = calc(row, col, max(row - offset, 0), 0)
            elif matrix == 'UPPER' and direction == 'COL':
                col, row = calc(col, row, max(row - offset, 0), 0)

            # End when all coordinates are generated
            if row >= size or col >= size:
                break

            yield row, col

    def weight(self, i, j):
        """Calculates weight of the edge between specified nodes basing on
        EDGE_WEIGHT_TYPE property.

        :param int i: Index of the first node.
        :param int j: Index of the second node.
        :return: Weight of the edge.
        :rtype: int
        """

        if self.specification['EDGE_WEIGHT_TYPE'] == 'EXPLICIT':
            return (self.weights[i][j] if self.weights[i][j] != -1 else
                    self.weights[j][i])
        elif self.specification['EDGE_WEIGHT_TYPE'] == 'EUC_2D':
            return self._w_euc_2d(i, j)
        else:
            raise TypeError('Unsupported edge weight type.')

    def _w_euc_2d(self, i, j):
        """Calculates euclidean distance between nodes.
        """

        xd = self.coords[i][0] - self.coords[j][0]
        yd = self.coords[i][1] - self.coords[j][1]
        return self._nint(sqrt(xd ** 2 + yd ** 2))

    @staticmethod
    def _nint(x):
        """Rounds number to the nearest integer.

        :param float x: Number to round.
        :return: Nearest integer.
        :rtype int:
        """

        return int(x + 0.5)
