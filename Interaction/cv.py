from pyautogui import screenshot, alert
from pynput import mouse
from time import sleep
from functools import partial
from numpy import linspace
from PIL import Image
from pytesseract import image_to_string
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.filters import threshold_multiotsu
from skimage.measure import label, regionprops
import numpy as np
import matplotlib.pyplot as plt
import config


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
        alert(text='Area selected is too small. Maximise the window and try again.', 
              title=context['title'], button='OK')
        screen = get_screenshot(context)
        area = context['width'] * context['height']

    # record screen    
    return screen


def calculate_box_dimensions(context: dict) -> None:
    """Compute the width and height of a single box in the sudoku grid."""
    context['box width'] = context['width'] // config.SUDOKU_SIZE
    context['box height'] = context['height'] // config.SUDOKU_SIZE


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
    Xs = linspace(left_, right_, config.SUDOKU_SIZE, endpoint=True)
    Ys = linspace(top_, bottom_, config.SUDOKU_SIZE, endpoint=True)
    return [[[Xs[i], Ys[j]] for i in range(config.SUDOKU_SIZE)] for j in range(config.SUDOKU_SIZE)]


def detect_number(image: Image) -> int | None:
    image = np.pad(image, 5, constant_values=1)
    detected = image_to_string(image, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789').replace('\n', '')
    if detected != '':
        return detected[0]
    return ''


def detect(image: np.ndarray, offset: int = 2) -> list[str, int, bool, bool, bool, bool]:
    output = ['', 0, False, False, False, False]
    regions = label(image, connectivity=1)
    image_height, image_width = image.shape
    for region in sorted(regionprops(regions), key=lambda x: -x.area):
        ymin, xmin, ymax, xmax = region.bbox
        width, height = xmax - xmin, ymax - ymin
        area = region.area
        xmin_, ymin_, xmax_, ymax_ = max(0, xmin - offset), max(0, ymin - offset), min(image_width, xmax + offset), min(image_height, ymax + offset)
        print(width, height, xmin, ymin, xmax, ymax, area, image_width, image_height)
        if width > 0.9 * image_width or height > 0.9 * image_height:
            continue
        elif xmax > image_width // 2 and xmin < image_width // 2 and ymax > image_height // 2 and ymin < image_height // 2 and area > 700 and height / width > 1.5:
            xmin_, ymin_, xmax_, ymax_ = max(0, xmin_ - offset), max(0, ymin_ - offset), min(image_width, xmax_ + offset), min(image_height, ymax_ + offset)
            output[0] = detect_number(1 - image)#[ymin_:ymax_, xmin_:xmax_])
            print('center digit')
        elif xmin < image_width // 2 and ymin < image_height // 2 and area > 500 and height / width > 1.5:
            result = detect_number(1 - image)# [ymin_:ymax_, xmin_:xmax_])
            if result != '':
                output[1] *= 10
                output[1] += int(result)
            print('sum digit')
        elif area < 500 and xmax < image_width / 4 and width / height > 2:
            output[4] = True
        elif area < 500 and xmin > image_width * 3 / 4 and width / height > 2:
            output[5] = True
        elif area < 500 and ymax < image_height / 4 and height / width > 2:
            output[2] = True
        elif area < 500 and ymin > image_height * 3 / 4 and height / width > 2:
            output[3] = True
    print(output)
    return output
    

def sudoku_image_to_array(context: dict) -> list[list[int]]:
    screen = context['screen']
    screen = np.asarray(screen)
    screen = resize(screen, (4096, 4096))
    screen = rgb2gray(screen)
    thresholds = threshold_multiotsu(screen)
    screen = np.digitize(screen, bins=thresholds)
    screen = (screen == 0).astype(int)
    plt.imshow(screen, cmap='gray')
    plt.show()

    Xs = np.linspace(0, 4096, config.SUDOKU_SIZE + 1, dtype=int)
    Ys = np.linspace(0, 4096, config.SUDOKU_SIZE + 1, dtype=int)
    grid = [['' for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    sum = [[0 for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    top_border = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    bottom_border = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    left_border = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    right_border = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    offset = 5
    for i in range(config.SUDOKU_SIZE):
        for j in range(config.SUDOKU_SIZE):
            xmin, ymin, xmax, ymax = max(0, Xs[i] - offset), max(0, Ys[j] - offset), min(4096, Xs[i + 1] + offset), min(4096, Ys[j + 1] + offset)
            crop = screen[ymin:ymax, xmin:xmax]
            grid[i][j], sum[i][j], top_border[i][j], bottom_border[i][j], left_border[i][j], right_border[i][j] = detect(crop)
            
    return grid, sum, top_border, bottom_border, left_border, right_border


def scan(context: dict) -> None:
    """"""
    # obtain screenshot of sudoku board
    context['screen'] = scan_sudoku_board(context)
    
    # obtain coordinates for all the boxes within the sudoku game
    context['box centers'] = calculate_box_centers(context)

    # obtain array representation of sudoku board
    context['data'] = sudoku_image_to_array(context)
    
    
