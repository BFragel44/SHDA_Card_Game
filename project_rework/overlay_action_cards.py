import pyxel
import action_cards as ac


class ActionOverlay():
    def __init__(self):
        self.action_cards = ac.Action_cards()
        # self.roll_screen = RollScreen()
        self.ac_count = 1
        self.atk_package = None

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
        if self.window_state == 2:
            pyxel.clip()
            pyxel.cls(0)
            ### atk_package() DRAW
            if self.atk_package:
                gs_left_x = 5
                gs_right_x = 183

                if self.phase_one:
                    card_border_x = 96
                    card_border_y = (40, 76, 112, 148, 184, 220)
                    card_border_w = 65
                    card_border_h = 33
                    selection = self.sm_list[self.sm_choice]
                    #marine
                    pyxel.rectb(
                        card_border_x - 2,
                        card_border_y[selection] - 2,
                        card_border_w + 4,
                        card_border_h + 4,
                        9)

                elif self.phase_two:
                    print(f"gs_choice = {self.gs_choice}")
                    #selected marine

                    pyxel.rectb(card_border_x - 2,
                        card_border_y[self.sm_list[self.sm_choice]] - 2,
                        card_border_w + 4,
                        card_border_h + 4,
                        13)

                    if self.direction == "LEFT":
                        selection = self.gs_list[self.gs_choice]
                        #gs
                        pyxel.rectb(gs_left_x,
                            card_border_y[selection] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)

                    elif self.direction == 'RIGHT':
                        #gs
                        pyxel.rectb(gs_right_x,
                            card_border_y[self.gs_list[self.gs_choice]] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)
                else:
                    pyxel.rect(screen_x/2-25, screen_y/2-25, 50, 15, 8)
                    pyxel.text(screen_x/2-24, screen_y/2-25, "No Valid ATK", 7)
