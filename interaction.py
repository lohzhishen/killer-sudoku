"""This module documents all interactions with the computer interface."""
import numpy as np
import functools
import pyautogui
import pynput
import time
import PIL


from config import *


class Controller:
    @staticmethod
    def act(context: dict, i: int, j: int, digit: str) -> None:
        """Keys in the specified digit at the given box in the sudoku game."""
        assert context.get('box centers', None) is not None
        assert len(context['box centers']) == SUDOKU_SIZE and len(context['box centers'][i]) == SUDOKU_SIZE
        assert 0 <= i < SUDOKU_SIZE and 0 <= j < SUDOKU_SIZE
        assert digit in '123456789'
        pyautogui.click(*context['box centers'][i][j])
        pyautogui.write(digit)

    @staticmethod
    def implement_solution(context: dict, solution: list[list[str]]) -> None:
        """Takes control over the mouse and keyboard to enter the solution into the sudoku board."""
        assert len(solution) == SUDOKU_SIZE and len(solution[0]) == SUDOKU_SIZE
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                digit = solution[i][j]
                Controller.act(context, i, j, digit)

    @staticmethod
    def calculate_box_dimensions(context: dict) -> None:
        """Compute the width and height of a single box in the sudoku grid."""
        context['box width'] = context['width'] // SUDOKU_SIZE
        context['box height'] = context['height'] // SUDOKU_SIZE

    @staticmethod
    def calculate_box_centers(context: dict) -> list[list[list[int, int]]]:
        """Compute the centers of each box within the sudoku grid."""
        Controller.calculate_box_dimensions(context)

        # obtain the coordiates of the center of the top left square
        left, top = context['top left']
        left_ = left + context['box width'] // 2
        top_ = top + context['box height'] // 2

        # obtain the coordinates of the center of the bottom right square
        right, bottom = left + context['width'], top + context['height']
        right_ = right - context['box width'] // 2
        bottom_ = bottom - context['box height'] // 2

        # create grid
        Xs = np.linspace(left_, right_, SUDOKU_SIZE, endpoint=True)
        Ys = np.linspace(top_, bottom_, SUDOKU_SIZE, endpoint=True)
        return [[[Xs[i], Ys[j]] for i in range(SUDOKU_SIZE)] for j in range(SUDOKU_SIZE)]

  
class Screenshot:
    @staticmethod
    def on_click(context: dict, x: int, y: int, button: pynput.mouse.Button, pressed: bool) -> None | bool:
        """Listener for detecting area selected by user. Records the position where the mouse was pressed 
        position where the mouse was released."""
        # click detection
        if button == pynput.mouse.Button.left and pressed and not context.get('pressed', False): 
            context['top left'] = (x, y)
            context['pressed'] = pressed

        # release detection
        elif button == pynput.mouse.Button.left and not pressed and context.get('pressed', False): 
            context['bottom right'] = (x, y)
            del context['pressed']
            # stop listener
            return False 
        
    @staticmethod
    def get_screenshot(context: dict) -> PIL.Image:
        """Returns a screenshot of area selected by the user."""
        # obtain region selected by user
        on_click_contextualised = functools.partial(Screenshot.on_click, context)
        with pynput.mouse.Listener(on_click=on_click_contextualised) as listener:
            listener.join()
        left, top = context['top left']
        right, bottom = context['bottom right']

        # ensure consistency of left and right
        if left > right:
            left, right = right, left
        # ensure consistency of top and bottom
        if top > bottom:
            top, bottom = bottom, top
        
        # compute and record details of region
        width = right - left
        height = bottom - top
        context['top left'] = (left, top)
        context['width'] = width
        context['height'] = height

        # take screenshot
        screen = pyautogui.screenshot(region=(left, top, width, height))
        return screen

    @staticmethod
    def scan_sudoku_board(context: dict) -> PIL.Image:
        """Returns a image of the sudoku game board."""
        # instruct the user on how to select region
        pyautogui.alert(text='Click and drag to outline the sudoku board.', title=context['title'], button='OK')
        time.sleep(1)
        screen = Screenshot.get_screenshot(context)
        area = context['width'] * context['height']

        # region selected is too small
        while area < 200_000:
            pyautogui.alert(text='Area selected is too small. Maximise the window and try again.', 
                title=context['title'], button='OK')
            screen = Screenshot.get_screenshot(context)
            area = context['width'] * context['height']

        # record screen    
        return screen
    
