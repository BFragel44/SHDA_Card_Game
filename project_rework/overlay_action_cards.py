import pyxel
import ui
import shda_marines as sm

# Action types:
# ----------------
# ----------------
# 1. SUPPORT CARD
# ----------------
#   a. [Gain a Support Token, to be placed on any Marine] + [Execute text of card]
#   b. limited to a single Support Token per Team
#   c. support card TEAM ABILITES:
#       RED = AFTER EVENT PHASE Each time a Support Card is played, the Team gains a Support Token.
#       GREEN = Each time GIDEON rolls SKULL while DEFENDING, attack misses.
#       GREY = After Support Token resolved, pick swarm, they cannot attack or be killed this turn.
# TODO - support card TEAM ABILITES need to be implemented/added

# 2. MOVE + ACTIVATE CARD
# ----------------
# Moves MAY be executed in following order:
#   a. MOVE TO ADJACENT (swap with adjacent Marine, above or below)
#   b. CHANGE FACING (flip to face left or right)
#   c. ACTIVATE TERRAIN FACING A TEAM MEMBER
#       - Resolve facing Terrain's "Activate" text).
#       - a Terrain Card cannot be activated more than once per round.

# 3. ATTACK CARDS
# ----------------
#   a. Choose Marine (any order): Must be facing target & IN RANGE per card
#       Range 0 = Directly-facing only.
#       Range 1 = Directly-facing or facing adjacent Marines.
#       Range 2 = Directly-facing or facing Marines up to 2 away up/down The Column
#       Range 3 = 3 spaces away

#   b. Roll Die
#       Skull = Kill (discard 1 GS from the targeted swarm to GS Discard Pile).
#       Any other result = Miss/No impact 
#           Note: If a Marine has Support Tokens, they may be spent 1 per re-roll and reattempt to roll an attack. 

# Action Cards remain selected until end of NEXT Chose Actions phase (cannot use same action twice in a row).


# ACTION RESOLUTION PHASE
# ----------------
# ----------------
#   - All Action Cards are played, starting with the lowest numbered card
#   - Action Special Abilities: Ignore facing, except for Attacking or spending Support Token to re-roll. 
#   - Abilities that say “each time” may be used multiple times per round.

# CARD_NUM: (CARD_ID, CARD_TYPE)
##### card_dict = {1: (8, 'attack_card'), 
#                  8: (3, 'support_card'), 
#                 17: (13,'move_act_card')}
class ResolveActionUI():
    def __init__(self, selected_action_cards, space_marines, location_and_spawns):
        self.selected_action_cards = selected_action_cards
        self.action_cards = iter(selected_action_cards)
        self.space_marines = space_marines
        self.location_and_spawns = location_and_spawns
        self.click_phase = 0
        # self.roll_screen = RollScreen() # <- needs to be built
        self.current_card = None
        self.move_card = None

    def update(self):
        if self.click_phase == 0:
            if ui.phase_box_click():
                # Get the next element of self.action_cards
                try:
                    self.current_card = next(self.action_cards)
                    self.click_phase = 1
                except StopIteration:
                    pass
                    # if no more elements in self.action_cards
                    # GENESTEALER ATTACK PHASE activation here       
        elif self.click_phase == 1:
            self.card_info = self.selected_action_cards.get(self.current_card)
            #  (3, 'support_card')
            if self.card_info[1] == 'support_card':
                self.support_card(self.card_info[0])

            elif self.card_info[1] == 'move_act_card':
                if not self.move_card:
                    self.move_card = MovementCard(self.card_info[0], self.space_marines)
                elif self.move_card:
                    self.move_card.update()

            elif self.card_info[1] == 'attack_card':
                self.attack_card(self.card_info[0])

    def support_card(self, card_info): # TODO do I need card_info here?
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive':
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']-1]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                # if box is clicked, add a support token to the marine
                if ui.box_click(box_x, box_y, box_w, box_h):
                    marine['support_tokens'] += 1
                    self.click_phase = 0

    def support_card_draw(self):
        for marines in self.space_marines.combat_teams:
            if marines['status'] == 'alive':
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][marines['formation_num'] - 1]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
###                          ###
### MAIN OVERLAY DRAW METHOD ###
###                          ###
    def overlay_draw(self):
        if self.click_phase == 1 and not self.move_card:
            self.support_card_draw()
        elif self.click_phase == 1 and self.move_card:
            self.move_card.draw()


###                          ###
###    MOVEMENT CLASS WIP    ###
###                          ###
class MovementCard():
    def __init__(self, card_info, space_marines):
        self.space_marines = space_marines
        self.card_info = card_info
        self.movement_phase = 1
        self.movement_team = []
        self.move_click = 0
        self.selected_move = None
        self.up_move = None
        self.down_move = None
# UPDATE METHODS---
    def available_moves_update(self, card_info):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']-1]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                if marine['formation_num'] not in self.movement_team:
                    self.movement_team.append(marine['formation_num'])
                # if box is clicked, move to the next MOVEMENT PHASE w/ the selected marine
                if self.movement_team:
                    if ui.box_click(box_x, box_y, box_w, box_h):
                        self.selected_move = marine['formation_num']
                        self.move_click = 1

    def move_selection_update(self):
        print("stay test")
        if self.up_move:
            if ui.box_click(self.up_move[0], 
                            self.up_move[1], 
                            self.up_move[2], 
                            self.up_move[3]):
                print("place move(up) method here move type should be -1")
                self.move_action("up", self.up_move[4])
                pyxel.flip()
        if self.down_move:
            if ui.box_click(self.down_move[0], 
                            self.down_move[1], 
                            self.down_move[2], 
                            self.down_move[3]):
                print("place move(down) method here move type should be 1")
                self.move_action("down", self.down_move[4])
                pyxel.flip()

    def move_action(self, move_type, formation_num):
        # move_dir = 0
        if move_type == "up":
            move_dir = -1
        elif move_type == "down":
            move_dir = 1
        # get the selected marine's formation number
        for marine in self.space_marines.combat_teams:
            if marine['formation_num'] == formation_num:
                print("selected marine:", marine['formation_num'])
                print(formation_num)
                # selected marine:
                marine.update({'formation_num': formation_num + move_dir})
                print(marine)
                # adjacent marine above/below the selected marine:
                if marine['formation_num'] == formation_num + move_dir:
                    marine['formation_num'] = formation_num

            # get the marine above the selected marine
            # swap the selected marine with the marine above
            pass
        # get the marine above/below the selected marine based on move_type
        # swap the selected marine with the marine above/below
        pass

# DRAW METHODS---
    def available_moves_draw(self, card_info):
        sm.Space_marines.formation_draw(self.space_marines)
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][marine['formation_num'] - 1]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
    
    def move_selection_draw(self):
        for marine in self.space_marines.combat_teams:
            # selected marine card is highlighted:
            if marine['status'] == 'alive' and marine['formation_num'] == self.selected_move:
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][self.selected_move - 1]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
                # check if the marine is at the top or bottom 
                # of formation for move up/down options
                # UP LIMIT CHECK:
                if self.selected_move-1 > 0:
                    # sets up the click-box for the "up" move:
                    self.up_move = [
                        sm.sm_visual_dimms["card_border_x"],
                        sm.sm_visual_dimms["card_border_y"][self.selected_move-1],
                        sm.sm_visual_dimms["card_border_w"],
                        sm.sm_visual_dimms["card_border_h"]-22,
                        marine['formation_num']] # last value is the formation number
                    # click-box on top of selected marine's portrait for "up" move:
                    pyxel.rectb(self.up_move[0], self.up_move[1],
                                self.up_move[2], self.up_move[3], 8)
                # Highlight the formation place above the selected marine:
                    pyxel.rectb(
                    sm.sm_visual_dimms["card_border_x"]-2,
                    sm.sm_visual_dimms["card_border_y"][self.selected_move-2]-2,
                    sm.sm_visual_dimms["card_border_w"]+4,
                    sm.sm_visual_dimms["card_border_h"]+4,
                    13)
                # DOWN LIMIT CHECK:
                if self.selected_move-1 < 5:
                    # sets up the click-box for the "down" move:
                    self.down_move = [
                        sm.sm_visual_dimms["card_border_x"],
                        sm.sm_visual_dimms["card_border_y"][self.selected_move-1]+22,
                        sm.sm_visual_dimms["card_border_w"],
                        sm.sm_visual_dimms["card_border_h"]-22,
                        marine['formation_num']] # last value is the formation number
                    # click-box on bottom of selected marine's portrait for "down" move:
                    pyxel.rectb(self.down_move[0], self.down_move[1], 
                                self.down_move[2], self.down_move[3], 8)

                # Highlight the formation place below the selected marine:
                    pyxel.rectb(
                    sm.sm_visual_dimms["card_border_x"]-2,
                    sm.sm_visual_dimms["card_border_y"][self.selected_move]-2,
                    sm.sm_visual_dimms["card_border_w"]+4,
                    sm.sm_visual_dimms["card_border_h"]+4,
                    13)
# card_border_x = 96 40 65 33
# card_border_y = [40, 65, 90, 115, 140, 165]
# card_border_w = 65
# card_border_h = 25                    

###
###  MovementCard MAIN Class Methods  
###
    def update(self):
        if self.move_click == 0:
            self.available_moves_update(self.card_info)
        elif self.move_click == 1:
                self.move_selection_update()

    def draw(self):
        if self.move_click == 0:
            self.available_moves_draw(self.card_info)
        elif self.move_click == 1:
            self.move_selection_draw()

# self.click_phase = 0 hold off on this until the whole team's movement
#   action is resolved.
