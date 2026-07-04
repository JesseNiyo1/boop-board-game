import graphics
import game_logic

board = graphics.Gameboard(tile_size=100)
logic = game_logic.GameLogic(board)

board.click_handler = logic.on_tile_click

logic.refresh_display()

board.game.mainloop()