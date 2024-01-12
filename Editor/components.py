import pygame

# colors
IRON = (217, 219, 220) # background colour (selected)
GREY = (135, 135, 135) # thin separator lines
WHITE = (255, 255, 255) # background colour
BLACK = (0, 0, 0) # separtor lines

# fonts
NORMAL_TEXT = pygame.font.SysFont(None, 92) # display numbers in grid
SMALL_TEXT = pygame.font.SysFont(None, 24) # display sum of grids
TEXT = pygame.font.SysFont(None, 36)

class Board:
    def __init__(self, 
                 board: list[list[str]] = None, 
                 sums: list[list[int]] = None, 
                 top_border: list[list[int]] = None,
                 bottom_border: list[list[int]] = None, 
                 left_border: list[list[int]] = None, 
                 right_border: list[list[int]] = None,
                 color: tuple[int, int, int] = BLACK):
        # record position to draw the board
        self.left = 30
        self.top = 30

        # record size of board
        self.width = 640
        self.height = 640

        # record state of board
        self.data = [board, sums, top_border, bottom_border, left_border, right_border]

        # rendering properties
        self.color = color
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.boxes = [[BigBox(self, i, j) for j in range(3)] for i in range(3)]
        self.small_boxes = [[Box(self, i, j) for j in range(9)] for i in range(9)]

    @property
    def position(self):
        return (self.left, self.top)
    
    @property
    def size(self):
        return (self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                self.boxes[i][j].draw(screen)
        for i in range(len(self.small_boxes)):
            for j in range(len(self.small_boxes[i])):
                self.small_boxes[i][j].draw(screen)

    def get(self, row: int, column: int):
        # UPDATE TO RETURN ALL GRID INFO
        return (self.data[0][row][column], 0, False, False, False, False)
        return (board[row][colum] for board in self.data)
    
    def select(self, row: int, column: int):
        for i in range(9):
            for j in range(9):
                self.small_boxes[i][j].highlight = i == row or j == column or (i // 3 == row // 3 and j // 3 == column // 3)

    def update(self, i:int , j: int, k: int, new_value):
        self.data[i][j][k] = new_value
        self.small_boxes[j][k].update()

class BigBox:
    def __init__(self, 
                 board: Board, row: int, column: int, 
                 color: tuple[int, int, int] = GREY):
        # position within the board
        self.row = row
        self.column = column 
        
        # size of box
        game_width, game_height = board.size
        self.width = (game_width - 4) // 3
        self.height = (game_height - 4) // 3
        
        # position on the screen
        game_left, game_top = board.position
        self.left = game_left + 1 + self.row * (self.width + 1)
        self.top = game_top + 1 + self.column * (self.height + 1)
        
        # rendering properties
        self.color = color
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Box:
    def __init__(self, 
                 board: Board, row: int, column: int,
                 default_color: tuple[int, int, int] = WHITE, 
                 highlighted_color: tuple[int, int, int] = IRON,
                 text_color: tuple[int, int, int] = BLACK):
        # position within the board
        self.row = row
        self.column = column
        self.board = board

        # size of box
        game_width, game_height = board.size
        self.width = (game_width - 10) // 9
        self.height = (game_height - 10) // 9

        # position on the screen
        game_left, game_top = board.position
        self.left = game_left + 1 + (self.width + 1) * row
        self.top = game_top + 1 + (self.height + 1) * column
        
        # rendering properties
        self.text_color = text_color
        self.default_color = default_color
        self.highlighted_color = highlighted_color
        self.highlight = False
        self.__value = board.get(self.row, self.column)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    @property
    def value(self):
        return NORMAL_TEXT.render(self.__value[0], True, self.text_color)

    def draw(self, screen):
        color = self.highlighted_color if self.highlight else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.value, (self.left + 18, self.top + 6))

    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self):
        self.__value = self.board.get(self.row, self.column)
    

class Editor:
    def __init__(self, board: Board):
        # record position to draw the editor
        self.left = 700
        self.top = 50

        # record size of board
        self.width = 501
        self.height = 181

        # record the state of the editor
        self.board = board
        self.selected = (-1, -1)

        # rendering properties
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.rows = ['Digit', 'Group sum', 'Border (Top)', 'Border (Bottom)', 'Border (Left)', "Border (Right)"]
        self.types = [DigitEditorRow, EditorRow, EditorRow, EditorRow, EditorRow, EditorRow]
        self.editor_rows = [c(self, board, i, label) for c, i, label in zip(self.types, range(len(self.rows)), self.rows)]


    @property
    def position(self):
        return (self.left, self.top)

    @property
    def size(self):
        return (self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        for row in self.editor_rows:
            row.draw(screen)

    def choose(self, i):
        for row in self.editor_rows:
            row.active = i == row.row

    def select(self, i, j):
        self.selected = (i, j)
        for value, row in zip(self.board.get(*self.selected), self.editor_rows):
            row.value = value


class EditorRow:
    def __init__(self, editor:Editor, board: Board, row: int, label: str, 
                 background_color: tuple[int, int, int] = WHITE,
                 text_color: tuple[int, int, int] = BLACK):
        # record position within the editor
        self.row = row

        # record size 
        editor_width, editor_height = editor.size
        self.width = (editor_width - 3) // 2
        self.height = (editor_height - 7) // 6

        # record position within the editor
        editor_left, editor_top = editor.position
        self.label_left = editor_left + 1
        self.content_left = editor_left + self.width + 2
        self.label_top = editor_top + 1 + (self.height + 1) * self.row
        self.content_top = self.label_top

        # rendering properties
        self.background_color = background_color
        self.text_color = text_color
        self.label = TEXT.render(label, True, self.text_color)
        self.value_text = ''
        self.label_rect = pygame.Rect(self.label_left, self.label_top, self.width, self.height)
        self.content_rect = pygame.Rect(self.content_left, self.content_top, self.width, self.height)

        # record state of editor
        self.active = False
        self.board = board
        self.editor = editor

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.label_rect)
        pygame.draw.rect(screen, self.background_color, self.content_rect)
        screen.blit(self.label, (self.label_left + 5, self.label_top + 3))
        screen.blit(self.value, (self.content_left + 5, self.content_top + 3))

    def collide(self, pos):
        return self.content_rect.collidepoint(pos)
    
    @property
    def value(self):
        return TEXT.render(self.value_text, True, self.text_color)
    
    @value.setter
    def value(self, value):
        self.value_text = str(value)

class DigitEditorRow(EditorRow):
    valid = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '']

    def backspace(self):
        self.update('')

    def update(self, new_value):
        i, j = self.editor.selected
        if self.active and i != -1 and j != -1 and new_value in self.valid:
            self.value = new_value
            self.board.update(self.row, i, j, new_value)

