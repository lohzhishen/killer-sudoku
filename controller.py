from pyautogui import click, write
import sudoku


def act(context: dict, i: int, j: int, digit: str) -> None:
    """Keys in the specified digit at the given box in the sudoku game."""
    click(*context['box centers'][i][j])
    write(digit)


def implement_solution(context: dict, solution: list[list[str]]) -> None:
    """Takes control over the mouse and keyboard to enter the solution into the sudoku board."""
    for i in range(sudoku.SUDOKU_SIZE):
        for j in range(sudoku.SUDOKU_SIZE):
            digit = solution[i][j]
            act(context, i, j, digit)
    