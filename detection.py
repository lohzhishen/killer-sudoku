"""This module handles all AI detection techniques."""

import numpy as np
from tensorflow import keras
import tensorflow as tf
import pathlib
import skimage


from config import *


class Detection:
    digit_recognizer = keras.models.load_model(pathlib.Path('Models', 'digit_recognizer.keras'))
    wall_reocognizer = keras.models.load_model(pathlib.Path('Models', 'wall_recognizer.keras'))

    @staticmethod
    def format_image(image: np.ndarray) -> tf.data.Dataset:
        image = tf.data.Dataset.from_tensor_slices([image])
        def transform(x):
            x = tf.reshape(x, [1, 28, 28, 1])
            x = tf.cast(x, tf.float32) / 255
            x = tf.image.resize(x, [28,28])
            return x
        image = image.map(transform)
        return image

    @staticmethod
    def detect_digit(image: np.ndarray) -> int:
        image = Detection.format_image(image)
        return Detection.digit_recognizer.predict(image).argmax(axis=1)[0]

    @staticmethod
    def detect_borders(image: np.ndarray) -> tuple[bool, bool, bool, bool]:
        image = Detection.format_image(image)
        return tuple((Detection.wall_recognizer.predict(image) < 0.5)[0])

    @staticmethod
    def detect(image: np.ndarray) -> tuple[str, int, bool, bool, bool, bool]:
        output = ['', 0, False, False, False, False]

        # detect borders
        box = Detection.preprocess_box_region(image)
        output[2], output[3], output[4], output[5] = Detection.detect_borders(box)

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
            num_pixels = region.num_pixels
            
            if width > 0.9 * image_width or height > 0.9 * image_height:
                # area too big
                continue
            elif xmax >= image_width / 2 and xmin <= image_width / 2 and ymax >= image_height // 2 and ymin <= image_height // 2 and area >= 13 and height / width >= 1:
                # detect center digits
                box = Detection.preprocess_digit_region(zones, region)
                output[0] = str(Detection.detect_digit(box))
            elif xmin < image_width / 2 and ymax < image_height / 2 and height > 2 and area >= 10 and 3 >= height / width >= 1 and num_pixels != width * height:
                # detect sum digits
                box = Detection.preprocess_digit_region(zones, region)
                output[1] *= 10
                output[1] += Detection.detect_digit(box)
        return output

    @staticmethod
    def preprocess_board(screen: np.ndarray) -> np.ndarray:
        screen = np.asarray(screen)

        # convert to grayscale
        gray = skimage.color.rgb2gray(screen)

        # apply thresholding
        thresholds = skimage.filters.threshold_multiotsu(gray)
        regions = np.digitize(gray, bins=thresholds)
        regions = (regions == 0).astype(int) * 255
        return regions

    @staticmethod
    def process_board(screen: np.ndarray) -> tuple[list]:
        regions = Detection.preprocess_board(screen)
        height, width = regions.shape

        board = [['' for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        sums = [[0 for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        top = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        bottom = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        left = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        right = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]

        Xs = np.linspace(0, width, SUDOKU_SIZE + 1, dtype=int)
        Ys = np.linspace(0, height, SUDOKU_SIZE + 1, dtype=int)
        offset = 5
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                xmin, ymin, xmax, ymax = max(0, Xs[i] - offset), max(0, Ys[j] - offset), min(width, Xs[i + 1] + offset), min(height, Ys[j + 1] + offset)
                crop = regions[ymin:ymax, xmin:xmax]
                board[i][j], sums[i][j], top[i][j], bottom[i][j], left[i][j], right[i][j] = Detection.detect(crop)
        return (board, sums, top, bottom, left, right)


    @staticmethod
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

    @staticmethod
    def preprocess_box_region(image: np.ndarray) -> np.ndarray:
        image = image.copy()
        
        # resize image
        output_shape = (28, 28)
        image = skimage.transform.resize(image, output_shape, preserve_range=True)
        image[image < 1] = 0

        return image 

