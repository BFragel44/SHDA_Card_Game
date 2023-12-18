import random
import pyxel

# GREY = 13
# GREEN = 3
# RED = 8

combat_teams = [
    {'sm_name':'Lexicanium Calistarius',
        'team_color': 13, 
        'visual': (0,0), 
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 1,
        },

    {'sm_name':'Brother Scipio',
        'team_color': 13,
        'visual': (0, 16), 
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 2,
        },

    {'sm_name':'Sargeant Gideon',
        'team_color': 3,
        'visual': (16, 0),  
        'attk_range': 0, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 1,
        },

    {'sm_name':'Brother Noctis',
        'team_color': 3,
        'visual': (16, 16),              
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 2,
        },

    {'sm_name':'Brother Leon',
        'team_color': 8,
        'visual': (32, 0),    
        'attk_range': 3, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 1,
        },

    {'sm_name':'Brother Valencio',
        'team_color': 8,
        'visual': (32, 16),             
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_token': 0,
        'team_id': 2,
        }]

sm_visual_dimms = {
    "name_x": 109,
    "name_y": (60, 96, 132, 168, 204, 240),
    "portrait_x": 120,
    "portrait_y": (40, 76, 112, 148, 184, 220),
    "left_arrow_x": 97,
    "right_arrow_x": 154,
    "arrow_y": (41, 77, 113, 149, 185, 221),
    "card_border_x": 96,
    "card_border_y": (40, 76, 112, 148, 184, 220),
    "card_border_w": 65,
    "card_border_h": 33}

def shuffle_deck(combat_teams):
    # Create a list formation numbers from 1-6
    formation_numbers = list(range(1, 7))
    random.shuffle(formation_numbers)
    # Assign random formation numbers, set facing accordingly
    for marine in combat_teams:
        marine['formation_num'] = formation_numbers.pop()  # Pop a unique formation number
        marine['facing'] = 'LEFT' if marine['formation_num'] <= 3 else 'RIGHT'
    return combat_teams


class Space_marines:
    def __init__(self):
        # LIST of DICTS
        self.combat_teams = shuffle_deck(combat_teams)
        self.atk_package = None
        self.phase_one = False
        self.phase_two = False
        self.sm_choice = 0
        self.sm_list = []
        self.gs_list = []
        self.gs_choice = 0
        self.opponents = {}
        self.direction = None

    def update(self):
        if self.atk_package:
            if self.phase_one:
                print("self.sm_list = ", self.sm_list)
                if pyxel.btnp(pyxel.KEY_W) and self.sm_choice > 0:
                    self.sm_choice -= 1

                if pyxel.btnp(pyxel.KEY_S) and self.sm_choice < len(
                        self.sm_list)-1:
                    self.sm_choice += 1

                if pyxel.btnp(pyxel.KEY_F):
                    self.opponents['attacker'] = self.sm_list[self.sm_choice]
                    for facing, val_dict in self.atk_package.items():
# TODO problem area #1                        
                        if self.opponents['attacker']+1 in val_dict:
                            self.direction = facing

                    self.phase_two = True
                    self.phase_one = False
            # self.sm_list[self.sm_choice] = LEFT
            
            elif self.phase_two:
                if pyxel.btnp(pyxel.KEY_UP) and self.gs_choice > 0:
                    self.gs_choice -= 1

                if pyxel.btnp(pyxel.KEY_DOWN) and self.gs_choice < len(
                        self.gs_list)-1:
                    self.gs_choice += 1

                if pyxel.btnp(pyxel.KEY_F):
                    #self.opponents['defender'] = self.gs_list[self.gs_choice]
                    self.sm_list = []
                    self.phase_two = False

    def atk_info_sort(self, attack_values):
        for side, pairings in attack_values.items():
            for sm, gs in pairings.items():
                self.sm_list.append(sm-1)
        self.phase_one = True
        self.atk_package = attack_values
        print("self.atk_package from shda_marines.py = ",self.atk_package)
    
    def defGs_info_sort(self):
        for k,v in self.atk_package.items():
            # k,v = {'LEFT': {2: [2]}}

            for facing, vs_list in v.items():
                #facing, vs_dict = LEFT, {3: [2], 2: [2]}
                for gs_list in vs_list:
                    print(gs_list)

    def attack_prep(self, attacking_marines, lgs, rgs):
        '''
        Parameters
        ----------
        attacking_marines : TYPE
            DESCRIPTION.
        lgs : TYPE
            DESCRIPTION.
        rgs : TYPE
            DESCRIPTION.

        Returns
        -------
        gs_in_range : LIST
            Returns list of enemies in Range
        '''
        left = [(k, v["g_stealers"]) for k, v in lgs.items()
                if len(v["g_stealers"]) != 0]

        right = [(k, v["g_stealers"]) for k, v in rgs.items()
                 if len(v["g_stealers"]) != 0]
        # left = [(0, ['claws', 'stingray'])] ## list --> tuple(int, [list])
        # right = [(3, ['tails'])]
# TODO may be out of date since marines are now 1-6 instead of 0-5
        # GS formation numbers MUST BE +1 in order to line up with ATK RANGE!!!!!
        gs_in_range = {}
        left_dict = {}
        right_dict = {}

        for attacker in attacking_marines:
            lo_range = 1
            hi_range = 6

            lo_range = attacker.get("formation_num") - attacker.get("attk_range")
            if lo_range < 1:
                lo_range = 1
            
            hi_range = attacker.get("formation_num") + attacker.get("attk_range")
            if hi_range > 6:
                hi_range = 6

            if attacker.get("facing") == "LEFT":
                for row in left:
                    if row[0] + 1 in range(lo_range, hi_range + 1):
                        left_atker = attacker.get("formation_num")
                        if left_atker in left_dict:
                            left_dict[left_atker].append(row[0])
                        else:
                            left_dict[left_atker] = [row[0]]

            if attacker.get("facing") == "RIGHT":
                for row in right:
                    if 6 - row[0] + 1 in range(lo_range, hi_range + 1):
                        right_atker = attacker.get("formation_num")
                        if right_atker in right_dict:
                            right_dict[right_atker].append(row[0])
                        else:
                            right_dict[right_atker] = [row[0]]
        if left_dict:
            gs_in_range["LEFT"] = left_dict
        if right_dict:
            gs_in_range["RIGHT"] = right_dict

        return gs_in_range 
# gs_in_range = {'LEFT': {3: {'targets': [0]}, 1: {'targets': [0]}}}

        # attacking_marines = list of dicts, 1 dict for each marine
        # GREY = 13: Each time team_id_1 rolls SKULL while ATTACKING, make 1 additional attack.
        # GREEN = 3: Each time a GREEN teammate rolls 4, kill up to THREE from defending swarm.
        # RED = 8: team_id_1 can attack up to THREE times.
    def _draw(self):
        for roster_dict in self.combat_teams:
            y_val = roster_dict["formation_num"]
            col = roster_dict["team_color"]
            sm_face = roster_dict["visual"]
            sm_name = roster_dict["sm_name"].split(" ")
            single_y = sm_visual_dimms["arrow_y"][y_val - 1]
            # sm card border
            pyxel.rectb(sm_visual_dimms["card_border_x"],
                        sm_visual_dimms["card_border_y"][y_val - 1],
                        sm_visual_dimms["card_border_w"],
                        sm_visual_dimms["card_border_h"], col,)
            # sm portrait
            pyxel.blt(sm_visual_dimms["portrait_x"] + 1,
                        sm_visual_dimms["portrait_y"][y_val - 1], 0, sm_face[0], sm_face[1], 15, 16,)
            # sm portrait border
            pyxel.rectb(sm_visual_dimms["portrait_x"],
                        sm_visual_dimms["portrait_y"][y_val - 1], 17, 17, col)
            # SM name 1
            pyxel.text(sm_visual_dimms["name_x"],
                       sm_visual_dimms["name_y"][y_val - 1], f"{sm_name[0]}", col)
            # SM name 2
            pyxel.text(sm_visual_dimms["name_x"] - 2,
                       sm_visual_dimms["name_y"][y_val - 1] + 6, f"{sm_name[1]}", col)
            # sm facing arrows
            y_arrow_list = [single_y, single_y + 7, single_y + 14]
            if roster_dict["facing"] == "LEFT":
                for y_val in y_arrow_list:
                    pyxel.blt(sm_visual_dimms["left_arrow_x"], y_val, 0, 0, 32, 6, 6)
            else:
                for y_val in y_arrow_list:
                    pyxel.blt(sm_visual_dimms["right_arrow_x"], y_val, 0, 10, 32, 6, 6)
