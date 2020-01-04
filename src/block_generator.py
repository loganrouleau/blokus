import block


def generate_blocks():
    return [block.Block(0, [0, 3], [[0, 0]]),
            block.Block(1, [0, 7], [[0, 0], [0, 1]]),
            block.Block(2, [0, 12], [[0, 0], [0, 1], [1, 1]]),
            block.Block(3, [0, 17], [[0, 0], [0, 1], [0, 2]]),
            block.Block(4, [2, 0], [[0, 0], [0, 1], [1, 0], [1, 1]]),
            block.Block(5, [2, 4], [[0, 1], [1, 0], [1, 1], [1, 2]]),
            block.Block(6, [3, 9], [[0, 0], [0, 1], [0, 2], [0, 3]]),
            block.Block(7, [3, 15], [[0, 0], [0, 1], [0, 2], [-1, 2]]),
            block.Block(8, [3, 20], [[0, 0], [0, 1], [-1, 1], [-1, 2]]),
            block.Block(9, [6, 0], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]),
            block.Block(10, [7, 5], [[0, 0], [-2, 1],
                                     [-1, 1], [0, 1], [0, 2]]),
            block.Block(11, [7, 9], [[-2, 0], [-1, 0],
                                     [0, 0], [0, 1], [0, 2]]),
            block.Block(12, [7, 13], [[0, 0], [0, 1],
                                      [-1, 1], [-1, 2], [-1, 3]]),
            block.Block(13, [7, 18], [[0, 0], [-1, 0],
                                      [-1, 1], [-1, 2], [-2, 2]]),
            block.Block(14, [5, 22], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]),
            block.Block(15, [9, 0], [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1]]),
            block.Block(16, [9, 3], [[1, 0], [2, 0], [0, 1], [1, 1], [0, 2]]),
            block.Block(17, [9, 7], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1]]),
            block.Block(18, [9, 11], [[1, 0], [0, 1], [1, 1], [2, 1], [0, 2]]),
            block.Block(19, [9, 15], [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]),
            block.Block(20, [9, 19], [[2, 0], [1, 1], [2, 1], [2, 2], [2, 3]])]