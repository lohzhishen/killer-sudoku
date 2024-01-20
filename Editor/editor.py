import pygame
pygame.init()
from .components import *


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

