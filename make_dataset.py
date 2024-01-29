from Interaction import cv
import numpy as np
import pathlib
import skimage
import config
import PIL
import os


# output directories 
BOX_OUTPUT = pathlib.Path('Models', 'Dataset', 'Wall Recognizer', 'Raw')
DIGIT_OUTPUT = pathlib.Path('Models', 'Dataset', 'Digit Recognizer', 'Raw')
LABELLED_BOX_OUTPUT = pathlib.Path('Models', 'Dataset', 'Wall Recognizer', 'Labelled')

# ========== processing functions ============
def process_board(screen: np.ndarray) -> list[list[int]]:
    regions = cv.preprocess_board(screen)
    height, width = regions.shape

    Xs = np.linspace(0, width, config.SUDOKU_SIZE + 1, dtype=int)
    Ys = np.linspace(0, height, config.SUDOKU_SIZE + 1, dtype=int)
    offset = 5
    for j in range(config.SUDOKU_SIZE):
        for i in range(config.SUDOKU_SIZE):
            xmin, ymin, xmax, ymax = max(0, Xs[i] - offset), max(0, Ys[j] - offset), min(width, Xs[i + 1] + offset), min(height, Ys[j + 1] + offset)
            crop = regions[ymin:ymax, xmin:xmax]
            process_box(crop)


def process_box(image: np.ndarray) -> None:
    # save the image
    save_box_image(cv.preprocess_box_region(image))

    # extract out digits
    image_height, image_width = image.shape
    zones = skimage.measure.label(image, connectivity=2)
    regions = skimage.measure.regionprops(zones)
    regions.sort(key=lambda x: -x.area)
    for region in regions:
        #plt.imshow(image[region.slice])
        #plt.colorbar()
        #plt.show()
        ymin, xmin, ymax, xmax = region.bbox
        width, height = xmax - xmin, ymax - ymin
        area = region.area
        num_pixels = region.num_pixels
        if width > 0.9 * image_width or height > 0.9 * image_height:
            continue
        elif xmax >= image_width / 2 and xmin <= image_width / 2 and ymax >= image_height // 2 and ymin <= image_height // 2 and area >= 13 and height / width >= 1:
            # center digits
            save_digit_image(cv.preprocess_digit_region(zones, region))
        elif xmin < image_width / 2 and ymax < image_height / 2 and height > 2 and area >= 10 and 3 >= height / width >= 1 and num_pixels != width * height:
            # sum digits
            save_digit_image(cv.preprocess_digit_region(zones, region))


# ========== saving images ==========
def save_digit_image(image: np.ndarray) -> None:
    # save the image
    image = PIL.Image.fromarray(image.astype(np.uint8))
    file_name = f"{len(os.listdir(DIGIT_OUTPUT)):>05}.png"
    # image.save(DIGIT_OUTPUT / file_name)


def save_box_image(image: np.ndarray) -> None:
    # save the image
    image = PIL.Image.fromarray(image.astype(np.uint8))
    no = len(os.listdir(BOX_OUTPUT)) + len(os.listdir(LABELLED_BOX_OUTPUT))
    file_name = f"{no:>05}.png"
    image.save(BOX_OUTPUT / file_name)


# ========== main ==========
def main():
    context = {"title": 'Dataset Maker'}
    context['screen'] = cv.scan_sudoku_board(context)
    process_board(context['screen'])


if __name__ == "__main__":
    main()
