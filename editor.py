import pygame

pygame.init()

IRON = (217, 219, 220) # background colour (selected)
GREY = (135, 135, 135) # thin separator lines
WHITE = (255, 255, 255) # background colour
BLACK = (0, 0, 0) # separtor lines

NORMAL_TEXT = pygame.font.SysFont(None, 92) # display numbers in grid
TEXT = pygame.font.SysFont(None, 36)
SMALL_TEXT = pygame.font.SysFont(None, 24) # display sum of grids

screen = pygame.display.set_mode((1280, 720)) # length x height, not resizable
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
context = {'selected': (-1, -1), 'board': board}

def draw_board(context, screen):
    selected = context['selected']
    board = context['board']

    # fill the screen with a color to wipe away anything from last frame
    screen.fill('white')

    # draw the grid
    grid_locations = []
    pygame.draw.rect(screen, BLACK, (30, 30, 640, 640))
    boxes = [(i, j, (31 + i * 213, 31 + j * 213, 212, 212))for j in range(3) for i in range(3)]
    for r, c, box in boxes:
        left, top= box[0], box[1]
        small_boxes = [(3 * r + i, 3 * c + j, pygame.Rect(left + 71 * i, top + 71 * j, 70, 70)) for j in range(3) for i in range(3)]
        grid_locations.extend(small_boxes)
        pygame.draw.rect(screen, GREY, box)
        for r, c, small_box in small_boxes:
            if selected[0] == r or selected[1] == c or (selected[0] // 3 == r // 3 and selected[1] // 3 == c // 3):
                pygame.draw.rect(screen, IRON, small_box)
            else:
                pygame.draw.rect(screen, WHITE, small_box)
            digit = board[r][c]
            if digit != '':
                digit = NORMAL_TEXT.render(digit, True, BLACK)
                x, y = small_box[0], small_box[1]
                screen.blit(digit, (x + 18, y + 6))
    context['grid_locations'] = grid_locations

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

    # flip() the display to put your work on screen
    pygame.display.flip()

active = False # text editor 
while running:
    r, c = context['selected']
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # allow user to select box
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, j, box in context['grid_locations']:
                if box.collidepoint(pos):
                    context['selected'] = (i, j)
            
            if context['Digit_editor'].collidepoint(pos):
                context['Digit_editor_active'] = True
            else:
                context['Digit_editor_active'] = False
        
        elif context.get('Digit_editor_active', False) and event.type == pygame.KEYDOWN:
            if r != -1 and c != -1:
                if event.key == pygame.K_BACKSPACE:
                    context['board'][r][c] = ''
                elif event.unicode in [str(x) for x in range(1, 10)]:
                    context['board'][r][c] = event.unicode
            
    draw_board(context, screen)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
