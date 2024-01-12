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

"""
def draw_board(context, screen):
    # draw the editor
    pygame.draw.rect(screen, BLACK, (700, 50, 501, 181))
    columns = ['Digit', 'Group sum', 'Border (Top)', 'Border (Bottom)', 'Border (Left)', "Border (Right)"]
    label_boxes = [(701, 51 + 30 * i, 249, 29) for i in range(6)]
    context_boxes = [(951, 51 + 30 * i, 249, 29) for i in range(6)]
    for name, label_box, context_box in zip(columns, label_boxes, context_boxes):
        c = box[0] - 701 // 25
        pygame.draw.rect(screen, WHITE, label_box)
        rect = pygame.draw.rect(screen, WHITE, context_box)
        label = TEXT.render(name, True, BLACK)
        x, y = label_box[0], label_box[1]
        screen.blit(label, (x + 5, y + 3))
        context[f'{name}_editor'] = rect
    
    # populate editor information
    r, c = selected[0], selected[1]
    if r != -1 and c != -1:
        x, y = context_boxes[0]
        screen.blit(TEXT.render(board[r][c], True, BLACK), (x + 5, y + 3))
"""
active = False # text editor 
while running:
    
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # allow user to select box
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            skip = False
            for i, row in enumerate(game.small_boxes):
                for j, box in enumerate(row):
                    if box.collide(pos):
                        game.select(i, j)
                        editor.select(i, j)
                        skip = True
                        break
            if not skip:
                for i, row in enumerate(editor.editor_rows):
                    if row.collide(pos):
                        editor.choose(i)
                        break
                else:
                    editor.select(-1)
        
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

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
