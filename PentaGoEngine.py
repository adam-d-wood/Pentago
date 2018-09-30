import pygame
from pygame.locals import *
import sys
import math

import PentaGoGraphics
import PentaGoBoard
import RandomAI

class PentaGo:

    def __init__(self,
    red_player = None,
    blue_player = None,
    ai_delay = 60
    ):

        pygame.init()
        pygame.font.init()

        self.board = PentaGoBoard.EmptyBoard()

        self.selected_index = -1
        self.display = PentaGoGraphics.setup_display(self.board)

        self.red_player = red_player
        self.blue_player = blue_player
        self.ai_delay = ai_delay
        self.can_end_turn = False
        self.can_insert_token = True
        self.can_rotate = False

        self.score_red = 0
        self.score_blue = 0
        self.longseq_blue = 0
        self.longseq_red = 0
        self.winner = 0
        self.game_running = True
        self.red_turn = True

        self.coords, self.end_turn_button, self.arrow_buttons = self.draw()
        pygame.display.flip()

    def human_turn(self):
        if self.red_turn and self.red_player is None:
            return True
        elif (not self.red_turn) and self.blue_player is None:
            return True
        else:
            return False

    def draw(self):
        coords, end_turn_button, arrow_buttons =  \
        PentaGoGraphics.draw_board(self.display, self.board, self.selected_index,
            self.game_running, self.human_turn(), self.red_turn, self.winner,
            self.can_end_turn)
        return coords, end_turn_button, arrow_buttons

    def turn_token(self):
        if self.red_turn:
            return PentaGoBoard.RED
        else:
            return PentaGoBoard.BLUE

    def handle_click(self, item):
        if item == -1:
            pass
        elif item == -2:
            if self.can_end_turn:
                self.red_turn = not(self.red_turn)
                self.can_end_turn = False
                self.can_insert_token = True
                self.can_rotate = False
        elif item[0] == -3:
            if self.can_rotate:
                direction, tile = self.board.get_rotate_direction(item[1])
                new_tile = self.board.rotate(self.board.field, direction,
                                            tile[0], tile[1])
                self.board.field[tile[0]][tile[1]] = new_tile
                self.can_end_turn = True
                self.can_rotate = False
        elif self.can_insert_token:
            token = self.turn_token()
            success = self.board.attempt_insert(item, token)
            neutrals = self.board.neutral_tiles()
            if success:
                self.can_insert_token = False
                self.can_rotate = True
                if neutrals:
                    self.can_end_turn = True

    def refresh_scores(self):
        (longest_sequence, red, blue) =  \
        self.board.get_sequences(self.board.combine_tiles(self.board.field))
        self.longseq_red = longest_sequence['red']
        self.longseq_blue = longest_sequence['blue']
        self.score_red = red
        self.score_blue = blue

    def win_check(self):
        red_win = self.longseq_red >= 5
        blue_win = self.longseq_blue >= 5
        full_board = self.board.is_full(self.board.field)
        return red_win or blue_win or full_board

    def attempt_move(self, cell, rotation):
        if self.can_insert_token:
            token = self.turn_token()
            success = self.board.attempt_insert(cell, token)
            neutrals = self.board.neutral_tiles()
            if success:
                self.can_insert_token = False
                self.can_rotate = True
                if neutrals:
                    self.can_end_turn = True
        if self.can_rotate and rotation != None:
            direction, tile = self.board.get_rotate_direction(rotation)
            new_tile = self.board.rotate(self.board.field, direction,
                                        tile[0], tile[1])
            self.board.field[tile[0]][tile[1]] = new_tile
            self.can_end_turn = True
        self.red_turn = not(self.red_turn)
        self.can_end_turn = False
        self.can_insert_token = True
        self.can_rotate = False

    def game_loop(self):
        while self.game_running:

            if not self.human_turn():
                start_ai_time = pygame.time.get_ticks()
                token = self.turn_token()
                if token == PentaGoBoard.RED:
                    value, cell, rotation = self.red_player(self,
                        self.board.field, 2, -math.inf, math.inf, True)
                    print('move value: ', value)
                elif token == PentaGoBoard.BLUE:
                    value, cell, rotation = self.blue_player(self,
                        self.board.field, 2, -math.inf, math.inf, True)
                    print('move value: ', value)
                self.attempt_move(cell, rotation)
                stop_ai_time = pygame.time.get_ticks()
                ai_time_span = stop_ai_time - start_ai_time
                if ai_time_span < self.ai_delay:
                    pygame.time.delay(self.ai_delay - ai_time_span)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == MOUSEMOTION:
                    self.selected_items = \
                    PentaGoGraphics.hovered_pos(self.board, self.coords,
                        self.end_turn_button, self.arrow_buttons)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.human_turn():
                        self.handle_click(self.selected_items)

            self.refresh_scores()
            if self.win_check():
                print('winner')
                self.game_running = False

            self.draw()
            pygame.display.flip()
            pygame.time.wait(40)

        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(60)
