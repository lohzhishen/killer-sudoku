from interaction import Controller, Screenshot
from detection import Detection
from solver import KillerSudokuSolver
from Editor import editor


def scan(context: dict) -> None:
    # obtain screenshot of sudoku board
    context['screen'] = Screenshot.scan_sudoku_board(context)
    
    # obtain coordinates for all the boxes within the sudoku game
    context['box centers'] = Controller.calculate_box_centers(context)

    # obtain array representation of sudoku board
    context['data'] = Detection.process_board(context['screen'])

if __name__ == '__main__':
    context = {'title': 'Killer Sudoku Solver'}
    scan(context)
    app = editor.KillerSudokuEditor(*context['data'])
    solution = KillerSudokuSolver.solve(*context['data'])
    Controller.implement_solution(context, solution)
    exit()
