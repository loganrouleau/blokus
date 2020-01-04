successful_validations = 0


def placement_is_valid(state, proposed_coordinates, player):
    global successful_validations
    for coord in proposed_coordinates:
        if not __square_is_within_gameboard(state, coord):
            return False
        if not __square_has_player(state, coord, None):
            return False
        adjacent_squares = [[coord[0]-1, coord[1]], [coord[0]+1,
                                                     coord[1]], [coord[0], coord[1]-1], [coord[0], coord[1]+1]]
        for adjacent_square in adjacent_squares:
            if __square_is_within_gameboard(state, adjacent_square) and not adjacent_square in proposed_coordinates:
                if __square_has_player(state, adjacent_square, player):
                    return False
        corner_squares = [[coord[0]+1, coord[1]+1], [coord[0]+1,
                                                     coord[1]-1], [coord[0]-1, coord[1]+1], [coord[0]-1, coord[1]-1]]
        is_block_connected = False
        for corner_square in corner_squares:
            if __square_is_within_gameboard(state, corner_square) and not corner_square in proposed_coordinates and not corner_square in adjacent_squares:
                other_player = 0 if player == 1 else 1
                if __square_has_player(state, corner_square, other_player):
                    return False
                if __square_has_player(state, corner_square, player):
                    is_block_connected = True
        if not is_block_connected and successful_validations > 2:
            return False
    successful_validations = successful_validations + 1
    return True


def __square_is_within_gameboard(state, square):
    return not (square[0] < 0 or square[1] < 0 or square[0] > len(state) - 1 or square[1] > len(state) - 1)


def __square_has_player(state, square, expected_player):
    return state[square[0]][square[1]] == expected_player
