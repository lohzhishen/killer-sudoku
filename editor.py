import pygame

IRON = (217, 219, 220) # background colour (selected)
GREY = (135, 135, 135) # thin separator lines
WHITE = (255, 255, 255) # background colour
BLACK = (0, 0, 0) # separtor lines

# NORMAL_TEXT = pygame.font.SysFont(None, 24) # display numbers in grid
# SMALL_TEXT = pygame.font.SysFont(None, 11) # display sum of grids

pygame.init()
screen = pygame.display.set_mode((1280, 720)) # length x height, not resizable
clock = pygame.time.Clock()
running = True
dt = 0
context = {'selected': (-1, -1)}

def draw_board(context, screen):
    selected = context['selected']

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

    # flip() the display to put your work on screen
    pygame.display.flip()
    return grid_locations

while running:
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

    context['grid_locations'] = draw_board(context, screen)


    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
