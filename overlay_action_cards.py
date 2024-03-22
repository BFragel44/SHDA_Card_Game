import pyxel
import ui
import shda_marines as sm

# Action types:
# ----------------
# ----------------
# TODO - add in text description of current action on location box
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
# TODO - build and implement TERRAIN ACTIVATION for this card type
# TODO - FIX: this card sometimes breaks when skipping certain parts of it.

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
# TODO add in space marine powers to attack rolls (aka Brother Leon able to attack 3x)


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
        self.current_card = None
        self.move_card = None
        self.attack_card = None
        self.current_card_type = None
        self.phase_resolved = False

    def update(self):
        if self.click_phase == 0:
            if ui.phase_box_click():
                # Get the next element of self.action_cards
                try:
                    self.current_card = next(self.action_cards)
                    self.click_phase = 1
                # if no more self.action_cards, NEXT PHASE activation
                except StopIteration:
                    self.phase_resolved = True       
        elif self.click_phase == 1:
            self.card_info = self.selected_action_cards.get(self.current_card)
            #  (3, 'support_card')
            if self.card_info[1] == 'support_card':
                self.current_card_type = 'sc'
                self.support_card()

            elif self.card_info[1] == 'move_act_card':
                if not self.move_card:
                    self.move_card = MovementCard(self.card_info[0], self.space_marines, 
                                                  self.location_and_spawns.room_terrain)
                elif self.move_card:
                    self.current_card_type = 'mc'
                    self.move_card.update()
                    if self.move_card.card_resolved:
                        self.click_phase = 0
                        self.move_card = None
            
            elif self.card_info[1] == 'attack_card':
                if not self.attack_card:
                    self.attack_card = AttackCard(self.card_info[0], self.space_marines, 
                                                  self.location_and_spawns.spawned_left_swarms,
                                                  self.location_and_spawns.spawned_right_swarms)
                elif self.attack_card:
                    self.current_card_type = 'ac'
                    self.attack_card.update()
                    if self.attack_card.card_resolved:
                        self.click_phase = 0
                        self.attack_card = None

    def support_card(self):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive':
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']]
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
                sm.sm_visual_dimms["card_border_y"][marines['formation_num']]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
###                          ###
### MAIN OVERLAY DRAW METHOD ###
###                          ###
    def overlay_draw(self):
        if self.click_phase == 1 and self.current_card_type == 'sc':
            self.support_card_draw()
        elif self.click_phase == 1 and self.current_card_type == 'mc':
            if self.move_card is not None:
                self.move_card.draw()
            else:
                print("Error: move_card is None")
        elif self.click_phase == 1 and self.current_card_type == 'ac':
            if self.attack_card is not None:
                self.attack_card.draw()
            else:
                print("Error: attack_card is None")

###                          ###
###    MOVEMENT CLASS        ###
###                          ###
class MovementCard():
    def __init__(self, card_info, space_marines, terrain_locations):
        self.space_marines = space_marines
        self.terrain_locations = terrain_locations
        self.card_info = card_info
        self.movement_phase = 1
        self.movement_team = []
        self.move_click = 0
        self.selected_move = None
        self.up_move = None
        self.down_move = None
        self.move_used = []
        self.activatable_terrain = None
        self.terrain_side = None
        self.card_resolved = False

    # UPDATE METHODS---
    def reset_selection(self):
        self.movement_team = []
        self.move_used = []
        for marine in self.space_marines.combat_teams:
            marine['selected'] = False

    def available_moves_update(self, card_info):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                if not marine.get('selected', False):
                    self.movement_team.append(marine['formation_num'])
                    # Mark marine as selected:
                    marine['selected'] = True
                # if box is clicked, move to the next MOVEMENT PHASE w/ the selected marine
                if marine['formation_num'] in self.movement_team and ui.box_click(box_x, box_y, box_w, box_h):
                    self.selected_move = marine['formation_num']
                    self.move_click = 1
    
    def skip_button_update(self):
        if ui.box_click(220, 4, 30, 10):
            if self.move_click == 0:
                self.move_click = 2
            elif self.move_click == 2:
                self.move_click = 4
            elif self.move_click == 4:
                pass
            self.reset_selection()

    def skip_button_draw(self):
        pyxel.rectb(220, 4, 30, 10, 7)
        pyxel.text(225, 6, "SKIP", 7)

    def move_selection_update(self):
        if self.up_move:
            if ui.box_click(self.up_move[0], 
                            self.up_move[1], 
                            self.up_move[2], 
                            self.up_move[3]):
                self.move_action("up", self.up_move[4])

        if self.down_move:
            if ui.box_click(self.down_move[0], 
                            self.down_move[1], 
                            self.down_move[2], 
                            self.down_move[3]):
                self.move_action("down", self.down_move[4])


    def move_action(self, move_type, formation_num):
        if move_type == "up":
            move_dir = -1
        elif move_type == "down":
            move_dir = 1
        # get the selected marine's formation number
        move_value = formation_num + move_dir
        selected_marine = None
        next_marine = None
        for marine in self.space_marines.combat_teams:
            if marine['formation_num'] == formation_num:
                selected_marine = marine
            elif marine['formation_num'] == move_value:
                next_marine = marine
        if selected_marine and next_marine:
            # Swap formation numbers
            selected_marine['formation_num'], next_marine['formation_num'] = next_marine['formation_num'], selected_marine['formation_num']
            # add clicked marine to the move_used list
            remove_index = self.movement_team.index(self.selected_move)
            remove_choice = self.movement_team.pop(remove_index)
            self.move_used.append(remove_choice)
            # reset the move_click to 0
            self.move_click = 0
        # sends update and draw into the "change facing" phase
        if len(self.move_used) == 2:
            self.move_click = 2
            self.reset_selection()

    def available_flip_update(self, card_info):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                box_x = sm.sm_visual_dimms["card_border_x"]
                box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']]
                box_w = sm.sm_visual_dimms["card_border_w"]
                box_h = sm.sm_visual_dimms["card_border_h"]
                if not marine.get('selected', False):
                    self.movement_team.append(marine['formation_num'])
                    # Mark marine as selected:
                    marine['selected'] = True
                # if box is clicked, move to the next MOVEMENT PHASE w/ the selected marine
                if marine['formation_num'] in self.movement_team and ui.box_click(box_x, box_y, box_w, box_h):
                    self.selected_move = marine['formation_num']
                    self.move_click = 3
    
    def flip_selection_update(self):
        self.space_marines.flip_facing(self.selected_move)
        remove_index = self.movement_team.index(self.selected_move)
        remove_choice = self.movement_team.pop(remove_index)
        self.move_used.append(remove_choice)
        if len(self.move_used) == 2:
            self.move_click = 4
            self.reset_selection()
        else:
            self.move_click = 2

    def available_activate_update(self, card_info):
        for terrain in self.terrain_locations:
            # 1. check if the terrain is door or control_panel
            if terrain[0] == 'door' or terrain[0] == 'control_panel':
                self.activatable_terrain = terrain
                terrain_index = self.terrain_locations.index(terrain)
                # 2. check if the terrain is on the left or right side of the room
                if terrain_index == 0 or terrain_index == 1:
                    self.terrain_side = "LEFT"
                elif terrain_index == 2 or terrain_index == 3:
                    self.terrain_side = "RIGHT"
                    terrain_index = 6 - terrain_index
        # 3. check if the selected marine is facing the terrain
        for marine in self.space_marines.combat_teams:
            if marine['facing'] == self.terrain_side and marine['team_color'] == card_info:
                if marine['formation_num'] == terrain_index:
                    if marine['support_tokens'] > 0:
                        # will need to add the activation function/method here
                        box_x = sm.sm_visual_dimms["card_border_x"]
                        box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']]
                        box_w = sm.sm_visual_dimms["card_border_w"]
                        box_h = sm.sm_visual_dimms["card_border_h"]
                        if marine['selected'] != False:
                            self.movement_team.append(marine['formation_num'])
                            # Mark marine as selected:
                            marine['selected'] = True
                        # if box is clicked, move to the next MOVEMENT PHASE w/ the selected marine
                        if ui.box_click(box_x, box_y, box_w, box_h):
                            self.selected_move = marine['formation_num']
                            self.move_click = 5
        else:
            self.move_click = 5
        

# DRAW METHODS---
    def available_moves_draw(self, card_info):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][marine['formation_num']]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
    
    def move_selection_draw(self):
        for marine in self.space_marines.combat_teams:
            # selected marine card is highlighted:
            if marine['status'] == 'alive' and marine['formation_num'] == self.selected_move:
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][self.selected_move]-2,
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
                        sm.sm_visual_dimms["card_border_y"][self.selected_move],
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
                        sm.sm_visual_dimms["card_border_y"][self.selected_move]+22,
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


    def available_flips_draw(self, card_info):
        for marine in self.space_marines.combat_teams:
            if marine['status'] == 'alive' and marine['team_color'] == card_info:
                if marine['formation_num'] in self.movement_team:
                    pyxel.rectb(
                    sm.sm_visual_dimms["card_border_x"]-2,
                    sm.sm_visual_dimms["card_border_y"][marine['formation_num']]-2,
                    sm.sm_visual_dimms["card_border_w"]+4,
                    sm.sm_visual_dimms["card_border_h"]+4,
                    9)

# card_border_x = 96 40 65 33
# card_border_y = [40, 65, 90, 115, 140, 165]
# card_border_w = 65
# card_border_h = 25                    

###
###  MovementCard MAIN Class Methods  
###
    def update(self):
        self.skip_button_update()
        if self.move_click == 0:
            self.available_moves_update(self.card_info)
        elif self.move_click == 1:
            self.move_selection_update()
        elif self.move_click == 2:
            self.available_flip_update(self.card_info)
        elif self.move_click == 3:
            self.flip_selection_update()
        elif self.move_click == 4:
            self.available_activate_update(self.card_info)
        elif self.move_click == 5:
            self.card_resolved = True

    def draw(self):
        self.skip_button_draw()
        if self.move_click == 0:
            self.available_moves_draw(self.card_info)
        elif self.move_click == 1:
            self.move_selection_draw()
        elif self.move_click == 2 or self.move_click == 3:
            self.available_flips_draw(self.card_info)

          
class AttackCard():
    def __init__(self, card_info, space_marines, left_gs, right_gs):
        self.left_gs = left_gs
        self.right_gs = right_gs
        self.attack_click = 0
        self.card_info = card_info
        self.gs_facing_match = []
        self.roll_screen = None
        self.space_marines = space_marines
        for marine in self.space_marines.combat_teams:
            marine['attack_used'] = False
        self.available_marines = []
        self.initial_length = None
        self.card_resolved = False
        

###                            ###
### ATTACK CARD UPDATE METHODS ###
###                            ###
    def available_sm_update(self):
        if not self.available_marines:
            self.available_marines = [marine for marine in self.space_marines.combat_teams 
                                      if marine['attack_used'] == False and 
                                      marine['team_color'] == self.card_info]
        
            self.initial_length = len(self.available_marines)
        
        # Check if self.available_marines is empty after it has been populated
        if len(self.available_marines) == 0 and self.initial_length == 0:
            pyxel.cls(0)
            self.attack_click = 3

        for marine in self.available_marines:
            box_x = sm.sm_visual_dimms["card_border_x"]
            box_y = sm.sm_visual_dimms["card_border_y"][marine['formation_num']]
            box_w = sm.sm_visual_dimms["card_border_w"]
            box_h = sm.sm_visual_dimms["card_border_h"]
            if ui.box_click(box_x, box_y, box_w, box_h):
                self.attacker_choice = [marine['formation_num'],
                                        marine['facing'],
                                        marine['attk_range'],
                                        marine['support_tokens']]
                self.attack_click = 1
        

    def sm_gs_selection_update(self):
        gs_side = None
        if self.attacker_choice[1] == 'LEFT':
            gs_side = self.left_gs
        elif self.attacker_choice[1] == 'RIGHT':
            gs_side = self.right_gs
        for key, value in gs_side.items():
            if value['g_stealers']:
                attack_info = [self.attacker_choice[1], key, 
                                len(value['g_stealers'])]
                if attack_info not in self.gs_facing_match:
                    self.gs_facing_match.append(attack_info)

    def in_range_check_update(self, gs_formation):
        # self.attacker_choice = [marine['formation_num'],
        #                                 marine['facing'],
        #                                 marine['attk_range']]
        lo_range = self.attacker_choice[0] - self.attacker_choice[2]
        if lo_range < 0:
            lo_range = 0   
        hi_range = self.attacker_choice[0] + self.attacker_choice[2]
        if hi_range > 5:
            hi_range = 5
        if gs_formation in range(lo_range, hi_range+1):
            return True
        return False

    ###                            ###
    ### ATTACK CARD DRAW METHODS   ###
    ###                            ###
    def available_sm_draw(self):
        for marine in self.space_marines.combat_teams:

            if marine['attack_used'] == False and marine['team_color'] == self.card_info:
                pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][marine['formation_num']]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)

    def gs_kill(self, gs_side, gs_formation, gs_swarm_num):
        left_or_right = None
        if gs_side == 'LEFT':
            left_or_right = self.left_gs
        else:
            left_or_right = self.right_gs
        left_or_right[gs_formation]['g_stealers'].pop(gs_swarm_num)
        self.gs_facing_match = [gs for gs in self.gs_facing_match if 
                                not (gs[0] == gs_side and gs[1] == gs_formation)]

    def sm_gs_selection_draw(self):
        # X COORDINATES FOR LEFT SIDE GS PORTRAITS, R to L
        gs_left_x = (52, 35, 18, 1)
        # X COORDINATES FOR RIGHT SIDE GS PORTRAITS, L to R
        gs_right_x = (188, 205, 222, 239)
        # Y COORDINATES FOR ALL GS IMAGES, TOP TO BOTTOM
        gs_img_y = (40, 76, 112, 148, 184, 220)
        if self.gs_facing_match:
            # self.gs_facing_match = [['RIGHT', 3, 2]] 
            #                         [FACING, GS_FORMATION_NUM, GS_COUNT]
            # Selected Marine's card is highlighted:
            pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][self.attacker_choice[0]]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
            for gs in self.gs_facing_match:
                if self.in_range_check_update(gs[1]):
                    if gs[0] == 'LEFT':
                        gs_x = gs_left_x
                        gs_y = gs[1]
                    elif gs[0] == 'RIGHT':
                        gs_x = gs_right_x
                        gs_y = 6 - gs[1]
                    for n in range(gs[2]):
                        pyxel.rectb(
                            gs_x[n], 
                            gs_img_y[gs_y], 
                            16, 32, 8)
                        if ui.box_click(gs_x[n], 
                                        gs_img_y[gs_y], 
                                        16, 32):
                            self.attack_click = 2
                            self.roll_screen = ui.RollScreen(gs[0], 
                                                             self.attacker_choice[0],
                                                             self.attacker_choice[3],
                                                             gs[1], 
                                                             n)
        # else:
        #     print("NO GS FACING MATCH")


    ###                               ###
    ### MAIN AttackCard Class Methods ###
    ###                               ###
    def update(self):
        if self.attack_click == 0:
            self.available_sm_update()
        elif self.attack_click == 1:
            self.sm_gs_selection_update()
        elif self.attack_click == 2:
            self.roll_screen.screen_update()
        elif self.attack_click == 3:
            self.card_resolved = True

        if self.roll_screen and self.attack_click != 0:
            if self.roll_screen.dice.roll_phase == 5:
                # removes the sm from the available attackers
                for marine in self.space_marines.combat_teams:
                        if marine['formation_num'] == self.attacker_choice[0]:
                            marine['attack_used'] = True
                if self.roll_screen.gs_hit:
                    self.gs_kill(self.attacker_choice[1], self.roll_screen.gs_formation_num, self.roll_screen.gs_swarm_num)
                pyxel.clip()
                pyxel.cls(0)
                self.roll_screen = None
                self.attack_click = 0
        # Remove marines from self.available_marines if marine['attack_used'] == True
        self.available_marines = [marine for marine in self.available_marines if not marine['attack_used']]


# TODO Need to check if available attackers == 0 to move on to
#       next card or phase.

    
    def draw(self):
        if self.attack_click == 0:
            self.available_sm_draw()
        elif self.attack_click == 1:
            self.sm_gs_selection_draw()
        elif self.attack_click == 2:
            self.roll_screen.screen_draw()
