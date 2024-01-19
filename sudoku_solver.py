import config

def sudoku_solver(board: list[list[str]]) -> list[list[list[str]]]:
    if not validate_board(board) or not iteration(board, 0, sudoku_validate):
        return None
    return board


def iteration(board: list[list[str]], pos: int, validation: 'function', **kwargs: dict) -> bool:
    pos = find_next_empty(board, pos)
    if pos == -1:
        return True
    r, c = pos // config.SUDOKU_SIZE, pos % config.SUDOKU_SIZE
    for action in [x for x in config.ACTIONS if x not in board[r]]:
        board[r][c] = action
        if not validation(board, r, c, **kwargs) or not iteration(board, pos, validation, **kwargs):
            continue
        return True
    board[r][c] = ''
    return False


def find_next_empty(board: list[list[str]], pos: int) -> int:
    while 0 <= pos < config.SUDOKU_SIZE ** 2 and board[pos // config.SUDOKU_SIZE][pos % config.SUDOKU_SIZE] != '':
        pos += 1
    return -1 if pos >= config.SUDOKU_SIZE ** 2 or pos < 0 else pos


def sudoku_validate(board: list[list[str]], r: int, c: int, **kwargs: dict) -> bool:
    return validate_box(board, r, c) and validate_col(board, r, c)


def validate_box(board: list[list[str]], i: int, j: int) -> bool:
    if i < 0 or i >= config.SUDOKU_SIZE or j < 0 or j >= config.SUDOKU_SIZE:
        return False
    r, c = i // config.SUDOKU_BOX_SIZE, j // config.SUDOKU_BOX_SIZE
    for dr in range(config.SUDOKU_BOX_SIZE):
        for dc in range(config.SUDOKU_BOX_SIZE):
            r_, c_ = config.SUDOKU_BOX_SIZE * r + dr, config.SUDOKU_BOX_SIZE * c + dc
            if (r_ != i or c_ != j) and board[r_][c_] == board[i][j]:
                return False
    return True


def validate_col(board: list[list[str]], i: int, j: int) -> bool:
    if i < 0 or i >= config.SUDOKU_SIZE or j < 0 or j >= config.SUDOKU_SIZE:
        return False 
    for r in range(config.SUDOKU_SIZE):
        if r != i and board[r][j] == board[i][j]:
            return False
    return True
   
def validate_board(board: list[list[str]]) -> bool:
    for r in range(config.SUDOKU_SIZE):
        row = [x for x in board[r] if x != '']
        if len(set(row)) != len(row):
            return False
    for c in range(config.SUDOKU_SIZE):
        col = [board[i][c] for i in range(config.SUDOKU_SIZE) if board[i][c] != '']
        if len(set(col)) != len(col):
            return False
    for r in range(config.SUDOKU_SIZE // config.SUDOKU_BOX_SIZE):
        for c in range(config.SUDOKU_SIZE // config.SUDOKU_BOX_SIZE):
            box = [board[config.SUDOKU_BOX_SIZE * r + dr][config.SUDOKU_BOX_SIZE * c + dc] for dr in range(config.SUDOKU_BOX_SIZE) for dc in range(config.SUDOKU_BOX_SIZE) if board[config.SUDOKU_BOX_SIZE * r + dr][config.SUDOKU_BOX_SIZE * c + dc] != '']
            if len(set(box)) != len(box):
                return False
    return True

