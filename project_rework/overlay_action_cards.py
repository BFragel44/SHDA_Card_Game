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
                self.move_card(self.card_info[0])

            elif self.card_info[1] == 'attack_card':
                self.attack_card(self.card_info[0])

    def support_card(self, card_info):
        for marines in self.space_marines.combat_teams:
            if marines['status'] == 'alive':
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marines['formation_num']-1]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                # if box is clicked, add a support token to the marine
                if ui.box_click(box_x, box_y, box_w, box_h):
                    marines['support_tokens'] += 1
                    self.click_phase = 0
                else:
                    continue

    def support_card_draw(self):
        for marines in self.space_marines.combat_teams:
            if marines['status'] == 'alive':
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][marines['formation_num'] - 1]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)

    def move_card(self, card_info):
        self.click_phase = 2
        for marines in self.space_marines.combat_teams:
            print("marines['team_color'] = ", marines['team_color'])
            print("card_info: ", card_info)
            if marines['status'] == 'alive' and marines['team_color'] == card_info:
                print("match!!!")
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marines['formation_num']-1]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                # if box is clicked, add a support token to the marine
                if ui.box_click(box_x, box_y, box_w, box_h):
                    print("click phase 2")
                    print(marines['sm_name'])
                    self.click_phase = 0

    def move_card_draw(self, card_info):
        for marines in self.space_marines.combat_teams:
            if marines['status'] == 'alive' and marines['team_color'] == card_info[0]:
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
        if self.click_phase == 1:
            self.support_card_draw()
        
        elif self.click_phase == 2:
            self.move_card_draw(self.card_info)
