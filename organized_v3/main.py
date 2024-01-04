import pyxel
from game_state import GameState
from ui import UI

class App:
    def __init__(self):
        # pyxel.init(160, 120, caption="Space Hulk: Death Angel")
        # self.game_state = GameState()
        # self.ui = UI(self.game_state)
        # pyxel.run(self.update, self.draw)
        pass

    def update(self):
    #     if pyxel.btnp(pyxel.KEY_Q):
    #         pyxel.quit()
        
    #     self.game_state.update()  # Update the game state
    #     self.ui.handle_input()   # Handle user input
        pass

    def draw(self):
    #     pyxel.cls(0)
    #     self.ui.draw()  # Draw the game state
        pass

if __name__ == "__main__":
    App()