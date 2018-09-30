import pygame
import math

OFFSET_CANVAS = 50
CELL_SIZE = 100
TOP_OFFSET = 20
BOTTOM_SPACING = 50
MIDDLE_SPACING = 25
FONTSIZE = 40

BLACK  = (  0,   0,   0)
GREY   = (109, 109, 109)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (250, 240, 190)

def setup_display(board):
    window_width = 2 * OFFSET_CANVAS + board.macro_width * \
        board.micro_width * CELL_SIZE + MIDDLE_SPACING
    window_height = 2 * OFFSET_CANVAS + TOP_OFFSET + BOTTOM_SPACING + \
        board.macro_height * board.micro_height * CELL_SIZE + MIDDLE_SPACING
    display = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('PentaGo')
    gamefont = pygame.font.Font(None, FONTSIZE)
    return (display, gamefont, window_width, window_height)

def draw_board(game_display,
        board, selected_index, game_running,
        player_turn, red_turn, winner, can_end_turn):
    (display, gamefont, window_width, window_height) = game_display
    display.fill(YELLOW)
    top_left = [OFFSET_CANVAS, OFFSET_CANVAS + TOP_OFFSET]
    bottom_right = [None, None]
    coords = []
    for i in range(board.macro_height):
        coords.append([])
        for j in range(board.macro_width):
            coords[i].append([])
            bottom_right[0] = top_left[0] + board.micro_width * CELL_SIZE
            bottom_right[1] = top_left[1] + board.micro_height * CELL_SIZE
            pygame.draw.rect(display, BLACK,
                            (top_left, [board.micro_width * CELL_SIZE,
                            board.micro_height * CELL_SIZE]), 2)
            centre = [int(ordinate + 1/2 * CELL_SIZE) for ordinate in top_left]
            left_centre_x = centre[0]
            for row in range(board.micro_height):
                centre[0] = left_centre_x
                coords[i][j].append([])
                for cell in range(board.micro_height):
                    coords[i][j][row].append([ordinate - 1/2 * CELL_SIZE \
                    for ordinate in centre])
                    token = board.field[i][j][row][cell]
                    if token == 0:
                        pygame.draw.circle(display, GREY, centre, int(CELL_SIZE/2 - 20), 2)
                    elif token == 1:
                        pygame.draw.circle(display, RED, centre, int(CELL_SIZE/2 - 20), 0)
                    else:
                        pygame.draw.circle(display, BLUE, centre, int(CELL_SIZE/2 - 20), 0)
                    centre[0] += CELL_SIZE
                centre[1] += CELL_SIZE
            top_left[0] += MIDDLE_SPACING + board.micro_width * CELL_SIZE
        top_left[0] = OFFSET_CANVAS
        top_left[1] = bottom_right[1] + MIDDLE_SPACING

    arc_areas = [
                pygame.Rect(20, 20 + TOP_OFFSET, OFFSET_CANVAS - 5, OFFSET_CANVAS - 5),
                pygame.Rect(window_width - 20, 20 + TOP_OFFSET, 5 - OFFSET_CANVAS, OFFSET_CANVAS - 5),
                pygame.Rect(window_width - 20, window_height -20 - BOTTOM_SPACING, 5 - OFFSET_CANVAS, 5 - OFFSET_CANVAS),
                pygame.Rect(20, window_height - 20 - BOTTOM_SPACING, OFFSET_CANVAS - 5, 5 - OFFSET_CANVAS)]
    for rect in arc_areas:
        pygame.Rect.normalize(rect)
    arc_angles = []
    x = 1/2 * math.pi
    for n in range(board.macro_width + board.macro_height):
        arc_angles.append([x, x + 1/2 * math.pi])
        x -= 1/2 * math.pi

    arrow_pos = [
    [0, math.pi/2, math.pi, 3*math.pi/2],
    [None, None, None, None],
    [[0,6], [6,0], [0,-6], [-6,0]]
    ]

    arrow_buttons = []
    for p in range(len(arc_areas)):
        pygame.draw.arc(display, BLACK, arc_areas[p], arc_angles[p][0], arc_angles[p][1], 3)
        arrow_pos[1] = [arc_areas[p].midright, arc_areas[p].midtop,
                        arc_areas[p].midleft, arc_areas[p].midbottom]
        i = 0
        for angle in arc_angles[p]:
            if angle < 0: angle += 2*math.pi
            index = arrow_pos[0].index(angle)
            a = arrow_pos[1][index]
            b = arrow_pos[2][index]
            c = [b[1], b[0]]
            if i == 0:
                tip = [a[i] + b[i] for i in range(2)]
                back_right = [a[i] - b[i] + c[i]  for i in range(2)]
                back_left = [a[i] - b[i] - c[i]  for i in range(2)]
            else:
                tip = [a[i] - b[i] for i in range(2)]
                back_right = [a[i] + b[i] + c[i]  for i in range(2)]
                back_left = [a[i] + b[i] - c[i]  for i in range(2)]
            pygame.draw.polygon(display, RED, [tip, back_right, back_left], 0)
            tl_corner = [min([tip[n],back_left[n],back_right[n]]) for n in range(2)]
            br_corner = [max([tip[m],back_left[m],back_right[m]]) for m in range(2)]
            box_dims = [br_corner[q]-tl_corner[q] for q in range(2)]
            arrow_buttons.append(pygame.Rect(tl_corner, box_dims))
            i += 1

    if can_end_turn:
        BOX_COLOUR = BLUE
        TEXT_COLOUR = WHITE
    else:
        BOX_COLOUR = GREY
        TEXT_COLOUR = BLACK

    end_turn_button = pygame.Rect(window_width/2 - 90, window_height - BOTTOM_SPACING - 30,
                                    180, BOTTOM_SPACING + 10)
    pygame.draw.rect(display, BOX_COLOUR, end_turn_button, 0)
    end_turn_text = gamefont.render('END TURN', False, TEXT_COLOUR)
    text_x = end_turn_button.centerx - 1/2 * end_turn_text.get_width()
    text_y = end_turn_button.centery - 1/2 * end_turn_text.get_height()
    display.blit(end_turn_text, (text_x, text_y))

    return coords, end_turn_button, arrow_buttons

def hovered_pos(board, coords, end_turn_button, arrow_buttons):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    for macro_row in coords:
        for macro_col in macro_row:
            for micro_row in macro_col:
                for cell in micro_row:
                    end_x = cell[0] + CELL_SIZE
                    end_y = cell[1] + CELL_SIZE
                    if mouse_x > cell[0] and mouse_x < end_x \
                    and mouse_y > cell[1] and mouse_y < end_y:
                        return [coords.index(macro_row), macro_row.index(macro_col),
                        macro_col.index(micro_row), micro_row.index(cell)]
    if end_turn_button.collidepoint(mouse_x, mouse_y):
        return -2
    for button in arrow_buttons:
        if button.collidepoint(mouse_x, mouse_y):
            return (-3, arrow_buttons.index(button))
    return -1
