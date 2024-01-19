import pygame
pygame.init()
from components import *


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


class KillerSudokuEditor:
    def __init__(self: 'KillerSudokuEditor', 
                 board: list[list[str]], 
                 sums: list[list[int]],
                 top_border: list[list[bool]],
                 bottom_border: list[list[bool]],
                 left_border: list[list[bool]],
                 right_border: list[list[bool]]
                 ) -> None:
        
        # settings
        self.screen_size = (1280, 720)

        # state
        self.screen =  pygame.display.set_mode(self.screen_size) # length x height, not resizable
        self.game = Board(board, sums, top_border, bottom_border, left_border, right_border)
        self.editor = Editor(self.game)
        self.button = Button()
        self.running = False

    def draw(self: 'KillerSudokuEditor') -> None:
        if self.running:
            # wipe away anything from last frame
            self.screen.fill('white')

            # draw the new frame
            self.game.draw(self.screen)
            self.editor.draw(self.screen)
            self.button.draw(self.screen)

            # display on screen
            pygame.display.flip()

    def stop(self: 'KillerSudokuEditor') -> None:
        self.running = False

    def check_click_small_box(self: 'KillerSudokuEditor', pos: tuple[int, int]) -> bool:
        if not self.running:
            return False
        for i, row in enumerate(self.game.small_boxes):
            for j, box in enumerate(row):
                if box.collide(pos):
                    self.game.select(i, j)
                    self.editor.select(i, j)
                    return True
        return False

    def check_click_editor_row(self: 'KillerSudokuEditor', pos: tuple[int, int]) -> bool:
        if not self.running:
            return False
        for i, row in enumerate(self.editor.editor_rows):
            if row.collide(pos):
                self.editor.choose(i)
                return True
        self.editor.choose(-1)
        return False

    def check_click_button(self: 'KillerSudokuEditor', pos: tuple[int, int]) -> bool:
        if not self.running:
            return False
        elif self.button.collide(pos):
            self.stop()
            return True
        return False
    
    def handle_key_press(self: 'KillerSudokuEditor', event: pygame.event.Event) -> None:
        if not self.running:
            return
        for row in self.editor.editor_rows:
            if isinstance(row, DigitEditorRow) or isinstance(row, NumberEditorRow):
                if event.key == pygame.K_BACKSPACE:
                    row.backspace()
                else:
                    row.update(event.unicode)
            
    def start(self: 'KillerSudokuEditor') -> list:
        self.running = True
        while self.running:
            
            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                
                # listener for mouse clicks
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if (self.check_click_small_box(pos) or 
                        self.check_click_editor_row(pos) or 
                        self.check_click_button(pos)):
                        continue

                # allow user to edit editor
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event)
                    
            self.draw()          
        pygame.quit()
        return self.game.data

if __name__ == '__main__':
    editor = KillerSudokuEditor(board, sums, top_border, bottom_border, left_border, right_border)
    editor.start()