import random
import PentaGoBoard

def choose_move(game, field, depth=None, maximisingPlayer=None):
    while True:
        macro_row = random.randint(0, 1)
        macro_col = random.randint(0, 1)
        micro_row = random.randint(0, 2)
        micro_col = random.randint(0, 2)
        if field[macro_row][macro_col][micro_row][micro_col] == 0:
            cell = [macro_row, macro_col, micro_row, micro_col]
            break
    rotation = random.randint(0, 7)
    # print(cell, rotation)
    return 'random', cell, rotation
