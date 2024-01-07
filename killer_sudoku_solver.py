from sudoku_solver import sudoku_validate, iteration

def killer_sudoku_solver(board: list[list[str]], group: list[list[int]], limit: dict[int: int], 
                  neighbors: dict[int: list[list[int, int]]]) -> list[list[list[str]]]:
    if not iteration(board, 0, killer_sudoku_validate, group=group, limit=limit, neighbors=neighbors):
        return None
    return board


def killer_sudoku_validate(board: list[list[str]], r: int, c: int, **kwargs: dict) -> bool:
    group = kwargs['group']
    limit = kwargs['limit']
    neighbors = kwargs['neighbors']
    return sudoku_validate(board, r, c) and validate_region(board, group, limit, neighbors, r, c)
   

def validate_region(board: list[list[str]], group: list[list[int]], limit: dict, neighbors: dict, i: int, j: int) -> bool:
    group = group[i][j]
    limit = limit[group]
    neighbors = neighbors[group]
    total = sum(int(board[x][y]) for x, y in neighbors if board[x][y] != '')
    if total > limit:
        return False
    return True