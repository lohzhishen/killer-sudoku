from typing import Callable
from config import *


class SudokuSolver:
    @classmethod
    def solve(cls, board: list[list[str]]) -> list[list[list[str]]] | None:
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
        if not cls.validate_sudoku_board(board):
            # invalid board arragement
            return None
        
        # solve the game
        if not cls.iteration(board, 0, cls.sudoku_validate):
            return None
        return board

    @classmethod
    def iteration(cls, board: list[list[str]], pos: int, validation: Callable, **kwargs: dict) -> bool:
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
        pos = cls.find_next_empty(board, pos)
        if pos == -1:
            # no empty position found
            return True
        
        # try all possible values at the empty position
        r, c = pos // SUDOKU_SIZE, pos % SUDOKU_SIZE
        for action in [x for x in ACTIONS if x not in board[r]]:
            board[r][c] = action
            if (not validation(board, r, c, **kwargs) or # check if move is legal
                not cls.iteration(board, pos, validation, **kwargs)):
                continue
            return True
        
        # reset the position to its initial state
        board[r][c] = ''
        return False

    @classmethod
    def find_next_empty(cls, board: list[list[str]], pos: int) -> int:
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
        return -1 if (pos == SUDOKU_SIZE ** 2 or pos < 0) else pos

    @classmethod
    def sudoku_validate(cls, board: list[list[str]], r: int, c: int, **kwargs: dict) -> bool:
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
        return cls.validate_box(board, r, c) and cls.validate_col(board, r, c)

    @classmethod
    def validate_box(cls, board: list[list[str]], i: int, j: int) -> bool:
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

    @classmethod
    def validate_col(cls, board: list[list[str]], i: int, j: int) -> bool:
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
    
    @classmethod
    def validate_sudoku_board(cls, board: list[list[str]]) -> bool:
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

class KillerSudokuSolver(SudokuSolver):
    @classmethod
    def solve(
            cls,
            board: list[list[str]], 
            sums: list[list[int]], 
            top_border: list[list[bool]], 
            bottom_border: list[list[bool]], 
            left_border: list[list[bool]], 
            right_border: list[list[bool]]
            ) -> list[list[list[str]]] | None:
        """Solves a killer sudoku game.
        
        Parameters
        ----------
        board: list[list[str]]
            A 2D array containing the values placed onto the board.
        sums: list[list[int]]
            The sum limit for each box on the board.
        top_border: list[list[bool]]
            A 2D array indicating the presence of a border on the top.
        bottom_border: list[list[bool]]
            A 2D array indicating the presence of a border on the bottom.
        left_border: list[list[bool]]
            A 2D array indicating the presence of a border on the left.
        right_border: list[list[bool]]
            A 2D array indicating the presence of a border on the right.

        Returns
        -------
        board: list[list[str]]
            A 2D array containing the values placed onto the board. It has no empty spots.
        If None is returned, the game parameters are invalid or it has no solution.
        """
        # validate the parameters of the game
        if not cls.validate_sudoku_board(board):
            # invalid board arragement
            return None

        result = cls.group(sums, top_border, bottom_border, left_border, right_border)
        if result is None:
            # problem detected in either the borders or group limit is inconsistent
            return None
        groups, limits, neighbors = result

        # solve the game
        if not cls.iteration(board, 0, cls.killer_sudoku_validate, groups=groups, limits=limits, neighbors=neighbors):
            return None
        return board

    @classmethod
    def killer_sudoku_validate(
            cls,
            board: list[list[str]], 
            r: int, 
            c: int, 
            **kwargs: dict
            ) -> bool:
        """Validates a move made in killer sudoku.
        
        Parameters
        ----------
        board: list[list[str]]
            A 2D array containing the values placed onto the board.
        i: int
            Row index where the new value was placed.  
        j: int
            Column index where the new value was placed.

        Keyword Arguments
        -----------------
        groups: list[list[int]]
            A 2D array indicating the group number of a position.
        limits: dict[int: int]
            A dictionary linking each group number to the sum of the group.
        neighbors: dict[int: list[list[int, int]]]
            A dictionary linking each group number to the positions of all members in the group.

        Returns
        -------
        validity: bool
            Indicates if the move was legal.
        """
        groups = kwargs['groups']
        limits = kwargs['limits']
        neighbors = kwargs['neighbors']
        return cls.sudoku_validate(board, r, c) and cls.validate_region(board, groups, limits, neighbors, r, c)
    
    @classmethod
    def validate_region(
            cls,
            board: list[list[str]], 
            groups: list[list[int]], 
            limits: dict, 
            neighbors: dict[int: list[list[int, int]]], 
            i: int, 
            j: int
            ) -> bool:
        """Validates that new value at (i,j) does not cause group sum to rise above its limit.
        
        Parameters
        ----------
        board: list[list[str]]
            A 2D array containing the values placed onto the board.
        groups: list[list[int]]
            A 2D array indicating the group number of a position.
        limits: dict[int: int]
            A dictionary linking each group number to the sum of the group.
        neighbors: dict[int: list[list[int, int]]]
            A dictionary linking each group number to the positions of all members in the group.
        i: int
            Row index where the new value was placed.  
        j: int
            Column index where the new value was placed.
        
        Returns
        -------
        validity: bool
            Indicates if the group sum has been violated.
        """
        # extract out relevant information for this group
        group = groups[i][j]
        limit = limits[group]
        neighbor = neighbors[group]

        # validate the group sum
        total = 0
        empty = False
        for x, y in neighbor:
            if board[x][y] != '':
                total += int(board[x][y])
            else:
                empty = True
        if empty:
            return total < limit
        else:
            return total == limit

    @classmethod      
    def group(
            cls,
            sums: list[list[int]], 
            top_border: list[list[bool]], 
            bottom_border: list[list[bool]], 
            left_border: list[list[bool]], 
            right_border: list[list[bool]]
            ) -> tuple[list[list[int]], dict[int: int], dict[int: list[list[int, int]]]] | None:
        """Establishes the groups on the board. 
        
        Parameters
        ----------
        sums: list[list[int]]
            The sum limit for each box on the board.
        top_border: list[list[bool]]
            A 2D array indicating the presence of a border on the top.
        bottom_border: list[list[bool]]
            A 2D array indicating the presence of a border on the bottom.
        left_border: list[list[bool]]
            A 2D array indicating the presence of a border on the left.
        right_border: list[list[bool]]
            A 2D array indicating the presence of a border on the right.

        Returns
        -------
        groups: list[list[int]]
            A 2D array indicating the group number of a position.
        limits: dict[int: int]
            A dictionary linking each group number to the sum of the group.
        neighbors: dict[int: list[list[int, int]]]
            A dictionary linking each group number to the positions of all members in the group.
        If the return value is None, the configuration of the board is not valid.
        """
        if not cls.validate_borders(top_border, bottom_border, left_border, right_border):
            # problem detected with the borders
            return None
        
        groups = [[0 for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        visited = [[False for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
        limits = {} # group_number: sum of group
        neighbors = {} # group_number: list of positions
        group_number = 0

        def explore(i: int, j: int, group_number: int) -> None:
            """DFS exploration of the game board.
            
            Parameters
            ----------
            i: int
                The row index of the current position.
            j: int
                The column index of the current position.
            group_number: int
                The group which is currently being explored.

            Remarks
            -------
            This algorithm assumes that the borders are valid.
            """
            sums[i][j] = limits[group_number]
            groups[i][j] = group_number
            visited[i][j] = True
            neighbors[group_number].append([i, j])

            # visit adjacent cells
            if not top_border[i][j] and not visited[i - 1][j]:
                explore(i - 1, j, group_number)
            if not bottom_border[i][j] and not visited[i + 1][j]:
                explore(i + 1, j, group_number)
            if not left_border[i][j] and not visited[i][j - 1]:
                explore(i, j - 1, group_number)
            if not right_border[i][j] and not visited[i][j + 1]:
                explore(i, j + 1, group_number)

        # explore the board
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                if not visited[i][j] and sums[i][j] != 0:
                    group_number += 1
                    limits[group_number] = sums[i][j]
                    neighbors[group_number] = []
                    explore(i, j, group_number)
        
        if not cls.validate_groups(sums, limits, neighbors):
            # inconsistent sum of group
            return None

        return groups, limits, neighbors

    @classmethod
    def validate_borders(
            cls,
            top_border: list[list[bool]], 
            bottom_border: list[list[bool]], 
            left_border: list[list[bool]], 
            right_border: list[list[bool]]
            ) -> bool:   
        """Verifies if the borders are consistent.
        
        Parameters
        ----------
        top_border: list[list[bool]]
            A 2D array indicating the presence of a border on the top.
        bottom_border: list[list[bool]]
            A 2D array indicating the presence of a border on the bottom.
        left_border: list[list[bool]]
            A 2D array indicating the presence of a border on the left.
        right_border: list[list[bool]]
            A 2D array indicating the presence of a border on the right.

        Returns
        -------
        validity: bool
            Indicates whether the borders are consistent.
        """ 
        # iterate over each cell in the board
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                if (# top row must have a border above
                    (i == 0 and not top_border[i][j]) or
                    # bottom row must have a border below  
                    (i == SUDOKU_SIZE - 1 and not bottom_border[i][j]) or 
                    # left most row must have a border on the left
                    (j == 0 and not left_border[i][j]) or
                    # right most row must have a border on the right
                    (j == SUDOKU_SIZE - 1 and not right_border[i][j]) or 
                    # for every cell with a border above, the cell above must have a border below
                    (0 < i < SUDOKU_SIZE and top_border[i][j] and not bottom_border[i - 1][j]) or
                    (0 <= i < SUDOKU_SIZE - 1 and bottom_border[i][j] and not top_border[i + 1][j]) or
                    # for every cell with a border on the right, the cell to the right must have a border on the left 
                    (0 <= j < SUDOKU_SIZE - 1 and right_border[i][j] and not left_border[i][j + 1]) or
                    (0 < j < SUDOKU_SIZE and left_border[i][j] and not right_border[i][j - 1])
                    ):
                    return False
        return True

    @classmethod
    def validate_groups(
            cls,
            sums:list[list[int]], 
            limits: dict[int: int], 
            neighbors: dict[int: list[list[int, int]]]
            ) -> bool:
        """Verifies the consistency of the sum limit within each group.
        
        Parameters
        ----------
        sums: list[list[int]]
            The sum limit for each box on the board.
        limits: dict[int: int]
            A dictionary linking each group number to the sum of the group.
        neighbors: dict[int: list[list[int, int]]]
            A dictionary linking each group number to the positions of all members in the group.

        Returns
        -------
        validity: bool
            Indicates whether each member of a group has the same sum limit.
        """
        seen = []
        # iterate over all the groups
        for group_number, total in limits.items():
            # check if each member within the group has the same sum limit
            for x, y in neighbors[group_number]:
                seen.append((x, y))
                if 0 > x or x >= SUDOKU_SIZE or 0 > y or y >= SUDOKU_SIZE or sums[x][y] != total:
                    return False
        # check if every box is in a group
        # and check if groups are disjoint
        return len(seen) == SUDOKU_SIZE ** 2 and len(seen) == len(set(seen))
        

