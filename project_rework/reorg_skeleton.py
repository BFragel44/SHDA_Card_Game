import pyxel
import action_cards as ac
import shda_marines as sm
import Genestealers as gs
import locations as loc
import event_cards as ec
import overlay_action_cards as oac

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
        self.space_marines._draw()
        
class SelectActionState(GameState):
    def __init__(self):
        super().__init__()
        self.action_cards = ac.Action_cards()

    def update(self, game):
        # Check for input to select an action card
        self.action_cards.update()    
        if self.action_cards.sorted_cards:
        # Checks if action cards are selected, sends them to GameState & switches back to MainGameScreen
            action_card_choices = self.action_cards.sorted_cards
            self.next_state = ResolveActionState(action_card_choices)

    def draw(self, game):
        # Draw the action card selection screen
        pyxel.cls(0)
        self.action_cards._draw()

class ResolveActionState(GameState):
    def __init__(self, action_card_choices):
        super().__init__()
        self.action_overlay = oac.ActionOverlay()
        self.ac_choices = action_card_choices
        # acards = {1: (8, 'attack_card'), 8: (3, 'support_card'), 17: (13, 'move_act_card')}
        self.ac_count = 1
        self.action_list = [a for a, v in self.ac_choices.items()]
        self.sm = sm.combat_teams
        self.current_card = None
        self.marine_selectors = False
        self.cardtype = None
        self.cardteam = None
        self.sm_list = []
        self.gs_list = []
        self.sm_choice = 0
        self.gs_choice = 0
        self.opponents = {}
        self.direction = None
        self.atk_package = None
        self.phase_one = False
        self.phase_two = False

    def update(self, game):
        # action_list = [a for a, v in self.ac_choices.items()]
        if not self.marine_selectors:
# Activates if "Enter" pressed and no current_card and there is a action_list
            if self.current_card == None and self.action_list and pyxel.btnp(pyxel.KEY_RETURN):
# self.current_card = None # resets the ability to press enter
                self.cardtype = self.ac_choices.get(self.action_list[self.ac_count-1])[1]
                self.cardteam = self.ac_choices.get(self.action_list[self.ac_count-1])[0]
                self.current_card = self.action_list.pop(0)
                # int of action card number, 1st element from action_list
                if self.cardtype != None:
# Starts up the self.marine_selectors section of update()
                    self.marine_selectors = True

        if self.marine_selectors:
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.cardtype == "attack_card":
                    self.attack_selectors(self.cardteam)
                    self.marine_selectors = False
########
        if self.atk_package:
            if self.phase_one:
                print("up-down self.sm_list = ", self.sm_list)
                print("up-down self.sm_choice = ", self.sm_choice)
                print("len(self.sm_list) = ", len(self.sm_list))

# TODO FIX up and down selections no longer working
                if len(self.atk_package) == 2:
                    if pyxel.btnp(pyxel.KEY_W) and self.sm_choice > 0:
                        self.sm_choice -= 1

                    if pyxel.btnp(pyxel.KEY_S) and self.sm_choice < len(self.sm_list) - 1:
                        self.sm_choice += 1

                if pyxel.btnp(pyxel.KEY_F):
                    self.opponents['attacker'] = self.sm_list[self.sm_choice]
                    # dict_items([('LEFT', {3: [2]}), ('RIGHT', {6: [2]})])
                    for facing, val_dict in self.atk_package.items():
# TODO removed +1 from self.opponents['attacker'] to fix problem area #1 (may cause issues later)
                        if self.opponents['attacker'] in val_dict:
                            self.direction = facing
                            self.phase_two = True
                            self.phase_one = False
# if F is pressed: 
# the selected SM is labeled as the 'attacker' in self.opponents
# if the 'attacker' is a key in the val_dict (from atk_package)
# self.direction is given the facing
# phase_one is DEACTIVATED
# phase_two is ACTIVATED
                            self.marine_selectors = False # resets marine_selectors
                            self.current_card = None      # resets the ability to press enter
                            self.sm_choice = 0
# TODO may need to place the above vars at the end of phase_two
            if self.phase_two:
                print("self.gs_list = ", self.gs_list)
                if pyxel.btnp(pyxel.KEY_UP) and self.gs_choice > 0:
                    self.gs_choice -= 1

                if pyxel.btnp(pyxel.KEY_DOWN) and self.gs_choice < len(self.gs_list) - 1:
                    self.gs_choice += 1

                if pyxel.btnp(pyxel.KEY_F):
                    print("Phase 2, F Key PRESSED")
                    self.defGs_info_sort()

                    print("self.opponents =", self.opponents)
                    print("gs_list =", self.gs_list)
                    print("gs_choice =", self.gs_choice)
                    if self.gs_choice < len(self.gs_list):
                        self.opponents.update({'defender': self.gs_list[self.gs_choice]})
                    print("self.opponents['defender'] = ", self.opponents['defender'])
                    self.sm_list = []
                    self.phase_two = False
# TODO will need to edit this so the 3rd card can be played     
        if not self.action_list:
            self.next_state = MainMenuState()
     
    def attack_selectors(self, cardteam):
        print("attack card")
        lgs = location_and_spawns.spawned_left_swarms
        rgs = location_and_spawns.spawned_right_swarms
        attacking_marines = [s for s in self.sm if s["team_color"] == cardteam]
# TODO returns list of enemies in range (PROBABLY WHY EVERYTHING IS BROKEN):
        attack_values = space_marines.attack_prep(attacking_marines, lgs, rgs)
        self.space_marines.atk_info_sort(attack_values)
        
        for side, pairings in attack_values.items():
            for sm_pairing, gs_pairing in pairings.items():
                self.sm_list.append(sm_pairing)
        self.sm_list.sort()
        self.phase_one = True
        self.atk_package = attack_values
        print(f"self.atk_package = {self.atk_package}")


    def defGs_info_sort(self):
        print(self.atk_package)

        for facing, sm_gs_pairing in self.atk_package.items(): # facing = LEFT, sm_gs_pairing = {2: [2]}
            for marine, in_range_list in sm_gs_pairing.items():
                print("marine =", marine, "vs_list =", in_range_list)
                for gs_listing in in_range_list:
                    print("self.sm_list = ", self.sm_list)
                    print("gs_listing = ", gs_listing)
                    print("self.sm_choice = ", self.sm_choice)
                    print("self.opponents['attacker'] = ", self.opponents['attacker'])
                    if self.sm_list[self.sm_choice] == self.opponents['attacker']:
                        self.gs_list.append(gs_listing)
                        print("appended!")
                        print(f"self.gs_list = {self.gs_list}")
# TODO need to find out why the values above are not matching up -- different if left/right facing?
                    else:
                        print("not appended!")
                        print("self.sm_list[self.sm_choice] != self.opponents['attacker']")


    def draw(self, game):
        pyxel.cls(0)
        self.space_marines._draw()
        location_and_spawns._draw()
        card_border_x = 96
        card_border_y = (40, 76, 112, 148, 184, 220)
        card_border_w = 65
        card_border_h = 33
# atk_package() DRAW
        if self.atk_package:
            gs_left_x = 5
            gs_right_x = 183

            if self.phase_one:
                selection = self.sm_list[self.sm_choice] - 1
                # marine current card
                pyxel.rectb(card_border_x - 2,
                            card_border_y[selection] - 2,
                            card_border_w + 4,
                            card_border_h + 4, 9)

            elif self.phase_two:
                # selected marines
                print("PHASE 2 IN DRAW")
                pyxel.rectb(card_border_x - 2,
                    card_border_y[self.sm_list[self.sm_choice]] - 2,
                    card_border_w + 4,
                    card_border_h + 4, 13)
                print("self.direction = ", self.direction)
                if self.direction == "LEFT":
                    selection = self.gs_list[self.gs_choice]
                    # gs
                    pyxel.rectb(gs_left_x,
                        card_border_y[selection] - 2,
                        card_border_w + 4,
                        card_border_h + 4, 9)

                elif self.direction == 'RIGHT':
                    # gs
                    pyxel.rectb(gs_right_x,
                        card_border_y[self.gs_list[self.gs_choice]] - 2,
                        card_border_w + 4,
                        card_border_h + 4, 9)
                else:
                    pyxel.rect(SCREEN_X/2-25, SCREEN_Y/2-30, 50, 15, 8)
                    pyxel.text(SCREEN_X/2-24, SCREEN_Y/2-25, "No Valid ATK", 7)

######################
######################
class App:
    def __init__(self):
        pyxel.init(SCREEN_X, SCREEN_Y, title="SPACE HULK: DEATH ANGEL", fps=30)
        pyxel.load("project_rework\sh_da.pyxres")
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
