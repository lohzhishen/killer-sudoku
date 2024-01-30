import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import numpy as np
import functools
import pyautogui
import skimage
import pathlib
import config
import pynput
import time
import PIL


# ========== Screenshotting functionality ==========
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
    

def get_screenshot(context: dict) -> PIL.Image:
    """Returns a screenshot of area selected by the user."""
    # obtain region selected by user
    on_click_contextualised = functools.partial(on_click, context)
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


def scan_sudoku_board(context: dict) -> PIL.Image:
    # instruct the user on how to select region
    pyautogui.alert(text='Click and drag to outline the sudoku board.', title=context['title'], button='OK')
    time.sleep(1)
    screen = get_screenshot(context)
    area = context['width'] * context['height']

    # region selected is too small
    while area < 200_000:
        pyautogui.alert(text='Area selected is too small. Maximise the window and try again.', 
              title=context['title'], button='OK')
        screen = get_screenshot(context)
        area = context['width'] * context['height']

    # record screen    
    return screen


# ========== Box locations ==========
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
    Xs = np.linspace(left_, right_, config.SUDOKU_SIZE, endpoint=True)
    Ys = np.linspace(top_, bottom_, config.SUDOKU_SIZE, endpoint=True)
    return [[[Xs[i], Ys[j]] for i in range(config.SUDOKU_SIZE)] for j in range(config.SUDOKU_SIZE)]


# ========== Converting image to arrays ==========
def detect_digit(image: np.ndarray) -> int:
    model = keras.models.load_model(pathlib.Path('Models', 'digit_recognizer.keras'))
    image = tf.data.Dataset.from_tensor_slices([image])
    def transform(x):
        x = tf.reshape(x, [1, 28, 28, 1])
        x = tf.cast(x, tf.float32) / 255
        x = tf.image.resize(x, [28,28])
        return x
    image = image.map(transform)
    return model.predict(image).argmax(axis=1)


def detect_borders(image: np.ndarray) -> tuple[bool, bool, bool, bool]:
    """TODO: Implement wall recognizer model"""
    return True, True, True, True


def detect(image: np.ndarray, offset: int = 2) -> tuple[str, int, bool, bool, bool, bool]:
    output = ['', 0, False, False, False, False]

    # detect borders
    box = preprocess_box_region(image)
    output[2], output[3], output[4], output[5] = detect_borders(box)

    # get regions of interest
    image_height, image_width = image.shape
    zones = skimage.measure.label(image, connectivity=1)
    regions = skimage.measure.regionprops(zones)

    # process roi from left to right, top to bottom
    regions.sort(key=lambda x: (x.bbox[1], x.bbox[0])) 

    # extract digits
    for region in regions:
        ymin, xmin, ymax, xmax = region.bbox
        width, height = xmax - xmin, ymax - ymin
        area = region.area
         
        if width > 0.9 * image_width or height > 0.9 * image_height:
            # area too big
            continue
        elif xmax > image_width // 2 and xmin < image_width // 2 and ymax > image_height // 2 and ymin < image_height // 2 and area > 100 and height / width > 1.5:
            # detect center digits
            box = preprocess_digit_region(zones, region)
            output[0] = detect_digit(box)
        elif xmin < image_width // 2 and ymin < image_height // 2 and area > 50 and height / width > 1.5:
            # detect sum digits
            box = preprocess_digit_region(zones, region)
            output[1] *= 10
            output[1] += detect_digit(box)
    return output


def preprocess_board(screen: np.ndarray) -> np.ndarray:
    screen = np.asarray(screen)

    # convert to grayscale
    gray = skimage.color.rgb2gray(screen)

    # apply thresholding
    thresholds = skimage.filters.threshold_multiotsu(gray)
    regions = np.digitize(gray, bins=thresholds)
    regions = (regions == 0).astype(int) * 255
    return regions


def process_board(screen: np.ndarray) -> tuple[list]:
    regions = preprocess_board(screen)
    height, width = regions.shape

    board = [['' for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    sums = [[0 for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    top = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    bottom = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    left = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]
    right = [[False for _ in range(config.SUDOKU_SIZE)] for _ in range(config.SUDOKU_SIZE)]

    Xs = np.linspace(0, width, config.SUDOKU_SIZE + 1, dtype=int)
    Ys = np.linspace(0, height, config.SUDOKU_SIZE + 1, dtype=int)
    offset = 5
    for i in range(config.SUDOKU_SIZE):
        for j in range(config.SUDOKU_SIZE):
            xmin, ymin, xmax, ymax = max(0, Xs[i] - offset), max(0, Ys[j] - offset), min(width, Xs[i + 1] + offset), min(height, Ys[j + 1] + offset)
            crop = regions[ymin:ymax, xmin:xmax]
            board[i][j], sums[i][j], top[i][j], bottom[i][j], left[i][j], right[i][j] = detect(crop)
    return (board, sums, top, bottom, left, right)


def preprocess_digit_region(zones: np.ndarray, region: np.ndarray, offset: int = 2) -> np.ndarray:
    image = zones.copy()
    h, w = image.shape

    # remove all other regions
    image[zones != region.label] = 0 
    image[zones == region.label] = 255

    # crop region around digit
    ymin, xmin, ymax, xmax = region.bbox
    ymin, xmin, ymax, xmax = max(0, ymin - offset), max(0, xmin - offset), min(h, ymax + offset), min(w, xmax + offset)
    image = image[ymin:ymax, xmin:xmax]

    # rescale the image
    target_width, target_height = 28, 28
    h, w = image.shape
    if h <= w:
        output_shape = (np.floor(h * target_width / w), target_width)
    else:
        output_shape = (target_height, np.floor(w * target_height / h))
    image = skimage.transform.resize(image, output_shape, preserve_range=True)

    # pad the image
    h, w = image.shape
    pad_horizontal = target_width - w 
    pad_vertical = target_height - h
    pad_left = pad_horizontal // 2
    pad_right = pad_horizontal - pad_left
    pad_top = pad_vertical // 2
    pad_bottom = pad_vertical - pad_top
    image = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)))
    return image


def preprocess_box_region(image: np.ndarray) -> np.ndarray:
    image = image.copy()
    
    # resize image
    output_shape = (28, 28)
    image = skimage.transform.resize(image, output_shape, preserve_range=True)
    image[image < 1] = 0

    return image 


# ========== overall function ==========
def scan(context: dict) -> None:
    # obtain screenshot of sudoku board
    context['screen'] = scan_sudoku_board(context)
    
    # obtain coordinates for all the boxes within the sudoku game
    context['box centers'] = calculate_box_centers(context)

    # obtain array representation of sudoku board
    context['data'] = process_board(context['screen'])
    
    
