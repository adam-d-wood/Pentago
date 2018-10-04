import copy
import math
import random

def wincheck(game, field):
    (longest_sequence, red, blue) = \
    game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    red_win = longseq_red >= 5
    blue_win = longseq_blue >= 5
    full_board = game.board.is_full(field)
    return red_win or blue_win or full_board

def evaluate_gamestate(game, field):
    (longest_sequence, score_red, score_blue) =  \
    game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    value = (score_red-score_blue if game.red_turn else score_blue-score_red)
    return value

def minimax(game, field, depth_remaining, maximisingPlayer):
    board = game.board
    if wincheck(game, field) or depth_remaining <= 0:
        return evaluate_gamestate(game, field)
    if maximisingPlayer:
        best_move = [0,0,0,0,0]
        value = -math.inf
        for i in range(board.macro_height):
            for j in range(board.macro_width):
                for k in range(board.micro_height):
                    for m in range(board.micro_width):
                        if field[i][j][k][m] == 0:
                            for n in range(8):
                                newfield = copy.deepcopy(field)
                                token = 1 if game.red_turn else 2
                                newfield[i][j][k][m] = token
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction,
                                                        tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                minmax = minimax(game, newfield,
                                        depth_remaining-1, False)
                                try:
                                    if minmax >= value:
                                        value = minmax
                                        best_move = [i,j,k,m,n]
                                except:
                                    if minmax[0] >= value:
                                        value = minmax[0]
                                        best_move = [i,j,k,m,n]
        rotation = best_move.pop(-1)
        return [value, best_move, rotation]
    else:
        value = math.inf
        best_move = [0,0,0,0,0]
        for i in range(board.macro_height):
            for j in range(board.macro_width):
                for k in range(board.micro_height):
                    for m in range(board.micro_width):
                        if field[i][j][k][m] == 0:
                            for n in range(8):
                                newfield = copy.deepcopy(field)
                                token = 2 if game.red_turn else 1
                                newfield[i][j][k][m] = token
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction,
                                                        tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                minmax = minimax(game, newfield,
                                            depth_remaining-1, True)
                                try:
                                    if minmax <= value:
                                        value = minmax
                                        best_move = [i,j,k,m,n]
                                except:
                                    if minmax[0] <= value:
                                        value = minmax[0]
                                        best_move = [i,j,k,m,n]
        rotation = best_move.pop(-1)
        return [value, best_move, rotation]
