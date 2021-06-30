import pygame, sys
import numpy as np
import time

pygame.init()

WIDTH = 900
HEIGHT = 900
CIRCLE_RADIOUS = 90
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
SPACE = 65

MEDIUM_FONT = pygame.font.SysFont('Comic Sans MS', 25)
END_FONT =  pygame.font.SysFont('Comic Sans MS', 40)

LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (153, 255, 255) #skyblue
CIRCLE_COLOR = (255, 51, 153) 
CROSS_COLOR = (51, 255, 51)
BOARD_ROWS = 3
BOARD_COLUMNS = 3
RED = (255, 0, 0)

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('KÓŁKO I KRZYŻYK')
screen.fill(BACKGROUND_COLOR)

board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))


#pygame.draw.line(screen, BLACK, (10,10), (300,300), 10)

def board_draw():
    #horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (50,300), (850,300), 10)
    pygame.draw.line(screen, LINE_COLOR, (50,600), (850,600), 10)
    
    #vertical lines
    pygame.draw.line(screen, LINE_COLOR, (300,50), (300,850), 10)
    pygame.draw.line(screen, LINE_COLOR, (600,50), (600,850), 10)

def pick_square(row, column, player):
    board[row][column] = player

def draw_figures():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(column*300+300/2), int(row*300+300/2)), CIRCLE_RADIOUS, CIRCLE_WIDTH)
            elif board[row][column] == 2:
                 pygame.draw.line(screen, CROSS_COLOR, (column*300+SPACE, row*300+300-SPACE), (column*300+300-SPACE, row*300+SPACE), CROSS_WIDTH)
                 pygame.draw.line(screen, CROSS_COLOR, (column*300+SPACE, row*300+SPACE), (column*300+300-SPACE, row*300+300-SPACE), CROSS_WIDTH)

def doable_move(row, column):
    if board[row][column] == 0:
        return True
    else:
        return False
    
def is_game_over():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 0:
                return False
    return True

def check_if_win(player):
    for column in range(BOARD_COLUMNS):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            winning_line_vertical(column, player)
            return True

    #hor win check
    for row in range(BOARD_ROWS):
             if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                 winning_line_horizontal(row,player)
                 return True

    #asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        winning_line_diagonal_asc(player)
        return True
    
    #desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        winning_line_diagonal_desc(player)
        return True

    return False

def winning_line_vertical(col, player):
    positoionX = col*300+150

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (positoionX, 15), (positoionX, HEIGHT - 15), 15)

def winning_line_horizontal(row, player):
    positoionY = row*300+150

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, positoionY), (WIDTH - 15,positoionY), 15)

def winning_line_diagonal_asc(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def winning_line_diagonal_desc(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def win(text):
    screen.fill(BACKGROUND_COLOR)
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            board[row][column] = 0
    restart_message = MEDIUM_FONT.render("Press R to RESTART", True, RED)
    screen.blit(text, (270, 420))
    screen.blit(restart_message, (300, 470))

def restart():
    screen.fill(BACKGROUND_COLOR)
    board_draw()
    player = 1
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            board[row][column] = 0

board_draw()

player = 1
game_over = False
# mainloop in every pygame program
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            
            
            mouseX = event.pos[0] #x
            mouseY = event.pos[1] #y
            
            picked_row = int(mouseY // 300)
            picked_column = int(mouseX // 300)
            
            if doable_move(picked_row, picked_column):
                if player == 1:
                    pick_square(picked_row, picked_column, 1)
                    if check_if_win(player):
                        game_over = True
                        text = MEDIUM_FONT.render("Press ENTER to continue.", True, RED)
                        screen.blit(text, (565, 870))
                    player = 2

                elif player == 2:
                    pick_square(picked_row, picked_column, 2)
                    if check_if_win(player):
                        game_over = True
                        text = MEDIUM_FONT.render("Press ENTER to continue.", True, RED)
                        screen.blit(text, (565, 870))
                    player = 1


                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False
            elif event.key == pygame.K_RETURN:
                if player == 2:
                    message = END_FONT.render("PLAYER 1 WON!", True, LINE_COLOR)
                else:
                     message = END_FONT.render("PLAYER 2 WON!", True, LINE_COLOR)
                win(message)




    pygame.display.update()
    
