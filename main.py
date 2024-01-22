import Interaction.cv as cv
from Solver.sudoku_solver import sudoku_solver
from Interaction.controller import implement_solution
import matplotlib.pyplot as plt
from numpy import asarray

def view_digit_roi(context, i=1, j=0):
    plt.imshow(cv.get_digit_roi(context, i, j))
    plt.xticks([])
    plt.yticks([])

def view_sum_roi(context, i=1, j=0):
    plt.imshow(cv.get_sum_roi(context, i, j))
    plt.xticks([])
    plt.yticks([])

def view_grid(context):
    plt.imshow(context['screen'])

def view_grid_centers(context):
    grid_centers = context['box centers']
    centers = []
    for row in grid_centers:
        centers.extend(row)
    centers = asarray(centers)
    centers[:, 0] -= context['top left'][0]
    centers[:, 1] -= context['top left'][1]
    plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='o')


if __name__ == '__main__':
    context = {'title': 'Killer Sudoku Solver'}
    # cv.scan(context)
    # print(context['board'])
    # solution = sudoku_solver(context['board'])
    # print(solution)
    # implement_solution(context, solution)
    exit()
