import unittest
from algorithms.generator import *


class PathConstructorTest(unittest.TestCase):
    def setUp(self):
        field = generate_hexagonal_field(5)
        self.constructor = PathConstructor(HexagonalField(field))
        self.field = HexagonalField(field)

    def test_count_added_neighbours_when_all_valid_and_zero(self):
        self.assert_count_added_neighbours(0, (2, 1))

    def test_count_added_neighbours_when_all_valid(self):
        field = self.field
        field[2, 0] = field[1, 1] = 1
        self.assert_count_added_neighbours(2, (2, 1))

    def test_count_added_neighbours_when_some_invalid(self):
        field = self.field
        field[0, 1] = field[1, 0] = field[1, 1] = 1
        self.assert_count_added_neighbours(6, (0, 0))

    def assert_count_added_neighbours(self, expected, position):
        constructor = PathConstructor(self.field)
        actual = constructor.count_added_neighbours_or_non_valid(position)
        self.assertEqual(expected, actual)

    def test_count_numbered_neighbours_when_all_empty(self):
        expected = 0
        actual = self.constructor.count_numbered_neighbours((0, 0), 1)
        self.assertEqual(expected, actual)

    def test_count_numbered_neighbours_when_not_same_number(self):
        expected = 0
        self.field[0, 0] = 2
        self.assert_count_numbered_neighbours(expected, (0, 1), 1)

    def test_count_numbered_neighbours(self):
        expected = 2
        self.field[0, 0] = self.field[0, 1] = 1
        self.assert_count_numbered_neighbours(expected, (1, 1), 1)

    def assert_count_numbered_neighbours(self, expected, position, number):
        constructor = PathConstructor(self.field)
        actual = constructor.count_numbered_neighbours(position, number)
        self.assertEqual(expected, actual)

    def test_isolated_False(self):
        self.assertFalse(
            PathConstructor(self.field).is_isolated((0, 0), 1, False)
        )

    def test_isolated_true_when_some_invalid(self):
        self.field[1, 0] = self.field[0, 1] = self.field[1, 1] = 1
        self.assertTrue(
            PathConstructor(self.field).is_isolated((0, 0), 1, True)
        )
        self.assertTrue(
            PathConstructor(self.field).is_isolated((0, 0), 2, False)
        )

    def test_isolated_true_when_all_valid(self):
        self.field[1, 0], self.field[0, 1], self.field[1, 1] = 1, 1, 1
        self.field[0, 0], self.field[1, 2] = 1, 1
        self.field[2, 1], self.field[2, 2] = 1, 1
        self.assertTrue(
            PathConstructor(self.field).is_isolated((1, 1), 1, True)
        )
        self.assertTrue(
            PathConstructor(self.field).is_isolated((1, 1), 2, False)
        )

    def test_has_isolated_empty_cell(self):
        self.field[0, 0], self.field[0, 1] = 1, 1
        self.field[1, 0], self.field[1, 2] = 1, 1
        self.field[2, 1], self.field[2, 2] = 1, 1
        self.assertTrue(
            PathConstructor(self.field).has_isolated_empty_cells(
                (2, 2), 1, False
            )
        )
        self.assertTrue(
            PathConstructor(self.field).has_isolated_empty_cells(
                (2, 2), 2, False
            )
        )

    def test_can_add_cell_false(self):
        self.field[0, 1] = self.field[1, 1] = 1
        self.assertFalse(
            PathConstructor(self.field).can_add_cell((1, 0), 1)
        )

    def test_can_add_cell_true(self):
        self.field[0, 0] = 1
        self.assertTrue(
            PathConstructor(self.field).can_add_cell((0, 1), 1)
        )


class GeneratorTest(unittest.TestCase):
    def test_count(self):
        sequence = [1, 2, 3, 4]
        expected = len(sequence)
        actual = count(sequence)
        self.assertEqual(expected, actual)

    def test_count_if_has_no_elements(self):
        sequence = []
        expected = 0
        actual = count(sequence)
        self.assertEqual(expected, actual)

    def test_centered_hex_number(self):
        expected = [1, 7, 19, 37]
        actual = [centered_hex_number(n) for n in range(1, 5)]
        self.assertListEqual(expected, actual)

    def test_generate_hexagonal_field(self):
        expected = [
            [0] * 3,
            [0] * 4,
            [0] * 5,
            [0] * 4,
            [0] * 3,
        ]
        actual = generate_hexagonal_field(5)

        self.assertEqual(expected, actual)

    def test_empty_cells(self):
        field = HexagonalField([
            [0, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0],
        ])

        expected = {(0, 0), (3, 1), (4, 2)}
        actual = set(get_empty_cells(field))

        self.assertSetEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
