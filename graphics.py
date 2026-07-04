import tkinter as tk
EMPTY = 0
PLAYER_1_KITTEN = 1
PLAYER_2_KITTEN = 2
PLAYER_1_CAT = 3
PLAYER_2_CAT = 4
ASSET_SIZE = 200

class Gameboard:
    def __init__(self, dimension, tile_size, click_handler = None):
        """
        Initialize the game board
        :param dimension: Size of the board (Typically 6 x 6)
        :param tile_size: image dimension of image assets (right now everything is 64 x 64 pixels)
        """
        self.DIMENSION = dimension
        self.TILE_SIZE = tile_size

        # Typical tkinter setup bs don't mind this
        self.game = tk.Tk()
        self.game.title("boop.")
        self.canvas = tk.Canvas(self.game, width=self.DIMENSION * self.TILE_SIZE, height=self.DIMENSION * self.TILE_SIZE)
        self.canvas.pack()

        # Click event handler
        self.click_handler = click_handler
        # Button-1 = Left Mouse click
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        # Retrieve image assets for later
        # Scale factor based on ASSET_SIZE and TILE_SIZE
        scale = max(1, round(ASSET_SIZE // self.TILE_SIZE))

        self.light_tile = tk.PhotoImage(file="./assets/light_blue_tile.png").subsample(scale, scale)
        self.dark_tile = tk.PhotoImage(file="./assets/dark_blue_tile.png").subsample(scale, scale)
        self.orange_kitten = tk.PhotoImage(file="./assets/orange_kitten.png").subsample(scale, scale)
        self.gray_kitten = tk.PhotoImage(file="./assets/gray_kitten.png").subsample(scale, scale)
        self.orange_cat = tk.PhotoImage(file="./assets/orange_cat.png").subsample(scale, scale)
        self.gray_cat = tk.PhotoImage(file="./assets/gray_cat.png").subsample(scale, scale)

    def make_board(self):
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                x = col * self.TILE_SIZE
                y = row * self.TILE_SIZE
                # Alternate between light and dark tiles
                tile = self.light_tile if (row + col) % 2 == 0 else self.dark_tile

                self.canvas.create_image(x, y, image=tile, anchor="nw")

    def update_board(self, board):
        """
        Given a NumPy array, draws the appropriate board state
        0 - Empty tile
        1 - Player 1 Kitten
        2 - Player 2 Kitten
        3 - Player 1 Cat
        4 - Player 2 Cat
        :param board: NumPy array
        :return: None
        """

        # Just delete current board and re-draw it
        self.canvas.delete("all")
        self.make_board()

        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                x = col * self.TILE_SIZE
                y = row * self.TILE_SIZE

                piece = board[row, col]

                if piece is None:
                    continue

                player, piece_type = piece

                if player == 1 and piece_type == "kitten":
                    self.canvas.create_image(x, y, image=self.orange_kitten, anchor="nw")

                elif player == 2 and piece_type == "kitten":
                    self.canvas.create_image(x, y, image=self.gray_kitten, anchor="nw")

                elif player == 1 and piece_type == "cat":
                    self.canvas.create_image(x, y, image=self.orange_cat, anchor="nw")

                elif player == 2 and piece_type == "cat":
                    self.canvas.create_image(x, y, image=self.gray_cat, anchor="nw")

    def canvas_clicked(self, event):
        print("Canvas clicked")
        # Get coordinates of click location
        col = event.x // self.TILE_SIZE
        row = event.y // self.TILE_SIZE

        if 0 <= row < self.DIMENSION and 0 <= col < self.DIMENSION:
            if self.click_handler:
                self.click_handler(row, col)





