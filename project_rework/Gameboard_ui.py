

class GameBoard():
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.board_size = game.board_size
        self.board_ui = []
        self.board_ui_size = 0
        self.board_ui_size = self.board_size * 2 + 1
        self.board_ui = self.create_board_ui()