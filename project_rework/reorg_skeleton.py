import pyxel
import action_cards as ac
import shda_marines as sm
import Genestealers as gs
import locations
import event_cards as ec

# SCREEN DIMENSIONS
SCREEN_X = 257
SCREEN_Y = 257

# TEAM COLORS
GREY = 13
GREEN = 3
RED = 8

location_and_spawns = locations.Location_and_spawns(gs.gs_deck_create)
event_cards = ec.Event_cards(ec.event_deck)
drawn_event_card = event_cards.draw_card()
location_and_spawns.populate_blips()
initial_spawns = location_and_spawns.gs_spawn_locs(drawn_event_card)
location_and_spawns.populate_GS_spawns(initial_spawns)


class GameState:
    def __init__(self):
        self.next_state = None
        self.prev_state = None

    def back(self):
        self.next_state = self.prev_state
        self.prev_state = None


class MainMenuState(GameState):
    def __init__(self):
        super().__init__()
        pyxel.playm(0,loop=True)
        
    def update(self, game):
        # Check for input to start a new game
        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.stop()
            self.next_state = GameBoardState()

    def draw(self, game):
        # Draw the main menu screen
        pyxel.cls(0)
        pyxel.text(SCREEN_X//2 - 16, (SCREEN_Y//2) - 12, 
                   "Space Hulk", 3)
        pyxel.text(SCREEN_X//2 - 18, (SCREEN_Y//2), 
                   "Death Angel", 6)
        pyxel.text(SCREEN_X//2 - 36, (SCREEN_Y//2) + 36, 
                   "Press ENTER to start", 6)


class GameBoardState(GameState):
    def __init__(self):
        super().__init__()
        # INITIAL sm PLACEMENT
        self.space_marines = sm.Space_marines()

    def update(self, game):
# Next State
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.next_state = SelectActionState()
# Previous State
        if pyxel.btnp(pyxel.KEY_T):
            pyxel.cls(0)
            pyxel.playm(0,loop=True)
            self.back()

    def draw(self, game):
        # Draw the main game screen
        pyxel.cls(0)
        location_and_spawns._draw()
        for roster_dict in sm.combat_teams:
            y_val = roster_dict["formation_num"]
            col = roster_dict["team_color"]
            sm_face = roster_dict["visual"]
            sm_name = roster_dict["sm_name"].split(" ")
            single_y = sm.sm_visual_dimms["arrow_y"][y_val - 1]
            # sm card border
            pyxel.rectb(sm.sm_visual_dimms["card_border_x"],
                        sm.sm_visual_dimms["card_border_y"][y_val - 1],
                        sm.sm_visual_dimms["card_border_w"],
                        sm.sm_visual_dimms["card_border_h"],
                        col,)
            
            # sm portrait
            pyxel.blt(sm.sm_visual_dimms["portrait_x"] + 1,
                        sm.sm_visual_dimms["portrait_y"][y_val - 1],
                        0, sm_face[0], sm_face[1], 15, 16,)
            # sm portrait border
            pyxel.rectb(sm.sm_visual_dimms["portrait_x"],
                        sm.sm_visual_dimms["portrait_y"][y_val - 1], 
                        17, 17, col)
            # SM name 1
            pyxel.text(sm.sm_visual_dimms["name_x"],
                       sm.sm_visual_dimms["name_y"][y_val - 1],
                       f"{sm_name[0]}", col)
            # SM name 2
            pyxel.text(sm.sm_visual_dimms["name_x"] - 2,
                       sm.sm_visual_dimms["name_y"][y_val - 1] + 6, 
                       f"{sm_name[1]}", col)
            # sm facing arrows
            y_arrow_list = [single_y, single_y + 7, single_y + 14]
            if roster_dict["facing"] == "LEFT":
                for y_val in y_arrow_list:
                    pyxel.blt(sm.sm_visual_dimms["left_arrow_x"], y_val, 0, 0, 32, 6, 6)
            else:
                for y_val in y_arrow_list:
                    pyxel.blt(sm.sm_visual_dimms["right_arrow_x"], y_val, 0, 10, 32, 6, 6)
            # if ac_selection:

            #     # card border
            #     pyxel.rectb(sm.sm_visual_dimms["card_border_x"] + 1,
            #                 sm.sm_visual_dimms["card_border_y"][y_val - 1] - 1,
            #                 sm.sm_visual_dimms["card_border_w"] + 1,
            #                 sm.sm_visual_dimms["card_border_h"] + 1,
            #                 9)


class SelectActionState(GameState):
    def __init__(self):
        super().__init__()
        self.action_cards = ac.Action_cards()

    def update(self, game):
        # Check for input to select an action card
        if pyxel.btnp(pyxel.KEY_1):
            # Select the first action card and transition back to the battle state
            self.next_state = GameBoardState()

    def draw(self, game):
        # Draw the action card selection screen
        pyxel.cls(0)
        pyxel.text(20,20,"Action State", 3)


class App:
    def __init__(self):
        pyxel.init(SCREEN_X, SCREEN_Y, title="SPACE HULK: DEATH ANGEL", fps=30)
        pyxel.load("sh_da.pyxres")
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


App()
