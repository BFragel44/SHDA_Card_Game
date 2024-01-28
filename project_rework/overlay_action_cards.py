import pyxel
import ui

# Action types:
# 1. SUPPORT CARD
# ----------------
#   a. [Gain a Support Token, to be placed on any Marine] + [Execute text of card]
#   b. limited to a single Support Token per Team

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
        # self.roll_screen = RollScreen() # <- needs to be built

    def update(self):
        if ui.box_click(0, 0, 255, 255):
            # Get the next element of self.action_cards
            try:
                next_card = next(self.action_cards)
            except StopIteration:
                pass
                # if no more elements in self.action_cards
                # GENESTEALER ATTACK PHASE activation here
            print(next_card)
            self.action_card_funnel(next_card)
 
    def action_card_funnel(self, next_card):
        card_info = self.selected_action_cards.get(next_card)
        #  (3, 'support_card')

        if card_info[1] == 'support_card':
            print('support card match!')
            self.support_card(card_info[0])

        elif card_info[1] == 'move_act_card':
            self.move_card(card_info[0])

        elif card_info[1] == 'attack_card':
            self.attack_card(card_info[0])
    
    def support_card(self, card_info):
#   a. [Gain a Support Token, to be placed on any Marine] + [Execute text of card]
#   b. limited to a single Support Token per Team
        for marines in self.space_marines.combat_teams:
            if marines['status'] == 'alive':
                print(marines['sm_name'])
                print(marines['formation_num'])
                
# support card TEAM ABILITES:
#   RED = AFTER EVENT PHASE Each time a Support Card is played, the Team gains a Support Token.
#   GREEN = Each time GIDEON rolls SKULL while DEFENDING, attack misses.
#   GREY = After Support Token resolved, pick swarm, they cannot attack or be killed this turn.
    
    def support_card_draw(self, card_info):
        pass


    def overlay_draw(self):
        pass
