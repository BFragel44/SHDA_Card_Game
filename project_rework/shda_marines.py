import random

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


# shuffle the cards
def shuffle_deck(combat_teams):
    formation_numbers = [1,2,3,4,5,6]
    random.shuffle(formation_numbers)
    for marine in combat_teams:   
        num = formation_numbers.pop(0)
        set_formation = {'formation_num': num}
        marine.update(set_formation)
        if num <= 3:
            set_facing = {'facing': 'LEFT'}
            marine.update(set_facing)
        else:
            set_facing = {'facing': 'RIGHT'}
            marine.update(set_facing)
    return(combat_teams)


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
                    
    # TODO
    def defense(self, defending_marines):
        pass

    
    def atk_info_sort(self, attack_values):
        for side, pairings in attack_values.items():
            for sm, gs in pairings.items():
                self.sm_list.append(sm-1)
        self.phase_one = True
        self.atk_package = attack_values
    
    
    def defGs_info_sort(self):
        for k,v in self.atk_package.items():
            # k,v = {'LEFT': {2: [2]}}
# TODO problem area #2
            for facing, vs_list in v.items():
                #facing, vs_dict = LEFT, {3: [2], 2: [2]}
                for gs_list in vs_list:
                    print(gs_list)


        #         if sm_num == self.opponents['attacker']:
        #             self.gs_list.append(gs_nums)
        #             print("appended!")
        #             print("appended!")
        #             print("appended!")
        # print(f"self.gs_list = {self.gs_list}")


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

    def support(self, supporting_marines):
        pass

    def move_action(self, moving_marines):
        pass

    def sm_death(self, killed_marine):
        pass

    # TODO

    def support_token(self):
        pass


### atk_package() DRAW
            # if self.atk_package:
            #     gs_left_x = 5
            #     gs_right_x = 183
                
            #     if self.phase_one:
            #         selection = self.sm_list[self.sm_choice]
            #         #marine
            #         pyxel.rectb(
            #             card_border_x - 2,
            #             card_border_y[selection] - 2,
            #             card_border_w + 4,
            #             card_border_h + 4,
            #             9)
                
                # elif self.phase_two:
                #     print(f"gs_choice = {self.gs_choice}")
                #     #selected marine
                    
                #     pyxel.rectb(
                #         card_border_x - 2,
                #         card_border_y[self.sm_list[self.sm_choice]] - 2,
                #         card_border_w + 4,
                #         card_border_h + 4,
                #         13)
                    
                #     if self.direction == "LEFT":
                #         selection = self.gs_list[self.gs_choice]
                #         #gs
                #         pyxel.rectb(
                #             gs_left_x,
                #             card_border_y[selection] - 2,
                #             card_border_w + 4,
                #             card_border_h + 4,
                #             9)
                    
                #     elif self.direction == 'RIGHT':
                #         #gs
                #         pyxel.rectb(
                #             gs_right_x,
                #             card_border_y[self.gs_list[self.gs_choice]] - 2,
                #             card_border_w + 4,
                #             card_border_h + 4,
                #             9)

                # else:
                #     pyxel.rect(screen_x/2-25, screen_y/2-25, 50, 15, 8)
                #     pyxel.text(screen_x/2-24, screen_y/2-25, "No Valid ATK", 7)
