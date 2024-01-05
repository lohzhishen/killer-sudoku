import sudoku

def sudoku_solver(board: list[list[str]]) -> list[list[list[str]]]:
    actions = {i: set(sudoku.ACTIONS) for i in range(sudoku.SUDOKU_SIZE)}
    for i in range(sudoku.SUDOKU_SIZE):
        for j in range(sudoku.SUDOKU_SIZE):
            if board[i][j] != '':
                actions[i].pop(board[i][j])
    if not iteration(board, 0, actions):
        return None
    return board


def iteration(board: list[list[str]], pos: int, actions) -> bool:
    pos = find_next_empty(board, pos)
    if pos == -1:
        return True
    r, c = pos // sudoku.SUDOKU_SIZE, pos % sudoku.SUDOKU_SIZE
    for action in actions[r]:
        board[r][c] = action
        if not validate_box(board, r, c) or not validate_col(board, r, c) or not validate_row(board, r, c) or not iteration(board, pos, actions):
            board[r][c] = ''
            continue
        return True
    return False


def find_next_empty(board: list[list[str]], pos: int) -> int:
    while pos < sudoku.SUDOKU_SIZE ** 2 and board[pos // sudoku.SUDOKU_SIZE][pos % sudoku.SUDOKU_SIZE] != '':
        pos += 1
    return -1 if pos >= sudoku.SUDOKU_SIZE ** 2 else pos


def validate_box(board: list[list[str]], i: int, j: int) -> bool:
    r, c = i // sudoku.SUDOKU_BOX_SIZE, j // sudoku.SUDOKU_BOX_SIZE
    for dr in range(sudoku.SUDOKU_BOX_SIZE):
        for dc in range(sudoku.SUDOKU_BOX_SIZE):
            r_, c_ = r + dr, c + dc
            if (r_ != i or c_ != j) and board[r_][c_] == board[i][j]:
                return False
    return True


def validate_col(board: list[list[str]], i: int, j: int) -> bool:
    for r in range(sudoku.SUDOKU_SIZE):
        if r != i and board[r][j] == board[i][j]:
            return False
    return True


def validate_row(board: list[list[str]], i: int, j: int) -> bool:
    for c in range(sudoku.SUDOKU_SIZE):
        if c != j and board[i][c] == board[i][j]:
            return False
    return True