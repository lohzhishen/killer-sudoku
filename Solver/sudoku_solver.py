from typing import Callable
from config import *


def sudoku_solver(board: list[list[str]]) -> list[list[list[str]]] | None:
    """Solves a sudoku game.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.

    Returns
    -------
    board: list[list[str]]
        A 2D array containing the values placed onto the board. It has no empty spots.
    If None is returned, the game parameters are invalid or it has no solution.
    """
    if not validate_sudoku_board(board):
        # invalid board arragement
        return None
    
    # solve the game
    if not iteration(board, 0, sudoku_validate):
        return None
    return board


def iteration(board: list[list[str]], pos: int, validation: Callable, **kwargs: dict) -> bool:
    """Recursively try values to find the solution to the game.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.
    pos: int
        The location to begin the search. If the position is (r, c), pos = r * SUDOKU_SIZE + c
        So, r = pos // SUDOKU_SIZE and c = pos % SUDOKU_SIZE
    validation: Callable
        A callable function to validate if the current move was legal.
    kwargs: dict
        A dictionary of keyword arguments to pass to the validation call.

    Returns
    -------
    success: bool
        Indicates if a solution has been found.
    """
    # find next empty position to fill in
    pos = find_next_empty(board, pos)
    if pos == -1:
        # no empty position found
        return True
    
    # try all possible values at the empty position
    r, c = pos // SUDOKU_SIZE, pos % SUDOKU_SIZE
    for action in [x for x in ACTIONS if x not in board[r]]:
        board[r][c] = action
        if (not validation(board, r, c, **kwargs) or # check if move is legal
            not iteration(board, pos, validation, **kwargs)):
            continue
        return True
    
    # reset the position to its initial state
    board[r][c] = ''
    return False


def find_next_empty(board: list[list[str]], pos: int) -> int:
    """Returns the position of the next empty spot on the board.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.
    pos: int
        The location to begin the search. If the position is (r, c), pos = r * SUDOKU_SIZE + c
        So, r = pos // SUDOKU_SIZE and c = pos % SUDOKU_SIZE
    
    Returns
    -------
    pos: int
        The position of the next empty spot on the board
    If pos == -1, it means that there is no empty spot.
    If pos == -2, it means that the input pos is invalid.
    """
    # check for invalid values
    if pos < 0 or pos > SUDOKU_SIZE ** 2:
        return -2
    
    # iterate until next position is found
    while pos < SUDOKU_SIZE ** 2 and board[pos // SUDOKU_SIZE][pos % SUDOKU_SIZE] != '':
        pos += 1
    return -1 if pos == SUDOKU_SIZE ** 2 or pos < 0 else pos


def sudoku_validate(board: list[list[str]], r: int, c: int, **kwargs: dict) -> bool:
    """Validates a move made in sudoku.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.
    r: int
        Row index where the new value was placed.  
    c: int
        Column index where the new value was placed.

    Returns
    -------
    validity: bool
        Indicates if the move was legal.
    """
    return validate_box(board, r, c) and validate_col(board, r, c)


def validate_box(board: list[list[str]], i: int, j: int) -> bool:
    """Validates if there are multiple identical values in a 3x3 box.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.
    i: int
        Row index where the new value was placed.  
    j: int
        Column index where the new value was placed.

    Returns
    -------
    validity: bool
        Indicates if there are multiple identical values in a 3x3 box.
    """
    # validate the i and j variables
    if i < 0 or i >= SUDOKU_SIZE or j < 0 or j >= SUDOKU_SIZE:
        return False

    # validate the 3x3 box
    r, c = i // SUDOKU_BOX_SIZE, j // SUDOKU_BOX_SIZE
    for dr in range(SUDOKU_BOX_SIZE):
        for dc in range(SUDOKU_BOX_SIZE):
            r_, c_ = SUDOKU_BOX_SIZE * r + dr, SUDOKU_BOX_SIZE * c + dc
            if (r_ != i or c_ != j) and board[r_][c_] == board[i][j]:
                return False
    return True


def validate_col(board: list[list[str]], i: int, j: int) -> bool:
    """Validates if there are multiple identical values in a column.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.
    i: int
        Row index where the new value was placed.  
    j: int
        Column index where the new value was placed.

    Returns
    -------
    validity: bool
        Indicates if there are multiple identical values in a column.
    """
    # validate the i and j variables
    if i < 0 or i >= SUDOKU_SIZE or j < 0 or j >= SUDOKU_SIZE:
        return False 

    # check the column
    for r in range(SUDOKU_SIZE):
        if r != i and board[r][j] == board[i][j]:
            return False
    return True
   
def validate_sudoku_board(board: list[list[str]]) -> bool:
    """Validates if the board arragement is valid.
    
    Parameters
    ----------
    board: list[list[str]]
        A 2D array containing the values placed onto the board.

    Returns
    -------
    validity: bool
        Indicates if board arragement is valid.
    """
    # validate the rows
    for r in range(SUDOKU_SIZE):
        row = [x for x in board[r] if x != '']
        if len(set(row)) != len(row):
            return False
    
    # validate the columns
    for c in range(SUDOKU_SIZE):
        col = [board[i][c] for i in range(SUDOKU_SIZE) if board[i][c] != '']
        if len(set(col)) != len(col):
            return False
        
    # validate each 3x3 box
    for r in range(SUDOKU_SIZE // SUDOKU_BOX_SIZE):
        for c in range(SUDOKU_SIZE // SUDOKU_BOX_SIZE):
            i, j = SUDOKU_BOX_SIZE * r, SUDOKU_BOX_SIZE * c
            # obtain all placed values
            box = [board[i + dr][j + dc] 
                   for dr in range(SUDOKU_BOX_SIZE) for dc in range(SUDOKU_BOX_SIZE) 
                   if board[i + dr][j + dc] != '']
            
            # verify uniqueness
            if len(set(box)) != len(box):
                return False
    return True

