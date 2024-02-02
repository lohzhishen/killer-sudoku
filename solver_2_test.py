"""Usage: python -m pytest"""

import pytest
from solver import SudokuSolver, KillerSudokuSolver


board = [['','','','8','','','','',''],
         ['2','','','','','','','',''],
         ['','','','','','','8','',''],
         ['','','','9','','','','',''],
         ['','','','','','','','','8'],
         ['','7','','','','','','',''],
         ['','','6','','','8','','',''],
         ['','','','','','','','3',''],
         ['','','','','6','','','','']]

sums = [[10,10,9,15,3,26,12,12,1],
        [13,13,6,15,26,26,22,22,22],
        [7,13,6,18,26,26,19,22,8],
        [6,6,9,18,18,19,19,6,8],
        [22,22,9,8,12,12,6,6,13],
        [18,22,9,8,4,4,5,25,13],
        [18,8,8,10,10,18,5,25,25],
        [18,12,14,14,14,18,11,11,25],
        [12,12,18,18,18,18,11,17,17]]

top_border = [[True, True, True, True, True, True, True, True, True],
              [True, True, True, False, True, False, True, True, True],
              [True, False, False, True, False, False, True, False, True],
              [True, True, True, False, True, True, False, True, False],
              [True, True, False, True, True, True, True, False, True],
              [True, False, False, False, True, True, True, True, False],
              [False, True, True, True, True, True, False, False, True],
              [False, True, True, True, True, False, True, True, False],
              [True, False, True, True, True, False, False, True, True]]

bottom_border = [[True, True, True, False, True, False, True, True, True],
              [True, False, False, True, False, False, True, False, True],
              [True, True, True, False, True, True, False, True, False],
              [True, True, False, True, True, True, True, False, True],
              [True, False, False, False, True, True, True, True, False],
              [False, True, True, True, True, True, False, False, True],
              [False, True, True, True, True, False, True, True, False],
              [True, False, True, True, True, False, False, True, True],
              [True, True, True, True, True, True, True, True, True]]

left_border = [[True, False, True, True, True, True, True, False, True],
              [True, False, True, True, True, False, True, False, False],
              [True, True, True, True, True, False, True, True, True],
              [True, False, True, True, False, True, False, True, True],
              [True, False, True, True, True, False, True, False, True],
              [True, True, True, True, True, False, True, True, True],
              [True, True, False, True, False, True, True, True, False],
              [True, True, True, False, False, True, True, False, True],
              [True, False, True, False, False, True, True, True, False]]

right_border = [[False, True, True, True, True, True, False, True, True],
              [False, True, True, True, False, True, False, False, True],
              [True, True, True, True, False, True, True, True, True],
              [False, True, True, False, True, False, True, True, True],
              [False, True, True, True, False, True, False, True, True],
              [True, True, True, True, False, True, True, True, True],
              [True, False, True, False, True, True, True, False, True],
              [True, True, False, False, True, True, False, True, True],
              [False, True, False, False, True, True, True, False, True]]

groups = [[1, 1, 2, 3, 4, 5, 6, 6, 7], 
          [8, 8, 9, 3, 5, 5, 10, 10, 10], 
          [11, 8, 9, 12, 5, 5, 13, 10, 14], 
          [15, 15, 16, 12, 12, 13, 13, 17, 14], 
          [18, 18, 16, 19, 20, 20, 17, 17, 21], 
          [22, 18, 16, 19, 23, 23, 24, 25, 21], 
          [22, 26, 26, 27, 27, 28, 24, 25, 25], 
          [22, 29, 30, 30, 30, 28, 31, 31, 25], 
          [29, 29, 32, 32, 32, 28, 31, 33, 33]]

limits = {1: 10, 2: 9, 3: 15, 4: 3, 5: 26, 
          6: 12, 7: 1, 8: 13, 9: 6, 10: 22, 
          11: 7, 12: 18, 13: 19, 14: 8, 15: 6, 
          16: 9, 17: 6, 18: 22, 19: 8, 20: 12, 
          21: 13, 22: 18, 23: 4, 24: 5, 25: 25, 
          26: 8, 27: 10, 28: 18, 29: 12, 30: 14, 
          31: 11, 32: 18, 33: 17}

neighbors = {1: [[0, 0], [0, 1]], 
             2: [[0, 2]], 
             3: [[0, 3], [1, 3]], 
             4: [[0, 4]], 
             5: [[0, 5], [1, 5], [2, 5], [2, 4], [1, 4]], 
             6: [[0, 6], [0, 7]], 
             7: [[0, 8]], 
             8: [[1, 0], [1, 1], [2, 1]], 
             9: [[1, 2], [2, 2]], 
             10: [[1, 6], [1, 7], [2, 7], [1, 8]], 
             11: [[2, 0]], 
             12: [[2, 3], [3, 3], [3, 4]], 
             13: [[2, 6], [3, 6], [3, 5]], 
             14: [[2, 8], [3, 8]], 
             15: [[3, 0], [3, 1]], 
             16: [[3, 2], [4, 2], [5, 2]], 
             17: [[3, 7], [4, 7], [4, 6]], 
             18: [[4, 0], [4, 1], [5, 1]], 
             19: [[4, 3], [5, 3]], 
             20: [[4, 4], [4, 5]], 
             21: [[4, 8], [5, 8]], 
             22: [[5, 0], [6, 0], [7, 0]], 
             23: [[5, 4], [5, 5]], 
             24: [[5, 6], [6, 6]], 
             25: [[5, 7], [6, 7], [6, 8], [7, 8]], 
             26: [[6, 1], [6, 2]], 
             27: [[6, 3], [6, 4]], 
             28: [[6, 5], [7, 5], [8, 5]], 
             29: [[7, 1], [8, 1], [8, 0]], 
             30: [[7, 2], [7, 3], [7, 4]], 
             31: [[7, 6], [8, 6], [7, 7]], 
             32: [[8, 2], [8, 3], [8, 4]], 
             33: [[8, 7], [8, 8]]
            }

solution = [['4', '6', '9', '8', '3', '2', '5', '7', '1'], 
            ['2', '8', '1', '7', '4', '5', '9', '6', '3'], 
            ['7', '3', '5', '1', '9', '6', '8', '4', '2'], 
            ['5', '1', '3', '9', '8', '4', '7', '2', '6'], 
            ['6', '9', '4', '2', '5', '7', '3', '1', '8'], 
            ['8', '7', '2', '6', '1', '3', '4', '9', '5'], 
            ['9', '2', '6', '3', '7', '8', '1', '5', '4'], 
            ['1', '5', '8', '4', '2', '9', '6', '3', '7'], 
            ['3', '4', '7', '5', '6', '1', '2', '8', '9']]


# ========== validate_borders ==========
def test_validate_borders_1():
    """Test description: valid borders"""
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == True

def test_validate_borders_2():
    """Test descripton: open top border"""
    top_border[0][0] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    top_border[0][0] = True

def test_validate_borders_3():
    """Test description: open bottom border"""
    bottom_border[8][8] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    bottom_border[8][8] = True

def test_validate_borders_4():
    """Test description: open left border"""
    left_border[0][0] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    left_border[0][0] = True

def test_validate_borders_5():
    """Test description: open right border"""
    right_border[0][8] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    right_border[0][8] = True

def test_validate_borders_6():
    """Test description: missing vertically adjacent borders"""
    top_border[1][0] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    top_border[1][0] = True

def test_validate_borders_7():
    """Test description: missing vertically adjacent borders"""
    bottom_border[0][0] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    bottom_border[0][0] = True

def test_validate_borders_8():
    """Test description: missing vertically adjacent borders"""
    right_border[0][1] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    right_border[0][1] = True

def test_validate_borders_9():
    """Test description: missing horizontally adjacent borders"""
    left_border[0][2] = False
    assert KillerSudokuSolver.validate_borders(top_border, bottom_border, left_border, right_border) == False
    left_border[0][2] = True


# ========== validate_groups ==========
def test_validate_groups_1():
    """Test description: valid groups"""
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == True

def test_validate_groups_2():
    """Test description: inconsistent groups"""
    temp = limits[1]
    limits[1] = 0
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    limits[1] = temp

def test_validate_groups_3():
    """Test description: not disjoint groups"""
    neighbors[1].append([8,8])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

def test_validate_groups_4():
    """Test description: box without group"""
    x = neighbors[1].pop()
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].append(x)

def test_validate_groups_5():
    """Test description: group has box which is out of range"""
    neighbors[1].append([9,8])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

def test_validate_groups_6():
    """Test description: group has box which is out of range"""
    neighbors[1].append([8,9])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

def test_validate_groups_7():
    """Test description: group has box which is out of range"""
    neighbors[1].append([0,-1])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

def test_validate_groups_8():
    """Test description: group has box which is out of range"""
    neighbors[1].append([-1,0])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

def test_validate_groups_9():
    """Test description: groups members are not unique"""
    neighbors[1].append([0,0])
    assert KillerSudokuSolver.validate_groups(sums, limits, neighbors) == False
    neighbors[1].pop()

# ========== group ==========
def test_group_1():
    """Test description: valid set up"""
    result = KillerSudokuSolver.group(sums, top_border, bottom_border, left_border, right_border)
    assert len(result) == 3
    groups_, limits_, neighbors_ = result
    assert groups == groups_
    assert limits == limits_
    assert neighbors == neighbors_

def test_group_2():
    """Test description: valid set up"""
    temp = sums[0][1]
    sums[0][1] = 0
    result = KillerSudokuSolver.group(sums, top_border, bottom_border, left_border, right_border)
    assert len(result) == 3
    groups_, limits_, neighbors_ = result
    assert groups == groups_
    assert limits == limits_
    assert neighbors == neighbors_
    sums[0][1] = temp

# ========== validate_region ==========
def test_validate_region_1():
    """Test description: Region has empty space and is below total value"""
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 0, 2) == True

def test_validate_region_2():
    """Test description: Region is full and is equal to total value"""
    board[0][2] = '9'
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 0, 2) == True
    board[0][2] = ''

def test_validate_region_3():
    """Test description: Region is full and over total value"""
    board[0][8] = '2'
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 0, 8) == False
    board[0][8] = ''

def test_validate_region_4():
    """Test description: Region is full and under total value"""
    board[0][2] = '1'
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 0, 2) == False
    board[0][2] = ''

def test_validate_region_5():
    """Test description: Region has empty space and is equal to total value"""
    board[4][2] = '9'
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 4, 2) == False
    board[4][2] = ''

def test_validate_region_6():
    """Test description: Region has empty space and is over total value"""
    board[6][1] = '9'
    assert KillerSudokuSolver.validate_region(board, groups, limits, neighbors, 6, 1) == False
    board[6][1] = ''

# ========== killer_sudoku_solver ==========
def test_killer_sudoku_solver_1():
    """Test description: Valid board with solution"""
    assert KillerSudokuSolver.solve(board, sums, top_border, bottom_border, left_border, right_border) == solution

def test_killer_sudoku_solver_2():
    """Test description: Invalid board with no solution"""
    board[0][0] = '1'
    assert KillerSudokuSolver.solve(board, sums, top_border, bottom_border, left_border, right_border) == None
    board[0][0] = ''