import pygame
pygame.init()
from components import *

screen =  pygame.display.set_mode((1280, 720)) # length x height, not resizable
clock = pygame.time.Clock()
running = True
dt = 0

board = [["3", "", "", "9", "", "6", "1", "", "8"],
         ["", "", "", "", "5", "", "9", "4", "3"],
         ["", "9", "", "", "7", "3", "", "5", ""],
         ["", "1", "3", "", "", "", "", "2", ""],
         ["6", "", "", "", "", "", "", "", ""],
         ["", "", "4", "", "9", "", "", "8", ""],
         ["", "", "8", "2", "", "", "", "", ""],
         ["1", "", "2", "7", "", "4", "", "9", "5"],
         ["", "", "9", "", "", "5", "", "", "1"]]

sums = [[9, 9, 5, 11, 11, 14, 14, 14, 17],
        [15, 9, 16, 13, 13, 21, 20, 17, 17],
        [15, 16, 16, 21, 21, 21, 20, 20, 17],
        [17, 18, 8, 8, 21, 17, 17, 6, 6],
        [17, 18, 10, 10, 4, 17, 6, 6, 9],
        [17, 18, 18, 3, 16, 16, 11, 11, 6],
        [16, 13, 13, 3, 4, 26, 14, 18, 18],
        [16, 16, 13, 13, 4, 26, 14, 13, 18],
        [16, 16, 16, 13, 26, 26, 14, 13, 13]]

top_border = [[True, True, True, True, True, True, True, True, True],
              [True, False, True, True, True, True, True, True, False],
              [False, True, False, True, True, False, False, True, False],
              [True, True, True, True, False, True, True, True, True],
              [False, False, True, True, True, False, True, True, True],
              [False, False, True, True, True, True, True, True, True],
              [True, True, True, False, True, True, True, True, True],
              [False, True, False, True, False, False, False, True, False],
              [False, True, True, False, True, False, False, False, True]]

bottom_border = [[True, False, True, True, True, True, True, True, False],
                 [False, True, False, True, True, False, False, True, False],
                 [True, True, True, True, False, True, True, True, True],
                 [False, False, True, True, True, False, True, True, True],
                 [False, False, True, True, True, True, True, True, True],
                 [True, True, True, False, True, True, True, True, True],
                 [False, True, False, True, False, False, False, True, False],
                 [False, True, True, False, True, False, False, False, True],
                 [True, True, True, True, True, True, True, True, True]]

left_border = [[True, False, True, True, False, True, False, False, True],
               [True, True, True, True, False, True, True, True, False],
               [True, True, False, True, False, False, True, False, True],
               [True, True, True, False, True, True, False, True, False],
               [True, True, True, False, True, True, True, False, True],
               [True, True, False, True, True, False, True, False, True],
               [True, True, False, True, True, True, True, True, False],
               [True, False, True, True, True, True, True, True, True],
               [True, True, False, True, True, False, True, True, False]]

right_border = [[False, True, True, False, True, False, False, True, True],
                [True, True, True, False, True, True, True, False, True],
                [True, False, True, False, False, True, False, True, True],
                [True, True, False, True, True, False, True, False, True],
                [True, True, False, True, True, True, False, True, True],
                [True, False, True, True, False, True, False, True, True],
                [True, False, True, True, True, True, True, False, True],
                [False, True, True, True, True, True, True, True, True],
                [True, False, True, True, False, True, True, False, True]]

game = Board(board, sums, top_border, bottom_border, left_border, right_border)
editor = Editor(game)
button = Button()

while running:
    
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # listener for mouse clicks
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            skip = False
            # allow user to select box
            for i, row in enumerate(game.small_boxes):
                for j, box in enumerate(row):
                    if box.collide(pos):
                        game.select(i, j)
                        editor.select(i, j)
                        skip = True
                        break
            # allow user to select editor
            if not skip:
                for i, row in enumerate(editor.editor_rows):
                    if row.collide(pos):
                        editor.choose(i)
                        skip = True
                        break
                else:
                    editor.choose(-1)
            # allow user to select confirm
            if not skip:
                if button.collide(pos):
                    running = False

        # allow user to edit editor
        elif event.type == pygame.KEYDOWN:
            for i, row in enumerate(editor.editor_rows):
                if isinstance(row, DigitEditorRow):
                    if event.key == pygame.K_BACKSPACE:
                        row.backspace()
                    else:
                        row.update(event.unicode)
                
    # fill the screen with a color to wipe away anything from last frame
    screen.fill('white')

    # draw the new frame
    game.draw(screen)
    editor.draw(screen)
    button.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
