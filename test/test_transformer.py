import unittest
from src import transformer
from src import block


class TestTransformer(unittest.TestCase):

    def test_rotated_block_has_origin_at_selected_segment(self):
        input_block = block.Block(0, [0, 3], [[0, 0], [0, 1]])
        self.assertEqual(transformer.rotate_90(
            input_block, "block_segment_1").coordinates[1], [0, 0])

    def test_flipped_block_has_origin_at_selected_segment(self):
        input_block = block.Block(0, [0, 3], [[0, 0], [0, 1]])
        self.assertEqual(transformer.flip(
            input_block, "block_segment_1").coordinates[1], [0, 0])

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
        expected_coords = [[0, -1], [0, 0], [0, 1], [0, 2], [0, 3]]
        actual_coords = transformer.rotate_90(
            input_block, "block_segment_1").coordinates
        self.assertEqual(actual_coords, expected_coords)

    def test_rotating_4_times_should_result_in_same_shape(self):
        input_block = block.Block(5, [2, 4], [[0, 1], [1, 0], [1, 1], [1, 2]])
        expected_coords = [[-1, 0], [0, -1], [0, 0], [0, 1]]
        actual_block = transformer.rotate_90(input_block, "block_segment_2")
        actual_block = transformer.rotate_90(actual_block, "block_segment_2")
        actual_block = transformer.rotate_90(actual_block, "block_segment_2")
        actual_block = transformer.rotate_90(actual_block, "block_segment_2")
        actual_coords = actual_block.coordinates
        self.assertEqual(actual_coords, expected_coords)

    def test_flip_large_block(self):
        input_block = block.Block(
            18, [9, 11], [[1, 0], [0, 1], [1, 1], [2, 1], [0, 2]])
        expected_coords = [[1, 1], [0, 0], [1, 0], [2, 0], [0, -1]]
        actual_coords = transformer.flip(
            input_block, "block_segment_1").coordinates
        self.assertEqual(actual_coords, expected_coords)


if __name__ == '__main__':
    unittest.main()
