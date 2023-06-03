import pyxel

# Sure, here is a state machine that includes states 
# for the MainMenuState, 
# the MainGameBoardState, 
# SelectActionState, 
# BattleState, 
# EndGameState. 
# Each state has its own draw() and update() methods:


class App:

    def __init__(self):
        # Initialize the Pyxel library.
        # pyxel.init(640, 480)

        # Load the sprite sheet.
        # self.sprite_sheet = pyxel.image.load("assets/space_hulk.png")

        # Create the player sprite.
        # self.player_sprite = pyxel.sprite.Sprite(self.sprite_sheet, 0, 0)

        # Create the enemy sprites.
        # self.enemy_sprites = []
        # for i in range(10):
        #     self.enemy_sprites.append(pyxel.sprite.Sprite(self.sprite_sheet, i * 16, 64))

        # Create the state machine.
        self.state_machine = StateMachine()
        self.state_machine.add_state(MainMenuState(self))
        self.state_machine.add_state(MainGameBoardState(self))
        self.state_machine.add_state(SelectActionState(self))
        self.state_machine.add_state(BattleState(self))
        self.state_machine.add_state(EndGameState(self))

        # Set the initial state.
        self.state_machine.set_state(MainMenuState)

    def update(self):
        # Update the state machine.
        self.state_machine.update()

        # Update the player sprite.
        self.player_sprite.update()

        # Update the enemy sprites.
        for enemy_sprite in self.enemy_sprites:
            enemy_sprite.update()

        # Check for collisions between the player and enemies.
        for enemy_sprite in self.enemy_sprites:
            if enemy_sprite.collide(self.player_sprite):
                # The player has been hit!
                pyxel.play(pyxel.sounds[0])
                self.player_sprite.x = SCREEN_WIDTH / 2
                self.player_sprite.y = SCREEN_HEIGHT / 2

    def draw(self):
        # Clear the screen.
        pyxel.cls(0)

        # Draw the player sprite.
        pyxel.draw(self.player_sprite)

        # Draw the enemy sprites.
        # for enemy_sprite in self.enemy_sprites:
        #     pyxel.draw(enemy_sprite)

        # Draw the state machine.
        self.state_machine.draw()


# The state machine is responsible for managing the different states of the game. 
# The state machine has a list of states, and each state has its own draw() and update() methods. 
# The state machine updates the current state, and then calls the draw() method of the current state to draw the game objects to the screen.

# The following states are defined in the state machine:

# * MainMenuState: This state displays the main menu.
# * MainGameBoardState: This state displays the main game board.
# * SelectActionState: This state displays the select action menu.
# * BattleState: This state displays the battle screen.
# * EndGameState: This state displays the end game screen.
