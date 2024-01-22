from Interaction.cv import scan_sudoku_board, calculate_box_centers
from PIL import Image
from numpy import pad
from pathlib import Path
from os import listdir
import config
output = Path('Dataset', 'Raw')

def get_box_roi(context: dict, i: int, j: int) -> Image:
    if 'padded_screen' not in context:
        image = context['screen']
        padding = ((context['box height'] // 2, context['box height'] // 2), (context['box width'] // 2, context['box width'] // 2), (0, 0))
        image = pad(image, padding, constant_values=255)
        context['padded_screen'] = Image.fromarray(image, 'RGB')
    image = context['padded_screen']
    anchor_x, anchor_y = context['top left']
    x, y = context['box centers'][i][j]
    top = y - context['box height'] // 1.5 - anchor_y + context['box height'] // 2
    bottom = y + context['box height'] // 1.5 - anchor_y + context['box height'] // 2
    left = x - context['box width'] // 1.5 - anchor_x + context['box width'] // 2
    right = x + context['box width'] // 1.5 - anchor_x + context['box width'] // 2
    return context['padded_screen'].crop(box=(left, top, right, bottom))


def make_dataset():
    context = {"title": 'Dataset Maker'}
    context['screen'] = scan_sudoku_board(context)
    context['box centers'] = calculate_box_centers(context)
    dataset_size = len(listdir(output))
    for i in range(config.SUDOKU_SIZE):
        for j in range(config.SUDOKU_SIZE):
            print(f'[INFO] Processing box ({i}, {j})')
            crop = get_box_roi(context, i, j)
            crop.save(output / "{:>05}.png".format(dataset_size + i * config.SUDOKU_SIZE + j))


if __name__ == "__main__":
    make_dataset()