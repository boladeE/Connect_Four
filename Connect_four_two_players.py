import numpy as np
import pygame
import math
import random

game_over = False
Player_one_turn = random.choice([True, False])
ROW_COUNT = 6
COLUMN_COUNT = 7
player_piece = 1
ai_piece = 2
window_length = 4
empty = 0

# Py game stuff
pygame.init()
square = 100
width = COLUMN_COUNT * square
height = (ROW_COUNT + 1) * square
radius = int(square/2 - 5)
font = pygame.font.SysFont("Times new roman", 75)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yel = (255, 255, 0)
screen = pygame.display.set_mode((width, height))


def draw_board(dot):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, blue, (c * square, r * square + square, square, square))
            pygame.draw.circle(screen, black, (int(c * square + square / 2), int(r * square + square * (3 / 2))),
                               radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if dot[r][c] == player_piece:
                pygame.draw.circle(screen, red, (int(c * square + square / 2), height - int(r * square + square/2)),
                                   radius)
            elif dot[r][c] == ai_piece:
                pygame.draw.circle(screen, yel, (int(c * square + square / 2), height - int(r * square + square/2)),
                                   radius)

    pygame.display.update()


def create_board():
    fish = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return fish


def drop_piece(dot, r, c, piece):
    dot[r][c] = piece


def valid_selection(dot, c):
    return dot[ROW_COUNT - 1][c] == 0


def get_next_open_row(dot, c):
    for i in range(ROW_COUNT):
        if dot[i][c] == 0:
            return i


def print_board(dot):
    print(np.flip(dot, 0))


def win(piece):
    # checking the rows
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece \
                    and board[r][c + 1] == piece \
                    and board[r][c + 2] == piece \
                    and board[r][c + 3] == piece:
                return True

    # checking the columns
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece \
                    and board[r + 1][c] == piece \
                    and board[r + 2][c] == piece \
                    and board[r + 3][c] == piece:
                return True

    # checking the positive slope diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece \
                    and board[r + 1][c + 1] == piece \
                    and board[r + 2][c + 2] == piece \
                    and board[r + 3][c + 3] == piece:
                return True

    # checking the negative slope diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece \
                    and board[r - 1][c + 1] == piece \
                    and board[r - 2][c + 2] == piece \
                    and board[r - 3][c] == piece:
                return True


board = create_board()
draw_board(board)
# game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, square))
            posx = event.pos[0]
            if Player_one_turn:
                pygame.draw.circle(screen, red, (posx, int(square/2)), radius)
            elif not Player_one_turn:
                pygame.draw.circle(screen, yel, (posx, int(square/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, square))
            if Player_one_turn:
                position_x = event.pos[0]
                column = int(math.floor(position_x/square))
                Player_one_turn = False

                if valid_selection(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, player_piece)

                    if win(1):
                        label = font.render("Player one wins", 1, red)
                        screen.blit(label, (40, 10))
                        game_over = True
                    draw_board(board)

            elif not Player_one_turn:
                position_x = event.pos[0]
                column = int(math.floor(position_x/square))
                Player_one_turn = True

                if valid_selection(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, ai_piece)

                    if win(2):
                        label = font.render("Player two wins", 2, yel)
                        screen.blit(label, (40, 10))
                        game_over = True
                    draw_board(board)
    if game_over:
        pygame.time.wait(3000)