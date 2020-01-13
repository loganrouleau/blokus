import unittest
from src import transformer
from src import block


class TestTransformer(unittest.TestCase):

    def test_rotate_single_coord_block(self):
        input_block = block.Block(0, [0, 3], [[0, 0]])
        expected_coords = [[0, 0]]
        actual_coords = transformer.rotate_90(
            input_block, "block_segment_0").coordinates
        self.assertEqual(actual_coords, expected_coords)

    def test_rotate_long_straight_block_from_end(self):
        input_block = block.Block(
            14, [5, 22], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]])
        expected_coords = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        actual_coords = transformer.rotate_90(
            input_block, "block_segment_0").coordinates
        self.assertEqual(actual_coords, expected_coords)

    def test_rotate_long_straight_block_from_middle(self):
        input_block = block.Block(
            14, [5, 22], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]])
        expected_coords = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        actual_coords = transformer.rotate_90(
            input_block, "block_segment_1").coordinates
        self.assertEqual(actual_coords, expected_coords)


if __name__ == '__main__':
    unittest.main()
