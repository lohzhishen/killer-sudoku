"""Usage: python -m pytest"""

import pytest
from .sudoku_solver import *

board = [['1', '', '6', '4', '3', '', '', '5', ''],
         ['', '', '5', '', '', '', '9', '', ''],
         ['', '', '', '', '2', '', '', '', ''],
         ['', '', '', '', '', '6', '', '', ''],
         ['', '8', '', '', '', '', '', '', '7'],
         ['3', '', '', '1', '5', '', '', '9', ''],
         ['', '3', '', '6', '4', '', '8', '', ''],
         ['', '', '', '', '', '2', '', '4', ''],
         ['6', '', '', '', '', '9', '', '', '']]

solution = [['1', '9', '6', '4', '3', '8', '7', '5', '2'],
           ['4', '2', '5', '7', '6', '1', '9', '8', '3'],
           ['8', '7', '3', '9', '2', '5', '4', '1', '6'],
           ['2', '1', '9', '8', '7', '6', '5', '3', '4'],
           ['5', '8', '4', '2', '9', '3', '1', '6', '7'],
           ['3', '6', '7', '1', '5', '4', '2', '9', '8'],
           ['9', '3', '1', '6', '4', '7', '8', '2', '5'],
           ['7', '5', '8', '3', '1', '2', '6', '4', '9'],
           ['6', '4', '2', '5', '8', '9', '3', '7', '1']]

# ========== find_next_empty() ==========
def test_find_next_empty_1():
    """Test description: empty spot on current row"""
    assert find_next_empty(board, 0) == 1

def test_find_next_empty_2():
    """Test description: currently on empty spot"""
    assert find_next_empty(board, 1) == 1

def test_find_next_empty_3():
    """Test description: empty spot on current row"""
    assert find_next_empty(board, 44) == 46
    
def test_find_next_empty_4():
    """Test description: no empty spot"""
    assert find_next_empty(solution, 80) == -1

def test_find_next_empty_5():
    """Test description: out of board"""
    assert find_next_empty(solution, 81) == -1

def test_find_next_empty_6():
    """Test description: negative position"""
    assert find_next_empty(board, -1) == -2

def test_find_next_empty_7():
    """Test description: out of board"""
    assert find_next_empty(board, 82) == -2

# ========== validate_box() ==========
def test_validate_box_1():
    """Test description: valid position"""
    assert validate_box(board, 0, 0) == True

def test_validate_box_2():
    """Test description: valid position"""
    assert validate_box(board, 0, 3) == True

def test_validate_box_3():
    """Test description: valid position"""
    assert validate_box(board, 0, 7) == True

def test_validate_box_4():
    """Test description: valid position"""
    assert validate_box(board, 4, 1) == True

def test_validate_box_5():
    """Test description: valid position"""
    assert validate_box(board, 3, 5) == True

def test_validate_box_6():
    """Test description: valid position"""
    assert validate_box(board, 4, 8) == True

def test_validate_box_7():
    """Test description: valid position"""
    assert validate_box(board, 8, 0) == True

def test_validate_box_8():
    """Test description: valid position"""
    assert validate_box(board, 8, 5) == True

def test_validate_box_9():
    """Test description: valid position"""
    assert validate_box(board, 6, 6) == True

def test_validate_box_10():
    """Test description: invalid position"""
    board[2][2] = board[0][0]
    assert validate_box(board, 0, 0) == False
    board[2][2] = ''

def test_validate_box_11():
    """Test description: invalid position"""
    board[2][5] = board[0][3]
    assert validate_box(board, 0, 3) == False
    board[2][5] = ''

def test_validate_box_12():
    """Test description: invalid position"""
    board[2][8] = board[0][7]
    assert validate_box(board, 0, 7) == False
    board[2][8] = ''

def test_validate_box_13():
    """Test description: invalid position"""
    board[5][2] = board[4][1]
    assert validate_box(board, 4, 1) == False
    board[5][2] = ''

def test_validate_box_14():
    """Test description: invalid position"""
    board[5][5] = board[3][5]
    assert validate_box(board, 3, 5) == False
    board[5][5] = ''

def test_validate_box_15():
    """Test description: invalid position"""
    board[5][8] = board[4][8]
    assert validate_box(board, 4, 8) == False
    board[5][8] = ''

def test_validate_box_16():
    """Test description: invalid position"""
    board[8][2] = board[8][0]
    assert validate_box(board, 8, 0) == False
    board[8][2] = ''

def test_validate_box_17():
    """Test description: invalid position"""
    board[8][4] = board[8][5]
    assert validate_box(board, 8, 5) == False
    board[8][4] = ''

def test_validate_box_18():
    """Test description: invalid position"""
    board[8][8] = board[6][6]
    assert validate_box(board, 6, 6) == False
    board[8][8] = ''

def test_validate_box_19():
    """Test description: invalid index"""
    assert validate_box(board, 0, -1) == False

def test_validate_box_20():
    """Test description: invalid index"""
    assert validate_box(board, -1, 0) == False

def test_validate_box_21():
    """Test description: invalid index"""
    assert validate_box(board, 0, 9) == False

def test_validate_box_22():
    """Test description: invalid index"""
    assert validate_box(board, 9, 0) == False

# ========== validate_col() ==========
def test_validate_col_1():
    """Test description: valid position"""
    assert validate_col(board, 0, 0) == True

def test_validate_col_2():
    """Test description: invalid position"""
    board[7][0] = board[0][0]
    assert validate_col(board, 0, 0) == False
    board[7][0] = ''

def test_validate_col_3():
    """Test description: invalid index"""
    board[7][0] = board[0][0]
    assert validate_col(board, 0, 0) == False
    board[7][0] = ''

def test_validate_col_4():
    """Test description: invalid position"""
    assert validate_col(board, -1, 0) == False

def test_validate_col_5():
    """Test description: invalid position"""
    assert validate_col(board, 0, -1) == False

def test_validate_col_6():
    """Test description: invalid position"""
    assert validate_col(board, 9, 0) == False

def test_validate_col_7():
    """Test description: invalid position"""
    assert validate_col(board, 0, 9) == False

# ========== validate_board() ==========
def test_validate_board_1():
    """Test description: valid board"""
    assert validate_sudoku_board(board) == True

def test_validate_board_2():
    """Test description: invalid last row"""
    board[8][8] = board[8][0]
    assert validate_sudoku_board(board) == False
    board[8][8] = ''

def test_validate_board_2():
    """Test description: invalid last colum"""
    board[8][8] = board[4][8]
    assert validate_sudoku_board(board) == False
    board[8][8] = ''

def test_validate_board_2():
    """Test description: invalid last box"""
    board[8][8] = board[7][7]
    assert validate_sudoku_board(board) == False
    board[8][8] = ''

# ========== sudoku_solver() ==========
def test_sudoku_solver_1():
    """Test description: valid board with solution"""
    assert sudoku_solver(board) == solution

def test_sudoku_solver_2():
    """Test description: invalid board without solution"""
    board[0][1] = board[0][0]
    assert sudoku_solver(board) == None
    board[0][1] = ''