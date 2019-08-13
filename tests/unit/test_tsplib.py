import unittest

from tspvisual.tsplib import Lines, TSPLib


class TestTSPLib(unittest.TestCase):

    def setUp(self):
        self.tsplib = TSPLib()

    def test_cells(self):
        formats = {
            'FULL_MATRIX':      [(0, 0), (0, 1), (0, 2), (0, 3),
                                 (1, 0), (1, 1), (1, 2), (1, 3),
                                 (2, 0), (2, 1), (2, 2), (2, 3),
                                 (3, 0), (3, 1), (3, 2), (3, 3)],

            'UPPER_ROW':                [(0, 1), (0, 2), (0, 3),
                                                 (1, 2), (1, 3),
                                                         (2, 3)],

            'LOWER_ROW':        [(1, 0),
                                 (2, 0), (2, 1),
                                 (3, 0), (3, 1), (3, 2)],

            'UPPER_DIAG_ROW':   [(0, 0), (0, 1), (0, 2), (0, 3),
                                         (1, 1), (1, 2), (1, 3),
                                                 (2, 2), (2, 3),
                                                         (3, 3)],

            'LOWER_DIAG_ROW':   [(0, 0),
                                 (1, 0), (1, 1),
                                 (2, 0), (2, 1), (2, 2),
                                 (3, 0), (3, 1), (3, 2), (3, 3)],

            'UPPER_COL':        [(0, 1),
                                 (0, 2), (1, 2),
                                 (0, 3), (1, 3), (2, 3)],

            'LOWER_COL':                [(1, 0), (2, 0), (3, 0),
                                                 (2, 1), (3, 1),
                                                         (3, 2)],

            'UPPER_DIAG_COL':   [(0, 0),
                                 (0, 1), (1, 1),
                                 (0, 2), (1, 2), (2, 2),
                                 (0, 3), (1, 3), (2, 3), (3, 3)],

            'LOWER_DIAG_COL':   [(0, 0), (1, 0), (2, 0), (3, 0),
                                         (1, 1), (2, 1), (3, 1),
                                                 (2, 2), (3, 2),
                                                         (3, 3)]
        }
        self.tsplib.specification['DIMENSION'] = 4

        for form, expected in formats.items():
            with self.subTest(form=form):
                self.tsplib.specification['EDGE_WEIGHT_FORMAT'] = form
                result = list(self.tsplib._cells())
                self.assertListEqual(result, expected,
                                     'Invalid cell coordinates sequence')

    def test_parse_spec(self):
        data = [
            ('NAME : gr17', 'NAME', 'gr17'),
            ('TYPE: TSP', 'TYPE', 'TSP'),
            ('DIMENSION    :    17', 'DIMENSION', 17)
        ]

        for line, key, expected in data:
            with self.subTest(line=line):
                self.tsplib.specification = {}
                self.tsplib._lines = Lines([line])
                self.tsplib._parse_spec()
                self.assertEqual(self.tsplib.specification[key], expected)

    def test_parse_coords(self):
        data = ['1 1 1', '2	2	5', '    3    4    9', '4 5.3 7',
                '5 9.7 10.1', 'EOF']
        expected = [(1, 1), (2, 5), (4, 9), (5.3, 7), (9.7, 10.1)]

        self.tsplib._lines = Lines(data)
        self.tsplib._parse_coords()

        self.assertListEqual(list(self.tsplib.coords), expected)
        self.assertEqual(self.tsplib._lines.current, data[-1])

    def test_parse_weights(self):
        data = ['0 2 3 4', ' 5    0 7 8', '9 10 0 12 13 14 15 0', 'EOF']
        expected = [[0,  2,  3,  4],
                    [5,  0,  7,  8],
                    [9,  10, 0, 12],
                    [13, 14, 15, 0]]

        self.tsplib.specification = {
            'DIMENSION': len(expected),
            'EDGE_WEIGHT_FORMAT': 'FULL_MATRIX'
        }
        self.tsplib._lines = Lines(data)
        self.tsplib._parse_weights()

        self.assertListEqual(self.tsplib.weights, expected)
        self.assertEqual(self.tsplib._lines.current, data[-1])

    def test_parse(self):
        data = ['DIMENSION : 3', 'EDGE_WEIGHT_FORMAT : FULL_MATRIX',
                'EDGE_WEIGHT_SECTION', '1 2 3 4 5', '6 7 8 9',
                'NODE_COORD_SECTION', '1 1 1', '2 4 5', '3 4.20 69.9', 'EOF']
        expected_spec = {'DIMENSION': 3, 'EDGE_WEIGHT_FORMAT': 'FULL_MATRIX'}
        expected_weigths = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected_coords = [(1, 1), (4, 5), (4.2, 69.9)]

        self.tsplib.specification = {}
        self.tsplib._lines = Lines(data)
        self.tsplib._parse()

        self.assertDictEqual(self.tsplib.specification, expected_spec)
        self.assertListEqual(self.tsplib.weights, expected_weigths)
        self.assertListEqual(self.tsplib.coords, expected_coords)

    def test_nint(self):
        data = [(1.0, 1), (2.1, 2), (3.4, 3), (4.5, 5), (5.6, 6)]

        for num, expected in data:
            with self.subTest(num=num):
                result = self.tsplib._nint(num)
                self.assertEqual(result, expected)
                self.assertIsInstance(result, int)

    def test_w_euc_2d(self):
        coords = [(1, 1), (5, 5), (8, 15), (-50, 10), (-1000, -1000)]
        data = [(0, 1, 6), (1, 0, 6), (2, 1, 10), (2, 3, 58),
                (0, 4, 1416), (3, 4, 1387)]

        self.tsplib.coords = coords

        for i, j, expected in data:
            with self.subTest(i=i, j=j):
                result = self.tsplib._w_euc_2d(i, j)
                self.assertEqual(result, expected)
                self.assertIsInstance(result, int)

    def test_weight(self):
        weights = [[0,  2,  3],
                   [4,  0,  6],
                   [-1, 8, 0]]
        coords = [(0, 1, 2), (1, 2, 1), (2, -2, 0)]
        data = [
            ('EXPLICIT', 2, 1, 8),
            ('EXPLICIT', 2, 0, 3),
            ('EXPLICIT', 0, 0, 0),
            ('EUC_2D', 2, 0, 4),
            ('EUC_2D', 0, 2, 4),
            ('EUC_2D', 1, 0, 1)
        ]

        self.tsplib.specification = {'DIMENSION': 3}
        self.tsplib.weights = weights
        self.tsplib.coords = coords

        for ewt, i, j, expected in data:
            with self.subTest(ewt=ewt, i=i, j=j):
                self.tsplib.specification['EDGE_WEIGHT_TYPE'] = ewt
                result = self.tsplib.weight(i, j)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
