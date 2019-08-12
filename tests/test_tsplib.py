import unittest

from tspvisual.tsplib import TSPLib


class TestTSPLib(unittest.TestCase):

    def setUp(self):
        self.tsplib = TSPLib()
        self.tsplib.specification['DIMENSION'] = 4
        self.formats = {
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

    def test_cells(self):
        for form, expected in self.formats.items():
            with self.subTest(form=form):
                self.tsplib.specification['EDGE_WEIGHT_FORMAT'] = form
                result = list(self.tsplib._cells())
                self.assertListEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
