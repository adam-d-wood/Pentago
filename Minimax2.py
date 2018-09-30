import copy
import math
import random

def wincheck(game, field):
    (longest_sequence, red, blue) = game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    red_win = longseq_red >= 5
    blue_win = longseq_blue >= 5
    full_board = game.board.is_full(field)
    return red_win or blue_win or full_board

def simulate_insert(game, field, cell, rotation, token):
    direction, tile = self.board.get_rotate_direction(rotation)


def evaluate_gamestate(game, field):
    (longest_sequence, red, blue) = game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    score_red = red
    score_blue = blue
    value = score_red - score_blue
    # print(longseq_red, longseq_blue)
    # if longseq_red >= 5:
    #     print('possible red win')
    #     print(score_red)
    # if longseq_blue >=5:
    #     print('possible blue win')
    #     print(score_blue)
    return value

def minimax(game, field, depth, maximisingPlayer):
    board = game.board
    if depth == 0 or wincheck(game, field):
        return evaluate_gamestate(game, field)
    if maximisingPlayer:
        best_move = [0,0,0,0,0]
        value = -math.inf
        newfield = copy.deepcopy(field)
        token = 1 if game.red_turn else 2
        for i in range(board.macro_height):
            for j in range(board.macro_width):
                for k in range(board.micro_height):
                    for m in range(board.micro_width):
                        if field[i][j][k][m] == 0:
                            for n in range(8):
                                newfield[i][j][k][m] = token
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                minmax = minimax(game, newfield, depth-1, False)
                                a = random.randint(0,1)
                                try:
                                    if minmax >= value and a:
                                        value = minmax
                                        # print('max', value)
                                        best_move = [i,j,k,m,n]
                                    # value = max(value, minmax)
                                except:
                                    # print('exception raised. minmax=', minmax)
                                    if minmax[0] >= value and a:
                                        value = minmax[0]
                                        print(i,j,k,m,n, 'chosen over', best_move)
                                        best_move = [i,j,k,m,n]
                                    # value = max(value, minmax[0])
                                # print(value)
        rotation = best_move.pop(-1)
        return [value, best_move, rotation]
    else:
        value = math.inf
        best_move = [0,0,0,0,0]
        newfield = copy.deepcopy(field)
        token = 1 if game.red_turn else 2
        for i in range(board.macro_height):
            for j in range(board.macro_width):
                for k in range(board.micro_height):
                    for m in range(board.micro_width):
                        if field[i][j][k][m] == 0:
                            for n in range(8):
                                newfield[i][j][k][m] = token
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                minmax = minimax(game, newfield, depth-1, True)
                                a = random.randint(0,1)
                                try:
                                    if minmax <= value and a:
                                        value = minmax
                                        # print('min', value)
                                        best_move = [i,j,k,m,n]
                                    # value = min(value, minmax)
                                except:
                                    # print('exception raised. minmax=', minmax)
                                    if minmax[0] <= value and a:
                                        value = minmax[0]
                                        print(i,j,k,m,n, 'chosen over', best_move)
                                        best_move = [i,j,k,m,n]
                                    # value = min(value, minmax[0])
                                # print(value)
        rotation = best_move.pop(-1)
        return [value, best_move, rotation]
