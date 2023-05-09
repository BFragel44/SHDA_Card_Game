# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:59:09 2022

@author: brett
"""

# GREY = 13 = Each time LC rolls SKULL while ATTACKING, make 1 additional attack.
# GREEN = 3 = Each time a GREEN teammate rolls 4, kill up to THREE from defending swarm.
# RED = 8 = BROTHER LEON can attack up to THREE times.

grey_cards = {
    'attack_card':{
        'ac_name':' Psionic Attack',
        'ac_number':15,
        'ac_effect':'Each time LC\nrolls SKULL while\nATTACKING, make 1\nadditional attack.'},
    'support_card':{
        'ac_name':'Power Field',
        'ac_number':6,
        'ac_effect':'After SUPPORT\nresolved, choose\nany SWARM. They\ncan\'t attack or\nbe killed this\nround.'},
    'move_act_card':{
        'ac_name':'Stealth Tactics',
        'ac_number':8,
        'ac_effect':'After MVE/ACT,\nyou may DISCARD 1\ncard from a blip\npile. Spend 1\nTOKEN to discard\n1 card from other pile.'}}

green_cards = {
    'attack_card':{
        'ac_name':'   Dead Aim',
        'ac_number':16,
        'ac_effect':'each time 1 of\nTEAM rolls 4,\nKILL up to 3\nXenos from the\ndefending swarm.'},
    'support_card':{
        'ac_name':'  Block',
        'ac_number':1,
        'ac_effect':'Each time GIDEON\nrolls a SKULL\nwhile DEFENDING,\nthe attack\nMISSES.'},
    'move_act_card':{
        'ac_name':'  Run and Gun',
        'ac_number':12,
        'ac_effect':'After MVE/ACT\nresolved, each\nof TEAM may\nspend 1 TOKEN\nto make 1 ATTACK'}}

red_cards = {
    'attack_card':{
        'ac_name':'   Full Auto',
        'ac_number':17,
        'ac_effect':'BROTHER LEON may\nATTACK up to 3\ntimes instead of\nonce.'},
    'support_card':{
        'ac_name':'Overwatch',
        'ac_number':4,
        'ac_effect':'At end of the\nEVENT PHASE,\neach TEAM may\nspend 1 TOKEN\nfor 1 ATTACK.'},
    'move_act_card':{
        'ac_name':'Onward Brothers',
        'ac_number':7,
        'ac_effect':'Each time 1 of\nTEAM activates\na DOOR, you may\nplace 1 extra\nTOKEN on the\nTERRAIN'}}

all_sm_action_cards = {3: green_cards, 8: red_cards, 13: grey_cards}


class Action_cards:
    def __init__(self):
        self.all_action_cards = all_sm_action_cards
        self.arrow_row = 0
        self.sel_rect_y = 0
        self.sel_rect_x = 0

        self.ac_sel = 0
        self.ac_selected_list = []
        self.blocked_out_rows = []

        self.ac_prev_turn = None
        self.ac_prev_blocked_out = None

        self.confirm_choices = 0
        self.miniscreen_choice = 0

    def ac_selection(self):
        x_value = self.sel_rect_x
        x_choice = self.select_rect_col

        y_value = self.sel_rect_y
        y_choice = self.select_rect_row

        single_choice = (x_choice[x_value], y_choice[y_value])
        y_check = single_choice[1]

        if len(self.ac_selected_list) < 3:

            if (
                single_choice not in self.ac_selected_list
                and y_check not in self.blocked_out_rows
            ):
                self.ac_selected_list.append(single_choice)
                self.blocked_out_rows.append(y_check)
            elif (
                single_choice not in self.ac_selected_list
                and y_check in self.blocked_out_rows
            ):
                pyxel.play(1, 12)
            else:
                if single_choice in self.ac_selected_list:
                    self.ac_selected_list.remove(single_choice)
                    self.blocked_out_rows.remove(single_choice[1])

    def sort_card_numbers(self):
        """
        Returns
        -------
        card_dict: dict of action card order numbers.

        """
        card_dict = {}
        card_type = {16: "attack_card", 88: "support_card", 160: "move_act_card"}
        team = {0: 8, 86: 3, 172: 13}  # [RED, GREEN, GREY]

        # self.ac_prev_turn = [(16, 0), (16, 86), (16, 172)]
        for card in self.ac_prev_turn:
            team_color = team.get(card[1])
            ac_type = card_type.get(card[0])
            each_number = self.all_action_cards[team_color][ac_type]["ac_number"]
            card_dict.update({each_number: (team_color, ac_type)})
        card_dict = {key: card_dict[key] for key in sorted(card_dict.keys())}
        return card_dict

    ##### card_dict = {1: (8, 'attack_card'), 8: (3, 'support_card'), 17: (13, 'move_act_card')}
    # TODO BROKEN FROM HERE --- WILL NEED TO USE THIS TO FIND FORMATION OF EACH CARD'S SMs with SM CLASS FROM WITHIN APP()

    def update(self):
        if self.confirm_choices == 0:
            if pyxel.btnp(pyxel.KEY_W) and self.arrow_row != 0:
                self.arrow_row -= 1
                self.sel_rect_y -= 1
            if pyxel.btnp(pyxel.KEY_S) and self.arrow_row != 2:
                self.arrow_row += 1
                self.sel_rect_y += 1
            if pyxel.btnp(pyxel.KEY_A) and self.sel_rect_x != 0:
                self.sel_rect_x -= 1
            if pyxel.btnp(pyxel.KEY_D) and self.sel_rect_x != 2:
                self.sel_rect_x += 1
            if pyxel.btnp(pyxel.KEY_RETURN) and len(self.ac_selected_list) < 3:
                self.ac_selection()
            if pyxel.btnp(pyxel.KEY_RETURN) and len(self.ac_selected_list) == 3:
                self.confirm_choices = 1
        
        if self.confirm_choices == 1:
            if pyxel.btnp(pyxel.KEY_F) and self.miniscreen_choice == 0:
                self.ac_prev_turn = self.ac_selected_list
                self.ac_prev_blocked_out = self.blocked_out_rows
                self.ac_selected_list = []
                self.confirm_choices = 2
            if pyxel.btnp(pyxel.KEY_F) and self.miniscreen_choice == 1:
                self.confirm_choices = 0
                self.ac_selected_list.pop(-1)
                self.blocked_out_rows.pop(-1)
            if pyxel.btnp(pyxel.KEY_W) and self.miniscreen_choice != 0:
                self.miniscreen_choice -= 1
            if pyxel.btnp(pyxel.KEY_S) and self.miniscreen_choice != 1:
                self.miniscreen_choice += 1

    # TODO clean up ACTION CARD visuals
    def draw(self):
        pyxel.cls(0)
        pyxel.clip(0, 0, 257, 257)

        GREY = 13
        GREEN = 3
        RED = 8

        rect_row1_y = 0
        type_row1_y = 3
        name_row1_y = 38
        desc_row1_y = 48

        rect_row2_y = 86
        type_row2_y = 89
        name_row2_y = 125
        desc_row2_y = 135

        rect_row3_y = 172
        type_row3_y = 175
        name_row3_y = 211
        desc_row3_y = 221

        ### SELECTOR RECTANGLE OUTLINE VALUES
        self.select_rect_row = [0, 86, 172]
        self.select_rect_col = [16, 88, 160]

        ### SELECTOR ARROW
        arrow_y = (38, 125, 211)
        pyxel.blt(8, arrow_y[self.arrow_row], 0, 10, 32, 6, 6)

        ### SELECTED ACTION CARD
        if self.ac_selected_list:
            for selection in self.ac_selected_list:
                pyxel.rect(selection[0], selection[1], 70, 85, 1)

                # ACTION#    #SUPPORT#   #MOVE + ACTION#
        # red_team_ac_cards =   (16, 0),    (88, 0),    (160, 0)
        # green_team_ac_cards = (16, 86),   (88, 86),   (160, 86)
        # grey_team_ac_cards =  (16, 172),  (88, 172),  (160, 172)

        ### ROW 1 -- RED TEAM
        pyxel.rectb(16, rect_row1_y, 70, 85, 7)
        pyxel.text(20, type_row1_y, "ATTACK", 7)
        pyxel.text(
            75,
            type_row1_y,
            str(self.all_action_cards[RED]["attack_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            20, name_row1_y, self.all_action_cards[RED]["attack_card"]["ac_name"], RED
        )
        pyxel.text(
            18, desc_row1_y, self.all_action_cards[RED]["attack_card"]["ac_effect"], 7
        )

        pyxel.rectb(88, rect_row1_y, 70, 85, 7)
        pyxel.text(92, type_row1_y, "SUPPORT", 7)
        pyxel.text(
            150,
            type_row1_y,
            str(self.all_action_cards[RED]["support_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            105, name_row1_y, self.all_action_cards[RED]["support_card"]["ac_name"], RED
        )
        pyxel.text(
            90, desc_row1_y, self.all_action_cards[RED]["support_card"]["ac_effect"], 7
        )

        pyxel.rectb(160, rect_row1_y, 70, 85, 7)
        pyxel.text(164, type_row1_y, "MOVE/ACTION", 7)
        pyxel.text(
            224,
            type_row1_y,
            str(self.all_action_cards[RED]["move_act_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            165,
            name_row1_y,
            self.all_action_cards[RED]["move_act_card"]["ac_name"],
            RED,
        )
        pyxel.text(
            162,
            desc_row1_y,
            self.all_action_cards[RED]["move_act_card"]["ac_effect"],
            7,
        )

        ### ROW 2 -- GREEN TEAM
        pyxel.rectb(16, rect_row2_y, 70, 85, 7)
        pyxel.text(20, type_row2_y, "ATTACK", 7)
        pyxel.text(
            75,
            type_row2_y,
            str(self.all_action_cards[GREEN]["attack_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            20,
            name_row2_y,
            self.all_action_cards[GREEN]["attack_card"]["ac_name"],
            GREEN,
        )
        pyxel.text(
            18, desc_row2_y, self.all_action_cards[GREEN]["attack_card"]["ac_effect"], 7
        )

        pyxel.rectb(88, rect_row2_y, 70, 85, 7)
        pyxel.text(92, type_row2_y, "SUPPORT", 7)
        pyxel.text(
            150,
            type_row2_y,
            str(self.all_action_cards[GREEN]["support_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            105,
            name_row2_y,
            self.all_action_cards[GREEN]["support_card"]["ac_name"],
            GREEN,
        )
        pyxel.text(
            90,
            desc_row2_y,
            self.all_action_cards[GREEN]["support_card"]["ac_effect"],
            7,
        )

        pyxel.rectb(160, rect_row2_y, 70, 85, 7)
        pyxel.text(164, type_row2_y, "MOVE/ACTION", 7)
        pyxel.text(
            220,
            type_row2_y,
            str(self.all_action_cards[GREEN]["move_act_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            165,
            name_row2_y,
            self.all_action_cards[GREEN]["move_act_card"]["ac_name"],
            GREEN,
        )
        pyxel.text(
            162,
            desc_row2_y,
            self.all_action_cards[GREEN]["move_act_card"]["ac_effect"],
            7,
        )

        ### ROW 3 -- GREY TEAM
        pyxel.rectb(16, rect_row3_y, 70, 85, 7)
        pyxel.text(20, type_row3_y, "ATTACK", 7)
        pyxel.text(
            75,
            type_row3_y,
            str(self.all_action_cards[GREY]["attack_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            20, name_row3_y, self.all_action_cards[GREY]["attack_card"]["ac_name"], GREY
        )
        pyxel.text(
            18, desc_row3_y, self.all_action_cards[GREY]["attack_card"]["ac_effect"], 7
        )

        pyxel.rectb(88, rect_row3_y, 70, 85, 7)
        pyxel.text(92, type_row3_y, "SUPPORT", 7)
        pyxel.text(
            150,
            type_row3_y,
            str(self.all_action_cards[GREY]["support_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            105,
            name_row3_y,
            self.all_action_cards[GREY]["support_card"]["ac_name"],
            GREY,
        )
        pyxel.text(
            90, desc_row3_y, self.all_action_cards[GREY]["support_card"]["ac_effect"], 7
        )

        pyxel.rectb(160, rect_row3_y, 70, 85, 7)
        pyxel.text(164, type_row3_y, "MOVE/ACTION", 7)
        pyxel.text(
            224,
            type_row3_y,
            str(self.all_action_cards[GREY]["move_act_card"]["ac_number"]),
            7,
        )
        pyxel.text(
            165,
            name_row3_y,
            self.all_action_cards[GREY]["move_act_card"]["ac_name"],
            GREY,
        )
        pyxel.text(
            162,
            desc_row3_y,
            self.all_action_cards[GREY]["move_act_card"]["ac_effect"],
            7,
        )

        ### SELECTOR RECTANGLE OUTLINE
        pyxel.rectb(
            self.select_rect_col[self.sel_rect_x],
            self.select_rect_row[self.sel_rect_y],
            70,
            85,
            RED,
        )

        ### CONFIRM AC CHOICES MINISCREEN\
        if self.confirm_choices == 1:
            pyxel.rect(12, 100, 222, 60, 0)
            pyxel.rectb(12, 100, 222, 60, 3)

            s = "CONFIRM CHOICES?"
            pyxel.text(100, 110, s, 7)
            pyxel.text(125, 118, "YES", 7)
            pyxel.text(125, 124, "NO", 7)

            ### MINISCREEN SELECTOR ARROW
            miniscreen_arrow = (118, 124)
            pyxel.blt(118, miniscreen_arrow[self.miniscreen_choice], 0, 10, 32, 6, 6)


# self.ac_prev_turn = [(16, 0), (88, 86), (160, 172)]
