import sudoku

def sudoku_solver(board: list[list[str]]) -> list[list[list[str]]]:
    if not iteration(board, 0, sudoku_validate):
        return None
    return board


def iteration(board: list[list[str]], pos: int, validation: function, **kwargs: dict) -> bool:
    pos = find_next_empty(board, pos)
    if pos == -1:
        return True
    r, c = pos // sudoku.SUDOKU_SIZE, pos % sudoku.SUDOKU_SIZE
    for action in [x for x in sudoku.ACTIONS if x not in board[r]]:
        board[r][c] = action
        if not validation(board, r, c, **kwargs) or not iteration(board, pos, validation, **kwargs):
            continue
        return True
    board[r][c] = ''
    return False


def find_next_empty(board: list[list[str]], pos: int) -> int:
    while pos < sudoku.SUDOKU_SIZE ** 2 and board[pos // sudoku.SUDOKU_SIZE][pos % sudoku.SUDOKU_SIZE] != '':
        pos += 1
    return -1 if pos >= sudoku.SUDOKU_SIZE ** 2 else pos


def sudoku_validate(board: list[list[str]], r: int, c: int, **kwargs: dict) -> bool:
    return validate_box(board, r, c) and validate_col(board, r, c)


def validate_box(board: list[list[str]], i: int, j: int) -> bool:
    r, c = i // sudoku.SUDOKU_BOX_SIZE, j // sudoku.SUDOKU_BOX_SIZE
    for dr in range(sudoku.SUDOKU_BOX_SIZE):
        for dc in range(sudoku.SUDOKU_BOX_SIZE):
            r_, c_ = sudoku.SUDOKU_BOX_SIZE * r + dr, sudoku.SUDOKU_BOX_SIZE * c + dc
            if (r_ != i or c_ != j) and board[r_][c_] == board[i][j]:
                return False
    return True


def validate_col(board: list[list[str]], i: int, j: int) -> bool:
    for r in range(sudoku.SUDOKU_SIZE):
        if r != i and board[r][j] == board[i][j]:
            return False
    return True
   