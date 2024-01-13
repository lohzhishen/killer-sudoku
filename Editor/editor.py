import pygame
pygame.init()

from components import *

screen =  pygame.display.set_mode((1280, 720)) # length x height, not resizable
clock = pygame.time.Clock()
running = True
dt = 0

board = [["", "2", "", "", "3", "", "5", "6", ""],
         ["9", "1", "5", "", "", "", "", "4", ""],
         ["6", "", "", "5", "4", "", "1", "9", ""],
         ["", "", "", "", "1", "", "", "7", ""],
         ["", "", "9", "2", "6", "", "8", "5", ""],
         ["", "7", "", "4", "", "", "", "", "6"],
         ["", "9", "", "6", "", "", "7", "", ""],
         ["", "", "4", "3", "", "", "2", "", ""],
         ["", "", "", "", "9", "", "6", "", ""]]

game = Board(board)
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
