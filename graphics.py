import tkinter as tk
EMPTY = 0
PLAYER_1_KITTEN = 1
PLAYER_2_KITTEN = 2
PLAYER_1_CAT = 3
PLAYER_2_CAT = 4
ASSET_SIZE = 200

class Gameboard:
    def __init__(self, tile_size, dimension = 6, click_handler = None):
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

        # ----- Status Display -----
        self.info_frame = tk.Frame(self.game)
        self.info_frame.pack(fill="x", pady=5)

        self.turn_label = tk.Label(
            self.info_frame,
            text="Player 1's Turn",
            font=("Arial", 16, "bold")
        )
        self.turn_label.pack()

        self.player1_label = tk.Label(
            self.info_frame,
            text="Player 1 - Kittens: 8 | Cats: 0",
            font=("Arial", 12)
        )
        self.player1_label.pack(anchor="w")

        self.player2_label = tk.Label(
            self.info_frame,
            text="Player 2 - Kittens: 8 | Cats: 0",
            font=("Arial", 12)
        )
        self.player2_label.pack(anchor="w")

        # ----- Game Board -----
        self.canvas = tk.Canvas(
            self.game,
            width=self.DIMENSION * self.TILE_SIZE,
            height=self.DIMENSION * self.TILE_SIZE
        )
        self.canvas.pack()

        # Click event handler
        self.click_handler = click_handler
        # Switch button event handler
        self.switch_handler = None
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

        # Button to switch between placing kittens and cats
        self.switch_button = tk.Button(
            self.info_frame,
            text="Switch Game Piece",
            command=self.on_switch_clicked
        )
        self.switch_button.pack(pady=5)

    def on_switch_clicked(self):
        if self.switch_handler:
            self.switch_handler()

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

    # Function to update current player pieces and whose turn it is
    def update_status(self, current_player, players, placing_cats):
        self.turn_label.config(
            text=f"Player {current_player}'s Turn"
        )

        self.player1_label.config(
            text=f"🟧 Player 1 - Kittens: {players[1]['kittens']} | Cats: {players[1]['cats']}",
            fg="orange" if current_player == 1 else "black"
        )

        self.player2_label.config(
            text=f"⬜ Player 2 - Kittens: {players[2]['kittens']} | Cats: {players[2]['cats']}",
            fg="gray" if current_player == 2 else "black"
        )

        player_cats = players[current_player]["cats"]
        if player_cats == 0:
            self.switch_button.config(
                text="No Cats Available",
                state="disabled"
            )
        else:
            self.switch_button.config(
                state="normal",
                text="Switch to Kitten" if placing_cats else "Switch to Cat"
            )

    def canvas_clicked(self, event):
        print("Canvas clicked")
        # Get coordinates of click location
        col = event.x // self.TILE_SIZE
        row = event.y // self.TILE_SIZE

        if 0 <= row < self.DIMENSION and 0 <= col < self.DIMENSION:
            if self.click_handler:
                self.click_handler(row, col)





