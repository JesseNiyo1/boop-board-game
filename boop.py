EMPTY = None

def boop(board, boop_row, boop_col):
    board = board.copy()
    removed_pieces = []

    booping_piece = board[boop_row][boop_col]

    if booping_piece is None:
        return board, removed_pieces

    _, booping_type = booping_piece
    can_boop = {
        "kitten": {"kitten"},
        "cat": {"kitten", "cat"}
    }

    boopable_types = can_boop[booping_type]

    for row in range(max(0, boop_row - 1), min(len(board), boop_row + 2)):
        for col in range(max(0, boop_col - 1), min(len(board[0]), boop_col + 2)):

            target_piece = board[row][col]

            if row == boop_row and col == boop_col or target_piece is None:
                continue

            _, target_type = target_piece

            if target_type not in boopable_types:
                continue

            # Compute destination
            new_row = row + (row - boop_row)
            new_col = col + (col - boop_col)

            # booped off the board, return to appropriate player
            if (new_row < 0 or new_row >= len(board)) or (new_col < 0 or new_col >= len(board[0])):
                board[row][col] = EMPTY
                removed_pieces.append(target_piece)
                continue

            # No chain reactions allowed!
            if board[new_row][new_col] is not None:
                continue

            # boop.
            board[row][col] = EMPTY
            board[new_row][new_col] = target_piece

    return board, removed_pieces