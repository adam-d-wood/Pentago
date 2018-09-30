import copy
import math
import random

def wincheck(game, field):
    (longest_sequence, red, blue) = game.board.get_sequences(game.board.combine_tiles(field))
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    print(longest_sequence)
    red_win = longseq_red >= 5
    blue_win = longseq_blue >= 5
    if blue_win: print('blue')
    full_board = game.board.is_full(field)
    return red_win or blue_win or full_board

def showfield(field):
    for i in range(2):
        for j in range(3):
            print(field[i][0][j], end='\t')
            print(field[i][1][j], end='\t')
            print()
        print()

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
    if depth <= 0 or wincheck(game, field):
        # print('done')
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
                                # showfield(newfield)
                                # print(depth)
                                # print('-'*30 + '\n')
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                # print('call')
                                depth -= 1
                                minmax = minimax(game, newfield, depth, False)
                                try:
                                    if minmax >= value:
                                        value = minmax
                                        # print('max', value)
                                        best_move = [i,j,k,m,n]
                                    # value = max(value, minmax)
                                except:
                                    # print('exception raised. minmax=', minmax)
                                    if minmax[0] >= value:
                                        value = minmax[0]
                                        # print(i,j,k,m,n, 'chosen over', best_move)
                                        best_move = [i,j,k,m,n]
                                    # value = max(value, minmax[0])
                                # print(value)
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
                                # showfield(newfield)
                                # print(depth)
                                # print('-'*30 + '\n')
                                direction, tile = board.get_rotate_direction(n)
                                new_tile = board.rotate(newfield, direction, tile[0], tile[1])
                                newfield[tile[0]][tile[1]] = new_tile
                                depth -= 1
                                print(depth)
                                minmax = minimax(game, newfield, depth, True)
                                try:
                                    if minmax <= value:
                                        value = minmax
                                        # print('min', value)
                                        best_move = [i,j,k,m,n]
                                    # value = min(value, minmax)
                                except:
                                    # print('exception raised. minmax=', minmax)
                                    if minmax[0] <= value:
                                        value = minmax[0]
                                        # print(i,j,k,m,n, 'chosen over', best_move)
                                        best_move = [i,j,k,m,n]
                                    # value = min(value, minmax[0])
                                # print(value)
        rotation = best_move.pop(-1)
        return [value, best_move, rotation]
