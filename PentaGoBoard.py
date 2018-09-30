import copy
import math

RED = 1
BLUE = 2

def new_empty_board(macro_height, macro_width, micro_height, micro_width):
    board = []
    for i in range(macro_height):
        board.append([])
        for j in range(macro_width):
            board[i].append([])
            for k in range(micro_height):
                board[i][j].append([])
                for m in range(micro_width):
                    board[i][j][k].append(0)
    return board

class Board():

    def __init__(self, board=None, winscore = 5):
        self.macro_height = 2
        self.macro_width = 2
        self.micro_height = 3
        self.micro_width = 3
        if board == None:
            board = new_empty_board(self.macro_height, self.macro_width, \
                    self.micro_height, self.micro_width)
        self.field = board
        self.winscore = winscore
        self.rewards = [0, 1, 8, 27, 64, math.inf]

    def copy(self):
        return Board(
            board = copy.deepcopy(self.field),
            winscore = self.winscore)

    def attempt_insert(self, i, token):
        if i == -1:
            return False
        elif self.field[i[0]][i[1]][i[2]][i[3]] == 0:
            self.field[i[0]][i[1]][i[2]][i[3]] = token
            return True
        else:
            return False

    def get_rotate_direction(self, index):
        x = [
        [0, 1, 2, 3, 4, 5, 6, 7],
        [-1, 1, -1, 1, -1, 1, -1, 1],
        [[0,0], [0,0], [0,1], [0,1], [1,1], [1,1], [1,0], [1,0]]
        ]
        n = x[0].index(index)
        return x[1][n], x[2][n]

    def combine_tiles(self, field):
        combined_board = [
        [],[],[],[],[],[]
        ]
        for i in range(len(field)):
            for j in range(len(field[i])):
                for k in range(len(field[i][j])):
                    for m in range(len(field[i][j][k])):
                        combined_board[self.micro_width*i + k].append(field[i][j][k][m])
        return combined_board

    def update_sequence(self, token, sequence, scores, longest_sequence):
        if token == sequence['colour']:
            sequence['length'] += 1

        else:
            if sequence['length'] > 0:
                if sequence['length'] >= 5:
                    points = self.rewards[-1]
                else:
                    points = self.rewards[sequence['length']]
            else:
                points = 0
            if sequence['colour'] == 1:
                scores['red'] += points
                if sequence['length'] > longest_sequence['red']:
                    longest_sequence['red'] = sequence['length']
            elif sequence['colour'] == 2:
                scores['blue'] += points
                if sequence['length'] > longest_sequence['blue']:
                    longest_sequence['blue'] = sequence['length']

            if token == 0:
                sequence['colour'] = 0
                sequence['length'] = 0
            else:
                sequence['colour'] = token
                sequence['length'] = 1

    def field_rotate(self, field):
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

    def half_diagonal(self, field, scores, longest_sequence):
        height = len(field)
        max_sum = 2*(height-1)
        sums = [x for x in range(max_sum+1)]
        for sum in sums:
            sequence = {'length': 0, 'colour': 0}
            for i in range(height):
                for j in range(height):
                    if i+j == sum:
                        token = field[i][j]
                        self.update_sequence(token, sequence, scores, longest_sequence)
            self.update_sequence(0, sequence, scores, longest_sequence)

    def score_diagonals(self, field):
        scores = {'red': 0, 'blue': 0}
        longest_sequence = {'red': 0, 'blue': 0}
        self.half_diagonal(field, scores, longest_sequence)
        self.half_diagonal(self.field_rotate(field), scores, longest_sequence)
        return scores, longest_sequence

    def score_horizontal(self, field):
        scores = {'red': 0, 'blue': 0,}
        longest_sequence = {'red': 0, 'blue': 0}
        for column in field:
            sequence = {'length': 0, 'colour': 0}
            for place in column:
                token = place
                self.update_sequence(token, sequence, scores, longest_sequence)
            self.update_sequence(0, sequence, scores, longest_sequence)
        return scores, longest_sequence

    def score_vertical(self, field):
        scores = {'red': 0, 'blue': 0}
        longest_sequence = {'red': 0, 'blue': 0}
        for i in range(len(field[0])):
            sequence = {'length': 0, 'colour': 0}
            for column in field:
                token = column[i]
                self.update_sequence(token, sequence, scores, longest_sequence)
            self.update_sequence(0, sequence, scores, longest_sequence)
        return scores, longest_sequence

    def get_sequences(self, field):
        longest_sequence = {}
        v_scores, v_sequences = self.score_vertical(field)
        h_scores, h_sequences = self.score_horizontal(field)
        diag_scores, diag_sequences = self.score_diagonals(field)
        red = v_scores['red'] + h_scores['red'] \
              + diag_scores['red']
        blue = v_scores['blue'] + h_scores['blue'] \
              + diag_scores['blue']
        for t in ['red', 'blue']:
            longest_sequence[t] = max(v_sequences[t], h_sequences[t],
                                    diag_sequences[t])
        return(longest_sequence, red, blue)


    def rotate(self, field, direction, row, col):
        new_tile = []
        if direction == -1: #clockwise
            i = 0
            while i < len(field[row][col]):
                new_tile.append([])
                j = len(field[row][col]) - 1
                while j >= 0:
                    new_tile[i].append(field[row][col][j][i])
                    j -= 1
                i += 1
        elif direction == 1: #anticlockwise
            i = len(field[row][col]) - 1
            while i >= 0:
                new_tile.append([])
                j = 0
                while j < len(field[row][col]):
                    new_tile[2 - i].append(field[row][col][j][i])
                    j += 1
                i -= 1
        return new_tile

    def neutral_tiles(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.rotate(self.field, 1, i, j) == self.field[i][j] or \
                        self.rotate(self.field, -1, i, j) == self.field[i][j]:
                    return True
        return False

    def is_full(self, field):
        for macro_row in field:
            for macro_col in macro_row:
                for micro_row in macro_col:
                    for cell in micro_row:
                        if cell == 0: return False
        return True

class EmptyBoard(Board):

    def __init__(self, macro_height = 2, macro_width = 2, \
                micro_height = 3, micro_width = 3, winscore=5):
        fresh_board = new_empty_board(macro_height, macro_width, \
                micro_height, micro_width)
        Board.__init__(self, fresh_board, winscore)
