import numpy as np
EMPTY = None

# Helper function to detect and clear matching in a 1d array
def check_row(row):
    # Sliiiiiiiide to the...right?
    left = 0
    removed = []

    while left < len(row):
        if row[left] is None:
            left += 1
            continue

        right = left
        while (right < len(row)) and (row[right] is not None) and (row[right] == row[left]):
            right += 1

        length = right - left

        if row[left] is not None and length > 2:
            removed.append((row[left], length))
            row[left:right] = [EMPTY] * length

        left = right

    return row, removed

def get_diagonal(board, offset):
    rows, cols = board.shape
    coords = []
    values = []

    for r in range(rows):
        c = r - offset
        if 0 <= c < cols:
            coords.append((r, c))
            values.append(board[r, c])

    return coords, values

def get_anti_diagonal(board, offset):
    rows, cols = board.shape
    coords = []
    values = []

    for r in range(rows):
        c = offset - r
        if 0 <= c < cols:
            coords.append((r, c))
            values.append(board[r, c])

    return coords, values

def write_back(board, coords, values):
    for (r, c), v in zip(coords, values):
        board[r, c] = v

def update_matchings(board):
    all_removed_symbols = []
    rows, cols = board.shape

    # Check row using check_row helper function
    for index, row in enumerate(board):
        new_row, removed_symbols = check_row(row)
        all_removed_symbols.extend(removed_symbols)
        board[index] = new_row

    # Check columns using check_row helper function and transposed board
    for index, col in enumerate(board.T):
        new_col, removed_symbols = check_row(col)
        all_removed_symbols.extend(removed_symbols)
        board[:, index] = new_col

    # no idea (some idea) how this works for diagonals and anti-diagonals
    for offset in range(-(rows - 1), cols):
        coords, diag = get_diagonal(board, offset)

        if len(diag) >= 3:
            new_diag, removed = check_row(diag)
            all_removed_symbols.extend(removed)
            write_back(board, coords, new_diag)

    for offset in range(rows + cols - 1):
        coords, diag = get_anti_diagonal(board, offset)

        if len(diag) >= 3:
            new_diag, removed = check_row(diag)
            all_removed_symbols.extend(removed)
            write_back(board, coords, new_diag)

    return all_removed_symbols




# # row = [0,0,1,1,1,0,0]
# # removed = check_row(row)
# # print(row, removed)
#
# board = np.array([[1,1,1,1,1,1],
# [1,1,1,1,1,1],
# [1,1,1,1,1,1],
# [1,1,1,1,1,1],
# [1,1,1,1,1,1],
# [1,1,1,1,1,1]])
#
# updated = update_matchings(board)
# print(board)
# print(updated)
