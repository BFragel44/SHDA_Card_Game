import pyxel

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


def sort_card_numbers(prev_turn_cards): # self.ac_prev_turn
        """
        Returns
        -------
        card_dict: dict of action card order numbers.

        """
        card_dict = {}
        card_type = {16: "attack_card", 88: "support_card", 160: "move_act_card"}
        team = {0: 8, 86: 3, 172: 13}  # [RED, GREEN, GREY]
        # self.ac_prev_turn = [(16, 0), (16, 86), (16, 172)]
        for card in prev_turn_cards:
            team_color = team.get(card[1])
            ac_type = card_type.get(card[0])
            each_number = ac.all_action_cards[team_color][ac_type]["ac_number"]
            card_dict.update({each_number: (team_color, ac_type)})
        card_dict = {key: card_dict[key] for key in sorted(card_dict.keys())}
        return card_dict
# acards = {1: (8, 'attack_card'), 8: (3, 'support_card'), 17: (13, 'move_act_card')}
# {Turn_order: (Team_color, Card_type)}


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
        self.sorted_cards = None

    def ac_selection(self):
        """
        Handles the selection and deselection of action cards.

        This method uses the current position of the selection rectangle to determine the selected card.
        - If the selected card is not already in the list of selected cards and its row is not blocked, it's added to the list.
        - If the selected card is already in the list, it's removed from the list.
        - If the selected card's row is blocked and the card is not in the list, a sound is played.

        The method also manages a list of blocked rows. When a card is selected, its row is added to the list of blocked rows.
        When a card is deselected, its row is removed from the list of blocked rows.

        Returns no value. It modifies the `ac_selected_list` and `blocked_out_rows` attributes of the `self` object.
        """
        # Get the x-coordinate and column of the selection rectangle
        x_value = self.sel_rect_x
        x_choice = self.select_rect_col

        # Get the y-coordinate and row of the selection rectangle
        y_value = self.sel_rect_y
        y_choice = self.select_rect_row

        # Create a tuple representing the selected card
        single_choice = (x_choice[x_value], y_choice[y_value])
        # Get the row of the selected card
        y_check = single_choice[1]

        # Check if < 3 cards have been selected
        if len(self.ac_selected_list) < 3:
            # If the selected card is not already selected and its row is not blocked
            if (single_choice not in self.ac_selected_list and y_check not in self.blocked_out_rows):
                # Add the selected card to the list of selected cards
                self.ac_selected_list.append(single_choice)
                # Block the row of the selected card
                self.blocked_out_rows.append(y_check)
            # If the selected card is not already selected but its row is blocked, plays a "no" sound
            elif (single_choice not in self.ac_selected_list and y_check in self.blocked_out_rows):
                
                pyxel.play(1, 12)
            else:
                # If the selected card is already selected
                if single_choice in self.ac_selected_list:
                    # Remove the selected card from the list of selected cards
                    self.ac_selected_list.remove(single_choice)
                    # Unblock the row of the selected card
                    self.blocked_out_rows.remove(single_choice[1])


    def sort_card_numbers(self):
        """
        Sorts the action cards based on their order numbers.

        This method creates a dictionary where the keys are the order numbers of the action cards and the values are tuples containing the team color and the type of the action card. The dictionary is then sorted by the order numbers.

        The method uses the `ac_prev_turn` attribute, which is a list of tuples representing the action cards. Each tuple contains the x-coordinate (representing the type of the action card) and the y-coordinate (representing the team color) of the action card.

        Returns
        -------
        dict
            A dict where the keys = order numbers of the action cards and the values are tuples containing the team color and the type of the action card. The dict is sorted by the order numbers.

        Example
        -------
        If `ac_prev_turn` is [(16, 0), (16, 86), (16, 172)], the method might return {1: (8, 'attack_card'), 2: (3, 'attack_card'), 3: (13, 'attack_card')}.
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

    def update(self):
        """
        Handles user input to select action cards and updates game state.

        This method responds to left mouse button clicks to select action cards based on the mouse position. 
        
        It updates the selection rectangle and arrow position accordingly. 
        
        If two cards are selected, a third card is added upon the next click, the selection is cleared, 
        
        and the game state progresses.

        The method utilizes several attributes: 
            `ac_selected_list` to track selected cards, 
            `ac_prev_turn` and `ac_prev_blocked_out` to store the previous turn's state, 
            `confirm_choices` to track confirmation state, 
            `sorted_cards` to store the sorted order of action cards.
        """
        # Check if left mouse button was pressed
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Calculate which card was clicked based on mouse position
            clicked_row = pyxel.mouse_y // 86  # Each row is 86 pixels high

            # Adjust mouse x position for starting x value and gap between cards
            adjusted_mouse_x = pyxel.mouse_x - 16
            if adjusted_mouse_x > 72:
                adjusted_mouse_x += 2  # Add gap for cards 2 and 3

            clicked_col = adjusted_mouse_x // 72  # Each column is 72 pixels wide

            # Check if clicked card is within valid range
            if 0 <= clicked_row <= 2 and 0 <= clicked_col <= 2:
                self.arrow_row = clicked_row
                self.sel_rect_y = clicked_row
                self.sel_rect_x = clicked_col
            # If clicked cards are not at 2, continue selecting
            if len(self.ac_selected_list) < 2:
                self.ac_selection()
            # If clicked cards are at 2 and mouse is clicked, add 3rd card and proceed to next game state --RESOLVE ACTIONS--
            elif len(self.ac_selected_list) == 2:
                self.ac_selection()
                self.confirm_choices = 1
                self.ac_prev_turn = self.ac_selected_list
                self.ac_prev_blocked_out = self.blocked_out_rows
                self.ac_selected_list = []
                self.confirm_choices = 2
                self.sorted_cards = self.sort_card_numbers()

##################


    def _draw(self):
# TODO clean up ACTION CARD visuals
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

                                #ACTION#    #SUPPORT#   #MOVE + ACTION#
        # red_team_ac_cards =   (16, 0),    (88, 0),    (160, 0)
        # green_team_ac_cards = (16, 86),   (88, 86),   (160, 86)
        # grey_team_ac_cards =  (16, 172),  (88, 172),  (160, 172)

        ### ROW 1 -- RED TEAM
        pyxel.rectb(16, rect_row1_y, 70, 85, 7)
        pyxel.text(20, type_row1_y, "ATTACK", 7)
        pyxel.text(75,type_row1_y, str(self.all_action_cards[RED]["attack_card"]["ac_number"]), 7)
        pyxel.text(20, name_row1_y, self.all_action_cards[RED]["attack_card"]["ac_name"], RED)
        pyxel.text(18, desc_row1_y, self.all_action_cards[RED]["attack_card"]["ac_effect"], 7)
        
        pyxel.rectb(88, rect_row1_y, 70, 85, 7)
        pyxel.text(92, type_row1_y, "SUPPORT", 7)
        pyxel.text(150,type_row1_y, str(self.all_action_cards[RED]["support_card"]["ac_number"]),7)
        pyxel.text(105, name_row1_y, self.all_action_cards[RED]["support_card"]["ac_name"], RED)
        pyxel.text(90, desc_row1_y, self.all_action_cards[RED]["support_card"]["ac_effect"], 7)
        
        pyxel.rectb(160, rect_row1_y, 70, 85, 7)
        pyxel.text(164, type_row1_y, "MOVE/ACTION", 7)
        pyxel.text(224, type_row1_y, str(self.all_action_cards[RED]["move_act_card"]["ac_number"]), 7)
        pyxel.text(165, name_row1_y, self.all_action_cards[RED]["move_act_card"]["ac_name"], RED)
        pyxel.text(162, desc_row1_y, self.all_action_cards[RED]["move_act_card"]["ac_effect"], 7)

        ### ROW 2 -- GREEN TEAM
        pyxel.rectb(16, rect_row2_y, 70, 85, 7)
        pyxel.text(20, type_row2_y, "ATTACK", 7)
        pyxel.text(75, type_row2_y, str(self.all_action_cards[GREEN]["attack_card"]["ac_number"]), 7)
        pyxel.text(20, name_row2_y, self.all_action_cards[GREEN]["attack_card"]["ac_name"], GREEN)
        pyxel.text(18, desc_row2_y, self.all_action_cards[GREEN]["attack_card"]["ac_effect"], 7)

        pyxel.rectb(88, rect_row2_y, 70, 85, 7)
        pyxel.text(92, type_row2_y, "SUPPORT", 7)
        pyxel.text(150, type_row2_y, str(self.all_action_cards[GREEN]["support_card"]["ac_number"]),7)
        pyxel.text(105,name_row2_y, self.all_action_cards[GREEN]["support_card"]["ac_name"], GREEN)
        pyxel.text(90, desc_row2_y, self.all_action_cards[GREEN]["support_card"]["ac_effect"], 7)

        pyxel.rectb(160, rect_row2_y, 70, 85, 7)
        pyxel.text(164, type_row2_y, "MOVE/ACTION", 7)
        pyxel.text(220, type_row2_y, str(self.all_action_cards[GREEN]["move_act_card"]["ac_number"]), 7)
        pyxel.text(165, name_row2_y, self.all_action_cards[GREEN]["move_act_card"]["ac_name"], GREEN)
        pyxel.text(162, desc_row2_y, self.all_action_cards[GREEN]["move_act_card"]["ac_effect"],7)

        ### ROW 3 -- GREY TEAM
        pyxel.rectb(16, rect_row3_y, 70, 85, 7)
        pyxel.text(20, type_row3_y, "ATTACK", 7)
        pyxel.text(75, type_row3_y, str(self.all_action_cards[GREY]["attack_card"]["ac_number"]), 7)
        pyxel.text(20, name_row3_y, self.all_action_cards[GREY]["attack_card"]["ac_name"], GREY)
        pyxel.text(18, desc_row3_y, self.all_action_cards[GREY]["attack_card"]["ac_effect"], 7)

        pyxel.rectb(88, rect_row3_y, 70, 85, 7)
        pyxel.text(92, type_row3_y, "SUPPORT", 7)
        pyxel.text(150, type_row3_y, str(self.all_action_cards[GREY]["support_card"]["ac_number"]), 7)
        pyxel.text(105, name_row3_y, self.all_action_cards[GREY]["support_card"]["ac_name"], GREY)
        pyxel.text(90, desc_row3_y, self.all_action_cards[GREY]["support_card"]["ac_effect"], 7)

        pyxel.rectb(160, rect_row3_y, 70, 85, 7)
        pyxel.text(164, type_row3_y, "MOVE/ACTION", 7)
        pyxel.text(224, type_row3_y, str(self.all_action_cards[GREY]["move_act_card"]["ac_number"]), 7)
        pyxel.text(165, name_row3_y, self.all_action_cards[GREY]["move_act_card"]["ac_name"], GREY)
        pyxel.text(162, desc_row3_y, self.all_action_cards[GREY]["move_act_card"]["ac_effect"], 7)

        ### SELECTOR RECTANGLE OUTLINE
        pyxel.rectb(self.select_rect_col[self.sel_rect_x], self.select_rect_row[self.sel_rect_y], 70, 85, RED)

        ### CONFIRM AC CHOICES MINISCREEN\
        if self.confirm_choices == 1:
            pyxel.rect(12, 100, 222, 60, 0)
            pyxel.rectb(12, 100, 222, 60, 3)

            pyxel.text(100, 110, "CONFIRM CHOICES?", 7)
            pyxel.text(125, 118, "YES", 7)
            pyxel.text(125, 124, "NO", 7)

            ### MINISCREEN SELECTOR ARROW
            miniscreen_arrow = (118, 124)
            pyxel.blt(118, miniscreen_arrow[self.miniscreen_choice], 0, 10, 32, 6, 6)


# self.ac_prev_turn = [(16, 0), (88, 86), (160, 172)]
class ActionOverlay:
    def __init__(self):
        self.ac_count = 1
        atk_package = None

    def update(self):
        if self.window_state == 2:
            actions = sort_card_numbers(prev_turn_cards)
# actions = {15: (13, 'attack_card'), 16: (3, 'attack_card'), 17: (8, 'attack_card')}
            a_list = [a for a, v in actions.items()]
# a_list = [15, 16, 17]
            sm = self.space_marines.combat_teams

            if a_list:
                if pyxel.btnp(pyxel.KEY_RETURN):
                    action_number = a_list.pop(0)
                    cardtype = actions.get(action_number[self.ac_count-1])[1]
                    cardteam = actions.get(action_number[self.ac_count-1])[0]

                    if cardtype == "attack_card":
                        lgs = self.location_and_spawns.spawned_left_swarms
                        rgs = self.location_and_spawns.spawned_right_swarms
                        attacking_marines = [s for s in sm if s["team_color"] == cardteam]

                        attack_values = self.space_marines.attack_prep(attacking_marines, lgs, rgs)
                        self.space_marines.atk_info_sort(attack_values)
                        if self.space_marines.phase_two == True:
                            self.space_marines.defGs_info_sort()
                    self.ac_count += 1
                    print(self.ac_count)
                self.space_marines.update()

    def _draw(self):
        pyxel.cls(0)
        pyxel.text(160, 160, "Action Overlay", 7)
