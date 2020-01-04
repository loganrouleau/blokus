import unittest
from src import validator

DIMENSION = 4
gameboard = [[None for _ in range(DIMENSION)] for _ in range(DIMENSION)]
gameboard[0][2] = 0
gameboard[2][0] = 1
gameboard[3][0] = 1


class TestValidator(unittest.TestCase):

    def test_all_conditions_met(self):
        proposed_coordinates = [[1, 1], [2, 1], [3, 1]]
        player = 0
        self.assertTrue(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[1, 3], [2, 2], [2, 3]]
        self.assertTrue(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[0, 1], [1, 1], [1, 2]]
        player = 1
        self.assertTrue(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))

    def test_out_of_bounds(self):
        proposed_coordinates = [[-1, 0]]
        player = 0
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[1, DIMENSION]]
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))

    def test_squares_are_empty(self):
        proposed_coordinates = [[1, 1], [2, 0], [2, 1]]
        player = 0
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))

    def test_adjacent_squares_are_taken(self):
        proposed_coordinates = [[0, 1], [0, 2], [0, 3]]
        player = 0
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[3, 1]]
        player = 1

    def test_corner_squares_invalid(self):
        proposed_coordinates = [[1, 1]]
        player = 0
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[1, 3], [2, 3]]
        player = 1
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))

    def test_at_least_one_corner_connected(self):
        proposed_coordinates = [[2, 2], [2, 3], [3, 3]]
        player = 0
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))
        proposed_coordinates = [[0, 0], [0, 1]]
        self.assertFalse(validator.placement_is_valid(
            gameboard, proposed_coordinates, player))


if __name__ == '__main__':
    unittest.main()
