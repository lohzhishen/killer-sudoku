import pygame
import numpy as np

# colors
IRON = (217, 219, 220) # background colour (selected)
GREY = (135, 135, 135) # thin separator lines
WHITE = (255, 255, 255) # background colour
BLACK = (0, 0, 0) # separtor lines

# fonts
FONT = None
NORMAL_TEXT = pygame.font.SysFont(FONT, 72) # display numbers in grid
SMALL_TEXT = pygame.font.SysFont(FONT, 24) # display sum of grids
TEXT = pygame.font.SysFont(FONT, 36) # display text in editor

class Board:
    def __init__(self: 'Board', 
                 board: list[list[str]] = None, 
                 sums: list[list[int]] = None, 
                 top_border: list[list[int]] = None,
                 bottom_border: list[list[int]] = None, 
                 left_border: list[list[int]] = None, 
                 right_border: list[list[int]] = None,
                 color: tuple[int, int, int] = BLACK) -> 'Board':
        # record position to draw the board
        self.left = 30
        self.top = 30

        # record size of board
        self.width = 640
        self.height = 640

        # record state of board
        self.data = [board, sums, top_border, bottom_border, left_border, right_border]
        self.find_root()

        # rendering properties
        self.color = color
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.boxes = [[BigBox(self, i, j) for j in range(3)] for i in range(3)]
        self.small_boxes = [[Box(self, i, j, True) for j in range(9)] for i in range(9)]


    @property
    def position(self: 'Board') -> tuple[int, int]:
        return (self.left, self.top)
    

    @property
    def size(self: 'Board') -> None:
        return (self.width, self.height)
    

    def draw(self: 'Board', screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                self.boxes[i][j].draw(screen)
        for i in range(len(self.small_boxes)):
            for j in range(len(self.small_boxes[i])):
                self.small_boxes[i][j].draw(screen)


    def get(self: 'Board', row: int, column: int) -> list[list[list]]:
        return [board[row][column] for board in self.data]
    

    def select(self: 'Board', row: int, column: int) -> None:
        for i in range(9):
            for j in range(9):
                self.small_boxes[i][j].highlight = i == row or j == column or (i // 3 == row // 3 and j // 3 == column // 3)


    def update(self: 'Board', i:int , j: int, k: int, new_value) -> None:
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
                 display_sum: bool,
                 default_color: tuple[int, int, int] = WHITE, 
                 highlighted_color: tuple[int, int, int] = IRON,
                 text_color: tuple[int, int, int] = BLACK,
                 border_color: tuple[int, int, int] = BLACK):
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
        self.display_sum = display_sum
        self.text_color = text_color
        self.default_color = default_color
        self.highlighted_color = highlighted_color
        self.border_color = border_color
        self.highlight = False
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.update() 

    @property
    def value(self):
        return NORMAL_TEXT.render(self.__value[0], True, self.text_color)
    
    @property
    def sum(self):
        return SMALL_TEXT.render(str(self.__value[1]), True, self.text_color)

    def draw(self, screen):
        color = self.highlighted_color if self.highlight else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.value, (self.left + 23, self.top + 13))
        if self.display_sum:
            screen.blit(self.sum, (self.left + 2, self.top + 2))
        for border in self.border:
            pygame.draw.line(screen, self.border_color, *border)

    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self):
        self.__value = self.board.get(self.row, self.column)
        self.border = []
        if self.__value[2]:
            Xs = np.linspace(self.left + 25, self.left + self.width - 10, 6)
            self.border.extend([((Xs[2 * i], self.top + 5), (Xs[2 * i + 1], self.top + 5)) for i in range(3)])
        if self.__value[3]:
            Xs = np.linspace(self.left + 10, self.left + self.width - 10, 8)
            self.border.extend([((Xs[2 * i], self.top + self.height - 5), (Xs[2 * i + 1], self.top + self.height - 5)) for i in range(4)])
        if self.__value[4]:
            Ys = np.linspace(self.top + 25, self.top + self.height - 10, 6)
            self.border.extend([((self.left + 10, Ys[2 * i]), (self.left + 10, Ys[2 * i + 1])) for i in range(3)])
        if self.__value[5]:
            Ys = np.linspace(self.top + 10, self.top + self.height - 10, 8)
            self.border.extend([((self.left + self.width - 10, Ys[2 * i]), (self.left + self.width - 10, Ys[2 * i + 1])) for i in range(4)])
        


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
        self.types = [DigitEditorRow, NumberEditorRow, BooleanEditorRow, BooleanEditorRow, BooleanEditorRow, BooleanEditorRow]
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

    def choose(self, i: int):
        for row in self.editor_rows:
            row.set_active(i == row.row)

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

    def set_active(self, value):
        self.active = value

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


class Button:
    def __init__(self, 
                 text: str = 'CONFIRM',
                 text_color: tuple[int, int, int] = BLACK,
                 background_color: tuple[int, int, int] = BLACK, 
                 foreground_color: tuple[int, int, int] = GREY):
        self.left = 850
        self.top = 250

        self.width = 200
        self.height = 30

        # rendering properties
        self.text = TEXT.render(text, True, text_color)
        width, height = self.text.get_size()
        self.text_xshift = (self.width - width) // 2
        self.text_yshift = (self.height - height) // 2
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.outline = pygame.Rect(self.left, self.top, self.width, self.height)
        self.button = pygame.Rect(self.left + 1, self.top + 1 , self.width - 2, self.height - 2)

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.outline)
        pygame.draw.rect(screen, self.foreground_color, self.button)
        screen.blit(self.text, (self.left + self.text_xshift, self.top + self.text_yshift))

    def collide(self, pos):
        return self.button.collidepoint(pos)
    
class NumberEditorRow(EditorRow):
    def backspace(self):
        i, j = self.editor.selected
        if self.active and i != -1 and j != -1 :
            self.value = int(self.value_text) // 10
            self.board.update(self.row, i, j, int(self.value_text))
    
    def update(self, new_value):
        i, j = self.editor.selected
        if self.active and i != -1 and j != -1:
            try:
                new_value = int(new_value)
                self.value = int(self.value_text) * 10 + new_value
                if int(self.value_text) >= 100:
                    self.value = int(self.value_text) % 100
                self.board.update(self.row, i, j, int(self.value_text))
            except ValueError:
                pass


class BooleanEditorRow(EditorRow):
    def set_active(self, value):
        i, j = self.editor.selected
        if value and i != -1 and j != -1:
            value = True if self.value_text == 'False' else False
            self.value = value
            self.board.update(self.row, i, j, value)
        
        