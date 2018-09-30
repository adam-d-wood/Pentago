import PentaGoBoard
import random
import math

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

def field_rotate(field):
    new_field = []
    i = 0
    while i < len(field):
        new_field.append([])
        j = len(field) - 1
        while j >= 0:
            new_field[i].append(field[j][i])
            j -= 1
        i += 1
    return new_field

def score_vertical(field):
    scores = {'red': 0, 'blue': 0,}
    longest_sequence = {'red': 0, 'blue': 0}
    for column in field:
        print('ding')
        sequence = {'length': 0, 'colour': 0}
        for place in column:
            token = place
            self.update_sequence(token, sequence, scores, longest_sequence)
        self.update_sequence(0, sequence, scores, longest_sequence)
    return scores, longest_sequence

# def half_diagonal(field):
#     height = len(field)
#     max_sum = 2*(height-1)
#     sums = [x for x in range(max_sum+1)]
#     sequence = []
#     for sum in sums:
#         for i in range(height):
#             for j in range(height):
#                 if i+j == sum:
#                     sequence.append(field[i][j])
#                     print(field[i][j])
#         print(sequence)
#         sequence = []

def half_diagonal(field, scores, longest_sequence):
    height = len(field)
    max_sum = 2*(height-1)
    sums = [x for x in range(max_sum+1)]
    for sum in sums:
        sequence = {'length': 0, 'colour': 0}
        for i in range(height):
            for j in range(height):
                if i+j == sum: board.update_sequence(token, sequence, scores, longest_sequence)
        board.update_sequence(0, sequence, scores, longest_sequence)

def score_diagonals(field):
    scores = {'red': 0, 'blue': 0}
    longest_sequence = {'red': 0, 'blue': 0}
    half_diagonal(field, scores, longest_sequence)
    half_diagonal(field_rotate(field), scores, longest_sequence)
    return longest_sequence

def get_sequences(field):
    longest_sequence = {}
    # v_scores, v_sequences = self.score_diagonals(0, 1, field)
    # h_scores, h_sequences = self.score_diagonals(1, 0, field)
    # ur_scores, ur_sequences = self.score_diagonals(1, 1, field)
    # ul_scores, ul_sequences = self.score_diagonals(-1, -1, field)
    d_sequences = score_diagonals(field)
    # red = v_scores['red'] + h_scores['red'] \
    #       + ul_scores['red'] + ur_scores['red']
    # blue = v_scores['blue'] + h_scores['blue'] \
    #       + ul_scores['blue'] + ur_scores['blue']
    # for t in ['red', 'blue']:
    #     longest_sequence[t] = d_sequences[t]
    return(d_sequences)

def showfield(field):
    for i in range(2):
        for j in range(3):
            print(field[i][0][j], end='\t')
            print(field[i][1][j], end='\t')
            print()
        print()

def random_move():
    a = random.randint(0,1)
    b = random.randint(0,1)
    c = random.randint(0,2)
    d = random.randint(0,2)
    return a, b, c, d

field = empty_field()
token = 1

field = [[1, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 1]]

# score_vertical(field)
print(get_sequences(field))

# for c in range(1):
#     # field = empty_field()
#     # i, j, k, m = random_move()
#     # field[i][j][k][m] = token
#     field[0][1][0] = [1, 0, 1]
#     field[0][1][1] = [0, 1, 0]
#     field[0][1][2] = [0, 0, 1]
#     field[1][0][0] = [1, 0, 0]
#     field[1][0][1] = [0, 1, 0]
#     showfield(field)
#     for row in board.combine_tiles(field):
#         print(row)
#     longest_sequence, red, blue = board.get_sequences(board.combine_tiles(field))
#     print(longest_sequence)
#     print(red, blue)
#     print('-'*30 + '\n')
#     token = 3-token
