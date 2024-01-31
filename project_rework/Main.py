import pyxel
import action_cards as ac
import shda_marines as sm
import Genestealers as gs
import locations as loc
import event_cards as ec
import overlay_action_cards as oac
import ui

# SCREEN DIMENSIONS
SCREEN_X = 257
SCREEN_Y = 257

# TEAM COLORS
GREY = 13
GREEN = 3
RED = 8

location_and_spawns = loc.Location_and_spawns(gs.gs_deck_create())
event_cards = ec.Event_cards(ec.event_deck)
drawn_event_card = event_cards.draw_card()
location_and_spawns.populate_blips()

initial_spawns = location_and_spawns.gs_spawn_locs(drawn_event_card)
location_and_spawns.populate_GS_spawns(initial_spawns)

# INITIAL SM PLACEMENT
space_marines = sm.Space_marines()

class GameState:
    def __init__(self):
        self.next_state = None
        self.prev_state = None
        self.space_marines = space_marines

    def back(self):
        self.next_state = self.prev_state
        self.prev_state = None

    def proceed(self, new_state):
        self.next_state = new_state


class MainMenuState(GameState):
    def __init__(self):
        super().__init__()
        # Play menu music
        pyxel.playm(0,loop=True)
        self.counter = 0
        
    def update(self, game):
        # Click screen to start game
        if ui.box_click(0, 0, SCREEN_X, SCREEN_Y):
                pyxel.stop()
                self.next_state = GameBoardState()

    def draw(self, game):
        pyxel.cls(0)
        # Creates flashing text
        if pyxel.frame_count % 10 == 0:
            flash = 6
        else:
            flash = 10
        pyxel.text(SCREEN_X//2 - 16, (SCREEN_Y//2) - 12, 
                   "Space Hulk", 3)
        pyxel.text(SCREEN_X//2 - 18, (SCREEN_Y//2), 
                   "Death Angel", 6)
        pyxel.text(SCREEN_X//2 - 38, (SCREEN_Y//2) + 26, 
                   "Click screen to start", flash)


class GameBoardState(GameState):
    def __init__(self):
        super().__init__()
        self.resolve_phase = False

    def update(self, game):
        if ui.phase_box_click():
            self.resolve_phase = True
            self.next_state = SelectActionState()

    def draw(self, game):
        # Draw the main game screen
        pyxel.cls(0)
        location_and_spawns.draw()
        self.space_marines.formation_draw()
        pyxel.rectb(ui.select_box[0], ui.select_box[1], 
                    ui.select_box[2], ui.select_box[3], 4)
    
        pyxel.text(ui.select_box[0]+4, ui.select_box[1]+4,  
                            "SELECT ACTIONS", 7)
     

class SelectActionState(GameState):
    def __init__(self):
        super().__init__()
        self.action_cards = ac.Action_cards()

    def update(self, game):
        # Check for input to select an action card
        self.action_cards.update()
        # Checks if action cards are selected, sends them to GameState & switches back to GameBoardState
        if self.action_cards.sorted_cards:
            action_card_choices = self.action_cards.sorted_cards
            self.next_state = ResolveActionState(action_card_choices)

    def draw(self, game):
        self.action_cards._draw()

# TODO
# TODO
# TODO - competely rework this state, first pass was GARBAGGIO
# TODO
# TODO
class ResolveActionState(GameState):
    def __init__(self, action_card_choices):
        super().__init__()
        self.action_overlay = oac.ResolveActionUI(action_card_choices, space_marines, location_and_spawns)

    def update(self, game):
        self.action_overlay.update()

    def draw(self, game):
        pyxel.cls(0)
        pyxel.text(101, 8, "Resolve Action", 7) 
        pyxel.text(119, 16, "State", 7)
        self.space_marines.formation_draw()
        location_and_spawns.draw()
        self.action_overlay.overlay_draw()


######################
######################
class App:
    def __init__(self):
        pyxel.init(SCREEN_X, SCREEN_Y, title="SPACE HULK: DEATH ANGEL", fps=30)
        pyxel.load("sh_da copy.pyxres")
        pyxel.mouse(True)
        self.state = MainMenuState()
        pyxel.run(self.update, self.draw)

    def update(self):
            if self.state.next_state is not None:
                self.state.next_state.prev_state = self.state
                self.state = self.state.next_state
                self.state.next_state = None
            self.state.update(self)

    def draw(self):
        self.state.draw(self)
######################
######################

App()
