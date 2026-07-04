from boop import *
from match_checking import *

EMPTY = None

class GameLogic:
    def __init__(self, gameboard):
        self.board = np.full((6, 6), None, dtype=object)
        self.gameboard = gameboard

        self.players = {
            1: {"kittens": 8, "cats": 0},
            2: {"kittens": 8, "cats": 0},
        }
        self.is_player_1_turn = True
        self.game_done = False
        self.victor = 0
        self.placing_cats = False


    # Will have to update this to include switching between placing kittens and cats
    def on_tile_click(self, row, col):
        """
        Applies game logic when tile is clicked (piece is placed on board). Handles re-drawing of board,
        update player resources, and booping logic (SOON).
        :param row: Tile's row
        :param col: Tile's column
        :return:
        """
        # Using this to debug
        print(f"Clicked {row}, {col}")

        # Make sure tile is empty
        if self.board[row][col] is not None:
            return

        # Determine whose turn it is
        player = 1 if self.is_player_1_turn else 2


        # Use appropriate symbol representation for kittens/cats
        piece = (player, "cat" if self.placing_cats else "kitten")

        # Place game piece, apply boop logic, and update player resources accordingly
        self.place_game_piece(row, col, piece)
        self.board, removed_pieces = boop(self.board, row, col)
        self.update_resources(removed_pieces)
        # Check for matchings
        matched_pieces = update_matchings(self.board)
        self.match_detected(matched_pieces)


        # Flip whose turn it is
        self.is_player_1_turn = not self.is_player_1_turn
        # Re-draw board
        self.gameboard.update_board(self.board)

        # Using this to debug
        print(f"Clicked {row}, {col}")
        print(self.players)


    def place_game_piece(self, row, col, piece):
        player, piece_type = piece
        self.board[row][col] = piece

        # Wooo I love grammar
        self.players[player][piece_type + "s"] -= 1

    def update_resources(self, removed_pieces):
        for piece in removed_pieces:
            player, piece_type = piece
            self.players[player][piece_type + "s"] += 1

    def match_detected(self, pieces):
        for piece, count in pieces:
            player, piece_type = piece

            if piece is None:
                continue

            if piece_type == "cat":
                self.game_done = True
                self.victor = player
                break
            else:
                self.players[player]["cats"] += count
