#    Main Author(s): 
#    Main Reviewer(s):

from a1_partc import Queue

def get_overflow_list(grid):
    """
    Identifies cells in the grid that overflow based on their neighbors.

    Args:
        grid (list of list of int): The 2D grid to process.

    Returns:
        list of tuple: List of coordinates for cells that overflow.
    """
    rows = len(grid)
    cols = len(grid[0])
    overflow_list = []

    for row in range(rows):
        for col in range(cols):
            if (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1):
                neighbors = 2
            elif row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                neighbors = 3
            else:
                neighbors = 4

            if abs(grid[row][col]) >= neighbors:
                overflow_list.append((row, col))

    return overflow_list if overflow_list else None


def overflow(grid, a_queue):
    """
    Recursively applies the overflow process to the grid and updates the queue with each new grid state.

    Args:
        grid (list of list of int): The 2D grid to process.
        a_queue (Queue): The queue to store intermediate grid states.

    Returns:
        int: The number of overflow operations performed.
    """
    overflow_cells = get_overflow_list(grid)
    if not overflow_cells or all_same_signs(grid):
        return 0

    apply_overflow(grid, overflow_cells)
    a_queue.enqueue([row[:] for row in grid])
    return 1 + overflow(grid, a_queue)


def get_neighbors(grid, row, col):
    """
    Gets the neighboring cells of a given cell in the grid.

    Args:
        grid (list of list of int): The 2D grid.
        row (int): The row index of the cell.
        col (int): The column index of the cell.

    Returns:
        list of tuple: List of coordinates for neighboring cells.
    """
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors


def apply_overflow(grid, overflow_cells):
    """
    Applies the overflow process to the specified cells in the grid.

    Args:
        grid (list of list of int): The 2D grid to process.
        overflow_cells (list of tuple): List of coordinates for cells that overflow.
    """
    sign = 1 if grid[overflow_cells[0][0]][overflow_cells[0][1]] > 0 else -1

    for r, c in overflow_cells:
        grid[r][c] = 0

    for r, c in overflow_cells:
        for nr, nc in get_neighbors(grid, r, c):
            grid[nr][nc] = sign * abs(grid[nr][nc])
            grid[nr][nc] += sign


def all_same_signs(grid):
    """
    Checks if all non-zero cells in the grid have the same sign.

    Args:
        grid (list of list of int): The 2D grid to check.

    Returns:
        bool: True if all non-zero cells have the same sign, False otherwise.
    """
    signs = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                signs.add(1 if cell > 0 else -1)
            if len(signs) > 1:
                return False
    return len(signs) <= 1
