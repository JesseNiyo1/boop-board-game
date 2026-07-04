import graphics
import game_logic
import numpy as np

graphics = graphics.Gameboard(6, 100)
logic = game_logic.GameLogic(graphics)

graphics.click_handler = logic.on_tile_click
graphics.make_board()


graphics.game.mainloop()
