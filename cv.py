from pyautogui import screenshot, alert
from pynput import mouse
from time import sleep
from functools import partial
from numpy import linspace
from PIL import Image
from pytesseract import image_to_string
from re import sub
import matplotlib.pyplot as plt
import sudoku


def on_click(context: dict, x: int, y: int, button: mouse.Button, pressed: bool) -> None | bool:
    """Listener for detecting area selected by user. Records the position where the mouse was pressed 
    position where the mouse was released."""
    # click detection
    if button == mouse.Button.left and pressed and not context.get('pressed', False): 
        context['top left'] = (x, y)
        context['pressed'] = pressed

    # release detection
    elif button == mouse.Button.left and not pressed and context.get('pressed', False): 
        context['bottom right'] = (x, y)
        del context['pressed']
        # stop listener
        return False 
    

def get_screenshot(context: dict) -> Image:
    """Returns a screenshot of area selected by the user."""
    # obtain region selected by user
    on_click_contextualised = partial(on_click, context)
    with mouse.Listener(on_click=on_click_contextualised) as listener:
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
    screen = screenshot(region=(left, top, width, height))
    return screen


def scan_sudoku_board(context: dict) -> Image:
    # instruct the user on how to select region
    alert(text='Click and drag to outline the sudoku board.', title=context['title'], button='OK')
    sleep(1)
    screen = get_screenshot(context)
    area = context['width'] * context['height']

    # region selected is too small
    while area < 200_000:
        alert(text='Area selected is too small. Maximise the window and try again.', title=context['title'], button='OK')
        screen = get_screenshot(context)
        area = context['width'] * context['height']

    # record screen    
    return screen


def calculate_box_dimensions(context: dict) -> None:
    """Compute the width and height of a single box in the sudoku grid."""
    context['box width'] = context['width'] // sudoku.SUDOKU_SIZE
    context['box height'] = context['height'] // sudoku.SUDOKU_SIZE


def calculate_box_centers(context: dict) -> list[list[list[int, int]]]:
    """Compute the centers of each box within the sudoku grid."""
    calculate_box_dimensions(context)

    # obtain the coordiates of the center of the top left square
    left, top = context['top left']
    left_ = left + context['box width'] // 2
    top_ = top + context['box height'] // 2

    # obtain the coordinates of the center of the bottom right square
    right, bottom = left + context['width'], top + context['height']
    right_ = right - context['box width'] // 2
    bottom_ = bottom - context['box height'] // 2

    # create grid
    Xs = linspace(left_, right_, sudoku.SUDOKU_SIZE, endpoint=True)
    Ys = linspace(top_, bottom_, sudoku.SUDOKU_SIZE, endpoint=True)
    return [[[Xs[i], Ys[j]] for i in range(sudoku.SUDOKU_SIZE)] for j in range(sudoku.SUDOKU_SIZE)]


def detect_number(image: Image) -> int | None:
    detected = image_to_string(image, config='--psm 10')
    return sub("[^1-9]", "", detected)


def get_digit_roi(context: dict, i: int, j: int) -> Image:
    anchor_x, anchor_y = context['top left']
    x, y = context['box centers'][i][j]
    top = y - context['box height'] // 4 - anchor_y
    bottom = y + context['box height'] // 4 - anchor_y
    left = x - context['box width'] // 4 - anchor_x
    right = x + context['box width'] // 4 - anchor_x
    return context['screen'].crop(box=(left, top, right, bottom))


def get_sum_roi(context: dict, i: int, j: int) -> Image:
    anchor_x, anchor_y = context['top left']
    x, y = context['box centers'][i][j]
    top = y - context['box height'] // 2 - anchor_y
    bottom = y - context['box height'] // 6 - anchor_y
    left = x - context['box width'] // 2 - anchor_x
    right = x - context['box width'] // 6 - anchor_x
    return context['screen'].crop(box=(left, top, right, bottom))


def sudoku_image_to_array(context: dict) -> list[list[int]]:
    grid = [[0 for _ in range(sudoku.SUDOKU_SIZE)] for _ in range(sudoku.SUDOKU_SIZE)]
    for i in range(sudoku.SUDOKU_SIZE):
        for j in range(sudoku.SUDOKU_SIZE):
            crop = get_digit_roi(context, i, j)
            grid[i][j] = detect_number(crop)
    return grid


def scan(context: dict) -> None:
    """"""
    # obtain screenshot of sudoku board
    context['screen'] = scan_sudoku_board(context)
    
    # obtain coordinates for all the boxes within the sudoku game
    context['box centers'] = calculate_box_centers(context)

    # obtain array representation of sudoku board
    context['board'] = sudoku_image_to_array(context)
    
    
