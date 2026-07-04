import graphics
import game_logic

board = graphics.Gameboard(tile_size=100)
logic = game_logic.GameLogic(board)

board.click_handler = logic.on_tile_click
board.make_board()

board.update_board(logic.board)

current_player = 1 if logic.is_player_1_turn else 2
board.update_status(current_player, logic.players)

board.game.mainloop()