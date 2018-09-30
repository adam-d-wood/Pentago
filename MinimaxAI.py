import math
import copy

def evaluate_gamestate(game, field):
    (longest_sequence, red, blue) = game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    score_red = red
    score_blue = blue
    value = score_red - score_blue
    return value


def max_play(game, board, field, depth):
    print('max', depth)
    moves = []
    if depth <= 0:
        return 0, evaluate_gamestate(game, field)
    for i in range(board.macro_height):
        for j in range(board.macro_width):
            for k in range(board.micro_height):
                for m in range(board.micro_width):
                    if field[i][j][k][m] == 0:
                        newfield = copy.deepcopy(field)
                        token = 1 if game.red_turn else 2
                        for n in range(8):
                            newfield[i][j][k][m] = token
                            direction, tile = board.get_rotate_direction(n)
                            new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                            newfield[tile[0]][tile[1]] = new_tile
                            if depth <= 0 or game.win_check():
                                value = evaluate_gamestate(game, newfield)
                            else:
                                min_move, value = min_play(game, board, newfield, depth)
                            moves += [([i,j,k,m,n], value)]
                            print(moves)
                            print(i,j,k,m,n)
    print(moves)
    print('end')
    depth -= 1
    return max(moves, key = lambda x: x[1])

def min_play(game, board, field, depth):
    print('min', depth)
    moves = []
    if depth <= 0:
        return 0, evaluate_gamestate(game, field)
    for i in range(board.macro_height):
        for j in range(board.macro_width):
            for k in range(board.micro_height):
                for m in range(board.micro_width):
                    if field[i][j][k][m] == 0:
                        newfield = copy.deepcopy(field)
                        token = 2 if game.red_turn else 1
                        for n in range(8):
                            newfield[i][j][k][m] = token
                            direction, tile = board.get_rotate_direction(n)
                            new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                            newfield[tile[0]][tile[1]] = new_tile
                            if depth <= 0 or game.win_check():
                                value = evaluate_gamestate(game, newfield)
                            else:
                                max_move, value = max_play(game, board, newfield, depth)
                            moves += [([i,j,k,m,n], value)]
                            print(i,j,k,m,n)
                            print(moves)
    print('end')
    depth -= 1
    return min(moves, key = lambda x: x[1])

def minimax(game, board):
    print('start')
    depth = 5
    (move, value) = max_play(game, board, board.field, depth)
    print('return')
    return move[0][:-1], move[0][-1]
