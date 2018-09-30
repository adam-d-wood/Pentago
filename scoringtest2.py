import PentaGoBoard

board = PentaGoBoard.Board()

def empty_field():
    field = []
    for i in range(2):
        macro_row = []
        for j in range(2):
            macro_col = []
            for k in range(3):
                micro_row = []
                for m in range(3):
                    micro_row.append(0)
                macro_col.append(micro_row)
            macro_row.append(macro_col)
        field.append(macro_row)
    return field

def evaluate_gamestate(board, field):
    (longest_sequence, red, blue) = board.get_sequences(field)
    longseq_red = longest_sequence['red']
    longseq_blue = longest_sequence['blue']
    score_red = red
    score_blue = blue
    value = score_red - score_blue
    return value

field = empty_field()
token = 1

field = [[2, 0, 0, 2, 2],
        [0, 2, 1, 2, 2],
        [2, 1, 2, 2, 2],
        [2, 1, 2, 2, 2],
        [2, 2, 2, 2, 2]]

# score_vertical(field)
print(evaluate_gamestate(board, field))
