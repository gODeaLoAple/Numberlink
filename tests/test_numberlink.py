import unittest
from numberlink import HexLink
from graph_tools import Graph


class HexLinkTest(unittest.TestCase):
    def setUp(self):
        self.field = [
            [3, 0, 0],            # 3 0 0
            [4, 1, 0, 0],        # 4 1 0 0
            [0, 0, 2, 2, 3],    # 0 0 2 2 3
            [0, 0, 1, 4],        # 0 0 1 4
            [0, 0, 0]             # 0 0 0
        ]
        self.game = HexLink(self.field)
        self.simple_game = HexLink([
            [1, 2],
            [0, 0, 0],
            [1, 2]
        ])

    def test_check_field_when_all_is_ok(self):
        self.assertEqual(self.field, HexLink(self.field).field)

    def test_init_when_wrong_cells(self):
        field = [
            ["a", "b"],
            ["c", "d", "e"],
            ["f", "g"]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_no_pairs(self):
        field = [
            [0, 0],
            [0, 0, 0],
            [0, 0]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_too_many_numbers(self):
        field = [
            [1, 0],
            [0, 1, 1],
            [2, 2]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_not_enough_pairs(self):
        field = [
            [1, 0],
            [0, 0, 0],
            [2, 0],
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_no_order(self):
        field = [
            [0, 0],
            [2, 0, 0],
            [2, 0]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_greater_than_nine(self):
        field = [
            [1, 0, 0, 1],
            [2, 0, 0, 0, 2],
            [3, 0, 0, 0, 0, 3],
            [4, 0, 0, 0, 0, 0, 4],
            [5, 0, 0, 5, 6, 6],
            [7, 7, 8, 0, 8],
            [9, 9, 10, 10]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_negative(self):
        field = [
            [-1, -1],
            [1, 0, 0],
            [1, 0]
        ]

        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_even_size(self):
        field = [
            [1],
            [0, 1]
        ]
        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_wrong_width(self):
        field = [
            [1, 2],
            [0, 0, 0, 0],
            [1, 2]
        ]
        self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_wrong_stairs(self):
        fields = [
            [
                [1, 2],
                [1, 2, 0],
                [0, 0, 0]
            ],
            [
                [1, 2, 0],
                [1, 2, 0],
                [0, 0]
            ]
        ]

        for field in fields:
            self.assertRaises(ValueError, HexLink, field)

    def test_init_raise_when_get_None(self):
        self.assertRaises(ValueError, HexLink, None)

    def test_init_raise_when_get_empty(self):
        self.assertRaises(ValueError, HexLink, [])

    def test_index_checker(self):
        self.assertTrue(self.game.is_valid(0, 1))
        self.assertFalse(self.game.is_valid(5, 0))
        self.assertFalse(self.game.is_valid(0, 3))

    def test_make_graph(self):
        expected = Graph(directed=False)

        # Top-Down
        expected.add_edge((0, 0), (1, 0))
        expected.add_edge((1, 0), (2, 0))
        expected.add_edge((0, 1), (1, 1))
        expected.add_edge((1, 1), (2, 1))

        # Left-Right
        expected.add_edge((0, 0), (0, 1))
        expected.add_edge((1, 0), (1, 1))
        expected.add_edge((1, 1), (1, 2))
        expected.add_edge((2, 0), (2, 1))

        # Diagonal
        expected.add_edge((0, 0), (1, 1))
        expected.add_edge((0, 1), (1, 2))
        expected.add_edge((2, 0), (1, 1))
        expected.add_edge((2, 1), (1, 2))

        actual = self.simple_game.make_graph()

        self.assertSetEqual(set(expected.vertices()),
                            set(actual.vertices()))
        self.assertSetEqual(set(frozenset(edge) for edge in expected.edges()),
                            set(frozenset(edge) for edge in actual.edges()))

    def test_get_targets(self):
        expected = {
            "vertices": {(0, 0), (0, 1), (2, 0), (2, 1)},
            "pairs": {frozenset({(0, 0), (2, 0)}), frozenset({(0, 1), (2, 1)})}
        }
        actual = self.simple_game.get_targets()

        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
