successful_validations = 0


def placement_is_valid(state, proposed_coordinates, player):
    global successful_validations
    for coord in proposed_coordinates:
        if not __square_is_within_gameboard(state, coord):
            return False
        if not __square_has_player(state, coord, None):
            return False
        immediate_neighbours = [[coord[0]-1, coord[1]],
                                [coord[0]+1, coord[1]],
                                [coord[0], coord[1]-1],
                                [coord[0], coord[1]+1]]
        for immediate_neighbour in immediate_neighbours:
            if __square_is_within_gameboard(state, immediate_neighbour) and not immediate_neighbour in proposed_coordinates:
                if __square_has_player(state, immediate_neighbour, player):
                    return False
        diagonal_neighbours = [[coord[0]+1, coord[1]+1],
                               [coord[0]+1, coord[1]-1],
                               [coord[0]-1, coord[1]+1],
                               [coord[0]-1, coord[1]-1]]
        is_block_connected = False
        for diagonal_neighbour in diagonal_neighbours:
            if __square_is_within_gameboard(state, diagonal_neighbour) and not diagonal_neighbour in proposed_coordinates and not diagonal_neighbour in immediate_neighbours:
                # Todo: add this into a second loop: and not diagonal_neighbour in immediate_neighbours:
                # other_player = 0 if player == 1 else 1
                # if __square_has_player(state, diagonal_neighbour, other_player):
                #     return False
                if __square_has_player(state, diagonal_neighbour, player):
                    is_block_connected = True
        if not is_block_connected and successful_validations > 2:
            return False
    successful_validations += 1
    return True


def __square_is_within_gameboard(state, square):
    return not (square[0] < 0 or square[1] < 0 or square[0] > len(state) - 1 or square[1] > len(state) - 1)


def __square_has_player(state, square, expected_player):
    return state[square[0]][square[1]] == expected_player
