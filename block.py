class Block:
    all_coordinates = {0: [[0, 0]],
                       1: [[0, 0], [1, 0]],
                       2: [[0, 0], [1, 0], [1, 1]],
                       3: [[0, 0], [1, 0], [2, 0]],
                       4: [[0, 0], [1, 0], [0, -1], [1, -1]]}

    def __init__(self, index):
        self.index = index
        self.coordinates = Block.all_coordinates[index]
