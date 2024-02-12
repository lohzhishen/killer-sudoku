"""This module handles all AI detection techniques."""

import numpy as np
import skimage
import prediction


from config import *


class Detection:
    @staticmethod
    def detect(image: np.ndarray) -> tuple[str, int, bool, bool, bool, bool]:
        """Returns the inferences for this box - digit, sum, top border, bottom border, left border, right border"""
        output = ['', 0, False, False, False, False]

        # detect borders
        box = Detection.preprocess_box_region(image)
        output[2], output[3], output[4], output[5] = prediction.Predictor.detect_borders(box)

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
                output[0] = str(prediction.Predictor.detect_digit(box))
            elif xmin < image_width / 2 and ymax < image_height / 2 and height > 2 and area >= 10 and 3 >= height / width >= 1 and num_pixels != width * height:
                # detect sum digits
                box = Detection.preprocess_digit_region(zones, region)
                output[1] *= 10
                output[1] += prediction.Predictor.detect_digit(box)
        return output

    @staticmethod
    def preprocess_board(screen: np.ndarray) -> np.ndarray:
        """Returns the image of the board after preprocessing."""
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
        """Overall function to extract data from the image."""
        regions = Detection.preprocess_board(screen)
        height, width = regions.shape

        board = [['' for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        sums = [[0 for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        top = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        bottom = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        left = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        right = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]

        Ys = np.linspace(0, width, SUDOKU_SIZE + 1, dtype=int)
        Xs = np.linspace(0, height, SUDOKU_SIZE + 1, dtype=int)
        offset = 5
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                xmin, ymin, xmax, ymax = max(0, Xs[i] - offset), max(0, Ys[j] - offset), min(height, Xs[i + 1] + offset), min(width, Ys[j + 1] + offset)
                crop = regions[xmin:xmax, ymin:ymax]
                board[i][j], sums[i][j], top[i][j], bottom[i][j], left[i][j], right[i][j] = Detection.detect(crop)
        return (board, sums, top, bottom, left, right)


    @staticmethod
    def preprocess_digit_region(zones: np.ndarray, region: np.ndarray, offset: int = 2) -> np.ndarray:
        """Preprocesses the digit image for inference."""
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
        """Preprocesses the box image for inference."""
        image = image.copy()
        
        # resize image
        output_shape = (28, 28)
        image = skimage.transform.resize(image, output_shape, preserve_range=True)
        image[image < 1] = 0

        return image 

