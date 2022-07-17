import pyxel
import random
# import itertools
import pandas as pd

import heartrate
heartrate.trace(browser=False)

import shda_marines as marines
import action_cards as act_cards

# https://morgan3d.github.io/articles/2017-05-29-space-hulk/

# GAME PHASES #
# -------------#
# 1. Choose Actions Phase:
# Player chooses which action card to play for each COMBAT TEAM.
# 2. Resolve Actions Phase:
# Player resolves the action cards they chose, in ASCENDING ORDER (start with lowest number card)
# 3. Genestealer Attack Phase:
# Each SWARM of GS in play ATTACKS the SM they are ENGAGED with.
# 4. Event Phase:
# Player draws the top card of the EVENT DECK and resolves it.

############################################################
screen_x = 257
screen_y = 257

GREY = 13
GREEN = 3
RED = 8

# Draws grid for game object placement help
draw_grid = "N"


def build_grid(max_x, max_y):
    for res in [max_x, max_y]:
        for i in range(res):
            if i % 4 == 0:
                if i == res // 2:
                    pyxel.line(i, 0, i, res, 9)
                    pyxel.line(0, i, res, i, 9)
                else:
                    pyxel.line(i, 0, i, res, 2)
                    pyxel.line(0, i, res, i, 2)


########################################################### SPACE MARINES
## INITIAL MARINE PLACEMENT
sm_deck = marines.shuffle_deck(marines.combat_teams)

########################################################### LOCATION DECK
## INITIAL LOCATION DECK CREATION
def create_location_deck():
    """
    Pulls location data from the CSV and sorts/shuffles each location into
    a main location deck - complete with the VOID LOCK on top to start.

    Returns
    -------
    final_locs : TYPE
        DESCRIPTION.
    """
    final_locs = []
    data = "location_cards.csv"
    df = pd.read_csv(data)
    df.set_index("location")
    df.to_dict("dict")
    loc_list = df.to_dict("records")

    vLock = loc_list.pop(0)
    loc_two = [loc for loc in loc_list if loc["loc_number"] == 2]
    loc_three = [loc for loc in loc_list if loc["loc_number"] == 3]
    loc_four = [loc for loc in loc_list if loc["loc_number"] == 4]
    all_locs = (loc_two, loc_three, loc_four)
    for deck in all_locs:
        random.shuffle(deck)
        loc_card = deck.pop(0)
        final_locs.append(loc_card)
    final_locs.insert(0, vLock)
    return final_locs


# This is the FINAL, shuffled, location deck
# locations_deck = create_location_deck()
# number_of_locations = len(locations_deck)
# print(number_of_locations)

########################################################## GENESTEALER DECK
def gs_deck_create():
    """
    Creates the Genestealer deck for the start of play.

    Returns
    -------
    initial_deck : TYPE
    """
    gs_icons = ["tails", "skulls", "stingray", "claws"]
    gs_raw_deck = []
    for g in gs_icons:
        for i in range(11):
            gs_raw_deck.append(g)
    random.shuffle(gs_raw_deck)
    return gs_raw_deck


gs_deck = gs_deck_create()

## INITIAL GS MAIN DECK CREATION
# def gs_deck_create():
#     initial_deck = list(itertools.product(range(1,10),['Tail','Skull','Stingray','Claw']))
#     random.shuffle(initial_deck)
#     return initial_deck

# gs_deck = gs_deck_create()
###########################################################
class Gene_deck:
    def __init__(self, gs_deck, loc_num_left=6, loc_num_right=6):
        self.deck = gs_deck
        self.loc_left = loc_num_left
        self.loc_right = loc_num_right
        self.left_num = 0
        self.right_num = 0
        self.left_cards = []
        self.right_cards = []

    def populate_blips(self):
        self.left_cards = [self.deck.pop(i) for i in range(self.loc_left)]
        self.left_num = len(self.left_cards)
        self.right_cards = [self.deck.pop(i) for i in range(self.loc_right)]
        self.right_num = len(self.right_cards)

    # def left_blip_pile(self, left_cards, swarm_num):
    #     left_cards = self.left_cards

    # def right_blip_pile(self, right_cards, swarm):
    #     right_cards = self.right_cards

    def draw(self):
        pyxel.text(36, 18, f"{self.left_num}", 7)
        pyxel.text(218, 18, f"{self.right_num}", 7)


########################################################### EVENT DECK CREATION
def create_event_deck():
    """
    Creates the EVENT deck for the start of play.

    Returns
    -------
    event_deck : TYPE
        DESCRIPTION.

    """
    data = "event_cards.csv"
    df = pd.read_csv(data)
    df["card_num"] = df.reset_index().index
    df.to_dict("dict")
    event_deck = df.to_dict("records")
    random.shuffle(event_deck)
    return event_deck


# #this is the initial, shuffled, Event deck
event_deck = create_event_deck()

###########################################################
class Event_cards:
    def __init__(self, initial_deck):
        self.deck = initial_deck
        self.cards_drawn = 0
        self.current_card = []
        self.discard = []

    def draw_card(self):
        # initial event card only spawns genestealers
        if self.cards_drawn < 1:
            self.current_card.append(self.deck.pop(0))
            self.cards_drawn += 1
        else:
            prev_card = self.current_card.pop(0)
            self.discard.append(prev_card)
            self.current_card.append(self.deck.pop(0))
            self.cards_drawn += 1
        return self.current_card
        # RESOLVE EVENT ON CARD AFTER INITIAL TURN

    def draw(self):
        pass
        # TODO Will need another screen to show card and description


########################################################### DICE
# handles all dice rolls and placement
class Dice:
    def __init__(self, dice_default=112):
        self.sm_dice = {0: 0, 1: 16, 2: 32, 3: 48, 4: 64, 5: 80, 6: 96, 7: 112}
        self.u = dice_default

    def dice_roll(self):
        generate_roll = random.randint(0, 6)
        self.u = self.sm_dice.get(generate_roll)

    def draw(self):
        pyxel.blt(75, 10, 0, self.u, 48, 16, 16)


############################## SPACE MARINES
class Space_marines:
    def __init__(self):
        self.combat_teams = sm_deck  # LIST of DICTS
        self.name_x = 109
        self.name_y = (60, 96, 132, 168, 204, 240)
        self.portrait_x = 120
        self.portrait_y = (40, 76, 112, 148, 184, 220)
        self.left_arrow_x = 97  # border_x + 1
        self.right_arrow_x = 154  # left_x + 57
        self.arrow_y = (
            41,
            77,
            113,
            149,
            185,
            221,)  
        # border_y + 1 = 41 (41,77,113,149,185,221)
        self.atk_package = None

    def update(self):
        if pyxel.btnp(pyxel.KEY_9):
            print("space_marine.update() test")
        
        
    def defense(self, defending_marines):
        pass

    def atk_info_sort(self, attack_values):
        # [{3: [(2, ['tails', 'tails'])]}, {5: [(2, ['skulls', 'tails'])]}]
        atk_length = len(attack_values)
        if atk_length == 2:
            print('attack value = 2')
            atk_form_list = attack_values.keys()
            print(atk_form_list)
        elif atk_length == 1:
            print('attack value = 1')
        else:
            print('attack value = 0')
        
        # self.atk_package = attack_values
        



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

        gs_in_range = []
        for attacker in attacking_marines:
            lo_range = 1
            hi_range = 6

            lo_range = attacker.get("formation_num") - attacker.get("attk_range")
            if lo_range < 1:
                lo_range = 1
            hi_range = attacker.get("formation_num") + attacker.get("attk_range")
            if hi_range > 6:
                hi_range = 6

            left_dict = {}
            right_dict = {}

            if attacker.get("facing") == "LEFT":
                for row in left:
                    if row[0] + 1 in range(lo_range, hi_range + 1):
                        left_atker = attacker.get("formation_num")
                        if left_atker in left_dict:
                            left_dict[left_atker].append(row)
                        else:
                            left_dict[left_atker] = [row]


            if attacker.get("facing") == "RIGHT":
                for row in right:
                    if 6 - row[0] + 1 in range(lo_range, hi_range + 1):
                        right_atker = attacker.get("formation_num")
                        if right_atker in right_dict:
                            right_dict[right_atker].append(row)
                        else:
                            left_dict[right_atker] = [row]
            if left_dict:
                gs_in_range.append(left_dict)
            if right_dict:
                gs_in_range.append(right_dict)

        print(gs_in_range)
        return gs_in_range

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

    # TODO

    def draw(self, ac_selection=None):
        card_border_x = 96
        card_border_y = (40, 76, 112, 148, 184, 220)
        card_border_w = 65
        card_border_h = 33

        for marine in self.combat_teams:

            y_val = marine["formation_num"]
            col = marine["team_color"]
            sm_face = marine["visual"]
            sm_name = marine["sm_name"].split(" ")
            single_y = self.arrow_y[y_val - 1]

            # card border
            pyxel.rectb(card_border_x,
                        card_border_y[y_val - 1],
                        card_border_w,
                        card_border_h,
                        col,)
            
            # portrait
            pyxel.blt(self.portrait_x + 1,
                        self.portrait_y[y_val - 1],
                        0,
                        sm_face[0],
                        sm_face[1],
                        15,
                        16,)
            
            # portrait border
            pyxel.rectb(self.portrait_x, self.portrait_y[y_val - 1], 17, 17, 
                        col)
            # SM name 1
            pyxel.text(self.name_x, self.name_y[y_val - 1], f"{sm_name[0]}", 
                       col)
            # SM name 2
            pyxel.text(self.name_x - 2, self.name_y[y_val - 1] + 6, 
                       f"{sm_name[1]}", col)

            # facing arrows
            if marine["facing"] == "LEFT":
                pyxel.blt(self.left_arrow_x, single_y, 0, 0, 32, 6, 6)  # left ARROW 1
                pyxel.blt(self.left_arrow_x, single_y + 7, 0, 0, 32, 6, 6)  # 2
                pyxel.blt(self.left_arrow_x, single_y + 14, 0, 0, 32, 6, 6)  # 3

            else:
                pyxel.blt(self.right_arrow_x, single_y, 0, 10, 32, 6, 6)  # right ARROW 1
                pyxel.blt(self.right_arrow_x, single_y + 7, 0, 10, 32, 6, 6)  # 2
                pyxel.blt(self.right_arrow_x, single_y + 14, 0, 10, 32, 6, 6)  # 3

            if ac_selection:

                # card border
                pyxel.rectb(card_border_x + 1,
                            card_border_y[y_val - 1] - 1,
                            card_border_w + 1,
                            card_border_h + 1,
                            9)


            if self.atk_package:
                gs_left_x = 5
                gs_right_x = 183

                for atk in self.atk_package:
                    if atk[0] == 'LEFT':
                        #marine
                        pyxel.rectb(
                            card_border_x - 2,
                            card_border_y[atk[1]-1] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)
                        #gs
                        pyxel.rectb(
                            gs_left_x,
                            card_border_y[atk[4][0]] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)
                    elif atk[0] == 'RIGHT':
                        #marine
                        pyxel.rectb(
                            card_border_x - 2,
                            card_border_y[atk[1]-1] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)
                        #gs
                        pyxel.rectb(
                            gs_right_x,
                            card_border_y[atk[4][0]] - 2,
                            card_border_w + 4,
                            card_border_h + 4,
                            9)
                    else:
                        pyxel.rect(screen_x/2-25, screen_y/2-25, 50, 15, 8)
                        pyxel.text(screen_x/2-24, screen_y/2-25, "No Valid ATK", 7)


                    # left_or_right_data = (
                    #     attacker.get("facing"),
                    #     attacker.get("formation_num"),
                    #     lo_range,
                    #     hi_range,
                    #     row,)

                # [('RIGHT', 4, 2, 6, (3, ['stingray'])),
                # ('LEFT', 3, 1, 5, (0, ['claws', 'stingray']))]


###############################################################################


class Location_and_spawns:
    def __init__(self, gs_deck):

        self.locations_deck = create_location_deck()
        self.number_of_locations = len(self.locations_deck)
        self.room_number = 0
        self.location_name = self.locations_deck[self.room_number]["location"]
        # TODO self.location_condition = self.locations_deck[self.room_number]['condition']

        # VOID LOCK TRIANGLE VISUALS
        self.tri_dict = {"wt": (1, 128, 0), "yt": (1, 128, 8)}

        # VOID LOCK L TRIANGLE SPAWN COLOR AND NUMBER
        self.left_blip_num = self.locations_deck[0]["left_blip"]
        self.left_spawn_triangle = self.locations_deck[0]["l_triangle"]
        self.left_spawn_color, self.left_spawn_num = self.left_spawn_triangle.split("_")

        # VOID LOCK R TRIANGLE SPAWN COLOR AND NUMBER
        self.right_blip_num = self.locations_deck[0]["right_blip"]
        self.right_spawn_triangle = self.locations_deck[0]["r_triangle"]
        self.right_spawn_color, self.right_spawn_num = self.right_spawn_triangle.split(
            "_"
        )

        self.voidlock_spawns = {
            self.left_spawn_color: self.left_spawn_num,
            self.right_spawn_color: self.right_spawn_num,
        }
        # 'l_triangle': 'yt_2', 'r_triangle': 'wt_1'

        # GS DECK VARIABLES
        self.gs_deck = gs_deck
        self.left_gs_num = 0
        self.right_gs_num = 0
        self.left_gs_cards = []
        self.right_gs_cards = []

        self.gs_left_formation_num = []
        self.gs_right_formation_num = []

        self.gs_discard = []

        self.spawned_left_swarms = {
            0: {"terrain_color": None, "g_stealers": []},
            1: {"terrain_color": None, "g_stealers": []},
            2: {"terrain_color": None, "g_stealers": []},
            3: {"terrain_color": None, "g_stealers": []},
            4: {"terrain_color": None, "g_stealers": []},
            5: {"terrain_color": None, "g_stealers": []},
        }

        self.spawned_right_swarms = {
            0: {"terrain_color": None, "g_stealers": []},
            1: {"terrain_color": None, "g_stealers": []},
            2: {"terrain_color": None, "g_stealers": []},
            3: {"terrain_color": None, "g_stealers": []},
            4: {"terrain_color": None, "g_stealers": []},
            5: {"terrain_color": None, "g_stealers": []},
        }

        # TERRAIN VARIABLES
        # TERRAIN DICT WITH COLOR FOR ACCESSING
        self.terrain_imgs = {
            "corridor": (0, "green"),
            "artefact": (16, "green"),
            "control_panel": (32, "yellow"),
            "door": (48, "yellow"),
            "prom_tank": (64, "orange"),
            "dark_corner": (80, "orange"),
            "vent_duct": (96, "red"),
            "spore_chimney": (112, "red"),
        }

        # SORTS EACH TERRAIN CARD IN THE CURRENT LOCATION
        # [('door', 1, 'yellow'), ...]
        self.loc_terrain_1L = (
            self.locations_deck[self.room_number]["l_terrain_1"],  # NAME
            self.locations_deck[self.room_number]["d_l_terrain_1"] - 1,  # FORMATION
            self.terrain_imgs.get(self.locations_deck[self.room_number]["l_terrain_1"])[
                1
            ],
        )  # COLOR

        self.loc_terrain_2L = (
            self.locations_deck[self.room_number]["l_terrain_2"],
            self.locations_deck[self.room_number]["d_l_terrain_2"] - 1,
            self.terrain_imgs.get(self.locations_deck[self.room_number]["l_terrain_2"])[
                1
            ],
        )

        terrain_marker_1L = {"terrain_color": self.loc_terrain_1L[2]}
        terrain_marker_2L = {"terrain_color": self.loc_terrain_2L[2]}
        self.spawned_left_swarms[self.loc_terrain_1L[1]].update(terrain_marker_1L)
        self.spawned_left_swarms[self.loc_terrain_2L[1]].update(terrain_marker_2L)

        self.loc_terrain_1R = (
            self.locations_deck[self.room_number]["r_terrain_1"],
            self.locations_deck[self.room_number]["u_r_terrain_1"],
            self.terrain_imgs.get(self.locations_deck[self.room_number]["r_terrain_1"])[
                1
            ],
        )

        self.loc_terrain_2R = (
            self.locations_deck[self.room_number]["r_terrain_2"],
            self.locations_deck[self.room_number]["u_r_terrain_2"],
            self.terrain_imgs.get(self.locations_deck[self.room_number]["r_terrain_2"])[
                1
            ],
        )

        terrain_marker_1R = {"terrain_color": self.loc_terrain_1R[2]}
        terrain_marker_2R = {"terrain_color": self.loc_terrain_2R[2]}
        self.spawned_right_swarms[self.loc_terrain_1R[1]].update(terrain_marker_1R)
        self.spawned_right_swarms[self.loc_terrain_2R[1]].update(terrain_marker_2R)

        self.room_terrain = [
            self.loc_terrain_1L,
            self.loc_terrain_2L,
            self.loc_terrain_1R,
            self.loc_terrain_2R,
        ]

    ####
    def populate_blips(self):
        self.left_gs_cards = [self.gs_deck.pop(i) for i in range(self.left_blip_num)]
        self.left_gs_num = len(self.left_gs_cards)

        self.right_gs_cards = [self.gs_deck.pop(i) for i in range(self.right_blip_num)]
        self.right_gs_num = len(self.right_gs_cards)

    ####
    def location_card_draw(self):
        if self.room_number < self.number_of_locations - 1:
            self.room_number += 1
            self.location_name = self.locations_deck[self.room_number]["location"]
        # SORTS EACH TERRAIN CARD INTO THE 4 LOCATIONS
        self.loc_terrain_1L = (
            self.locations_deck[self.room_number]["l_terrain_1"],  # NAME
            self.locations_deck[self.room_number]["d_l_terrain_1"],  # FORMATION
            self.terrain_imgs.get(self.locations_deck[self.room_number]["l_terrain_1"])[
                1
            ],
        )  # COLOR

        self.loc_terrain_2L = (
            self.locations_deck[self.room_number]["l_terrain_2"],
            self.locations_deck[self.room_number]["d_l_terrain_2"],
            self.terrain_imgs.get(self.locations_deck[self.room_number]["l_terrain_2"])[
                1
            ],
        )

        self.loc_terrain_1R = (
            self.locations_deck[self.room_number]["r_terrain_1"],
            self.locations_deck[self.room_number]["u_r_terrain_1"],
            self.terrain_imgs.get(self.locations_deck[self.room_number]["r_terrain_1"])[
                1
            ],
        )

        self.loc_terrain_2R = (
            self.locations_deck[self.room_number]["r_terrain_2"],
            self.locations_deck[self.room_number]["u_r_terrain_2"],
            self.terrain_imgs.get(self.locations_deck[self.room_number]["r_terrain_2"])[
                1
            ],
        )

        self.room_terrain = [
            self.loc_terrain_1L,
            self.loc_terrain_2L,
            self.loc_terrain_1R,
            self.loc_terrain_2R,
        ]

    ####
    def gs_spawn_locs(self, drawn_event_card):
        """
        Grabs the EVENT CARD's spawn colors and triangles, then sorts the number of cards from the L or R blip piles
        each TERRAIN color shown on the EVENT CARD color will get.

        Returns
        -------
        left_spawn_info : TYPE
            DESCRIPTION.
        right_spawn_info : TYPE
            DESCRIPTION.

        """

        self.drawn_event_card = drawn_event_card
        # [{'Card Name': 'Full Scan',
        #   'Card Effect': 'INSTINCT: Choose a blip pile, DISCARD the top card of this pile.',
        #   'L Spawn': 'yt_red',
        #   'R Spawn': 'yt_yellow',

        # TODO will need to read and act on the event card info below after INITIAL EVENT CARD DRAW
        #   'GS Maneuver ': 'up_down_chevrons',
        #   'GS Emblem': 'stingray',
        #   'card_num': 6}]

        # TRIANGLE NUMBER AND TERRAIN COLOR FOR CURRENT EVENT CARD
        left_event_card_tri, left_event_card_color = (
            self.drawn_event_card[0].get("L Spawn").split("_")
        )
        right_event_card_tri, right_event_card_color = (
            self.drawn_event_card[0].get("R Spawn").split("_")
        )

        event_card_spawns = [
            (self.voidlock_spawns.get(left_event_card_tri), left_event_card_color),
            (self.voidlock_spawns.get(right_event_card_tri), right_event_card_color),
        ]

        swarm_spawn_sides = {
            "left1": None,
            "left2": None,
            "right1": None,
            "right2": None,
        }

        for terrain in [self.room_terrain[0], self.room_terrain[1]]:
            if event_card_spawns[0][1] == terrain[2]:
                left_info1 = {
                    "left1": (event_card_spawns[0][0], event_card_spawns[0][1])
                }
                swarm_spawn_sides.update(left_info1)
            if event_card_spawns[1][1] == terrain[2]:
                left_info2 = {
                    "left2": (event_card_spawns[1][0], event_card_spawns[1][1])
                }
                swarm_spawn_sides.update(left_info2)
        # CHECKS RIGHT TERRAINS FOR SPAWNS
        for terrain in [self.room_terrain[2], self.room_terrain[3]]:
            # print(terrain[2]) # color
            if event_card_spawns[0][1] == terrain[2]:
                right_info1 = {
                    "right1": (event_card_spawns[0][0], event_card_spawns[0][1])
                }
                swarm_spawn_sides.update(right_info1)
            if event_card_spawns[1][1] == terrain[2]:
                right_info2 = {
                    "right2": (event_card_spawns[1][0], event_card_spawns[1][1])
                }
                swarm_spawn_sides.update(right_info2)
        return swarm_spawn_sides
        # [('2', 'red'), ('1', 'yellow')]

    ####
    def populate_GS_spawns(self, swarm_spawn_sides):
        """
        matches terrain_color with event card color
        and places cards from each blip pile into it's side's spawns.

        Returns
        -------
        None.

        """
        # swarm_spawn_sides =    {'left1': ('2', 'yellow'),
        # 'left2': None,
        # 'right1': None,
        # 'right2': ('1', 'red')}

        spawn_placement = {"left": [], "right": []}
        sides = ["left1", "left2", "right1", "right2"]

        for side in sides:
            print(f"side in sides = {swarm_spawn_sides[side]}")
            if swarm_spawn_sides[side] != None:
                if side in ["left1", "left2"]:
                    spawn_placement["left"].append(swarm_spawn_sides[side])
                else:
                    if side in ["right1", "right2"]:
                        spawn_placement["right"].append(swarm_spawn_sides[side])
            else:
                del swarm_spawn_sides[side]
        if spawn_placement["left"]:
            for spawn in spawn_placement["left"]:
                left_spawn_amount = int(spawn[0])
                left_spawn_color = spawn[1]

                for spawn in self.spawned_left_swarms:
                    if (
                        self.spawned_left_swarms[spawn]["terrain_color"]
                        == left_spawn_color
                    ):
                        for i in range(left_spawn_amount):
                            self.left_blip_num -= 1
                            each_spawn = self.left_gs_cards.pop(0)
                            self.spawned_left_swarms[spawn]["g_stealers"].append(
                                each_spawn
                            )
        for key in self.spawned_left_swarms:
            if self.spawned_left_swarms[key]["g_stealers"]:
                print(
                    f"the L formation number is {key} and its value is {self.spawned_left_swarms[key]['g_stealers']}"
                )
                # self.gs_left_formation_num = key
                self.gs_left_formation_num.append(key)
        if spawn_placement["right"]:
            for spawn in spawn_placement["right"]:
                right_spawn_amount = int(spawn[0])
                right_spawn_color = spawn[1]

                for spawn in self.spawned_right_swarms:
                    if (
                        self.spawned_right_swarms[spawn]["terrain_color"]
                        == right_spawn_color
                    ):
                        for i in range(right_spawn_amount):
                            self.right_blip_num -= 1
                            each_spawn = self.right_gs_cards.pop(0)
                            self.spawned_right_swarms[spawn]["g_stealers"].append(
                                each_spawn
                            )
        for key in self.spawned_right_swarms:
            if self.spawned_right_swarms[key]["g_stealers"]:
                print(
                    f"the R formation number is {key} and its value is {self.spawned_right_swarms[key]['g_stealers']}"
                )
                # self.gs_right_formation_num = key
                self.gs_right_formation_num.append(key)

    # self.spawned_left_swarms = {0: {'terrain_color': None, 'g_stealers': []},
    # self.left_gs_cards = ['Stingray', 'Claw', 'Claw']

    ####
    def draw(self):
        # LOCATION CARD TRIANGLE INFO DRAW
        pyxel.rectb(96, 4, 65, 33, 7)  # LOCATION card border rectangle
        pyxel.text(111, 30, self.location_name, 7)  # LOCATION TEXT (ie "VOID LOCK")

        # LOCATION CARD TRIANGLE INFO DRAW
        left_tri = self.tri_dict.get(self.left_spawn_color)
        left_tri_img = left_tri[0]
        left_tri_x = left_tri[1]
        left_tri_y = left_tri[2]

        right_tri = self.tri_dict.get(self.right_spawn_color)
        right_tri_img = right_tri[0]
        right_tri_x = right_tri[1]
        right_tri_y = right_tri[2]

        pyxel.blt(97, 20, left_tri_img, left_tri_x, left_tri_y, 16, 8)
        pyxel.text(104, 21, self.left_spawn_num, 8)
        pyxel.blt(144, 20, right_tri_img, right_tri_x, right_tri_y, 16, 8)
        pyxel.text(150, 21, self.right_spawn_num, 0)

        # BLIP PILE DRAW
        pyxel.blt(21, 4, 0, 192, 48, 32, 32)  # LEFT BLIP "SONAR" VISUAL
        pyxel.text(36, 18, str(self.left_blip_num), 7)  # LEFT BLIP NUMBER

        pyxel.blt(204, 4, 0, 192, 48, 32, 32)  # RIGHT BLIP "SONAR" VISUAL
        pyxel.text(218, 18, str(self.right_blip_num), 7)  # RIGHT BLIP NUMBER

        # TERRAIN DRAW
        # IMAGES HAVE DANGER LEVEL (COLOR) BELOW THEM (EACH IMAGE HAS A 'H' VALUE OF 32)

        terrain_left_x = 75  # X COORDINATE FOR ALL LEFT TERRAIN PLACEMENTS
        terrain_right_x = 166  # X COORDINATE FOR ALL RIGHT TERRAIN PLACEMENTS
        terrain_y = (
            40,
            76,
            112,
            148,
            184,
            220,
        )  # Y COORDINATE FOR ALL TERRAIN PLACEMENTS

        left1_img = self.terrain_imgs.get(
            self.loc_terrain_1L[0]
        )  # ACCESSES DICT ABOVE BY TERRAIN NAME (SELF.loc_terrain_1L) GETTING ITS FORMATION NUMBER
        left2_img = self.terrain_imgs.get(self.loc_terrain_2L[0])
        left1_formation_num = self.loc_terrain_1L[
            1
        ]  # THE NUMBER EACH TERRAIN CARD WILL BE PLACED ON THE LEFT AND RIGHT OF THE FORMATION
        left2_formation_num = self.loc_terrain_2L[1]

        right1_img = self.terrain_imgs.get(self.loc_terrain_1R[0])
        right2_img = self.terrain_imgs.get(self.loc_terrain_2R[0])
        right1_formation_num = 6 - self.loc_terrain_1R[1]
        right2_formation_num = 6 - self.loc_terrain_2R[1]

        ##PACKAGES ALL TERRAIN INFO ABOVE AND CREATES EACH TERRAIN IMG AND PLACEMENT PER LOCATION CARD
        # pyxel.blt(x, y, img, u, v, w, h)
        left_loc_1 = pyxel.blt(
            terrain_left_x, terrain_y[left1_formation_num], 1, left1_img[0], 0, 16, 32
        )

        left_loc_2 = pyxel.blt(
            terrain_left_x, terrain_y[left2_formation_num], 1, left2_img[0], 0, 16, 32
        )

        right_loc_1 = pyxel.blt(
            terrain_right_x,
            terrain_y[right1_formation_num],
            1,
            right1_img[0],
            0,
            16,
            32,
        )

        right_loc_2 = pyxel.blt(
            terrain_right_x,
            terrain_y[right2_formation_num],
            1,
            right2_img[0],
            0,
            16,
            32,
        )

        ### GS IMAGE COORDINATES ON IMAGE BANK
        gs_img = 96
        swarm_dict = {
            "tails": 112,
            "skulls": 128,
            "claws": 144,
            "stingray": 160,
        }

        gs_left_x = (52, 35, 18, 1)  # X COORDINATES FOR LEFT SIDE GS PORTRAITS, R to L
        gs_right_x = (
            188,
            205,
            222,
            239,
        )  # X COORDINATES FOR RIGHT SIDE GS PORTRAITS, L to R
        gs_img_y = (
            40,
            76,
            112,
            148,
            184,
            220,
        )  # Y COORDINATES FOR ALL GS IMAGES, TOP TO BOTTOM
        gs_team_y = (
            57,
            93,
            129,
            165,
            201,
            237,
        )  # Y COORDINATES FOR ALL GS TEAM IMAGES, TOP TO BOTTOM

        for left_swarms in self.spawned_left_swarms:
            if self.spawned_left_swarms[left_swarms]["g_stealers"]:
                row_number = 0
                for gs_left_team in self.spawned_left_swarms[left_swarms]["g_stealers"]:
                    pyxel.blt(
                        gs_left_x[row_number],
                        gs_img_y[left_swarms],
                        0,
                        gs_img,
                        0,
                        16,
                        16,
                    )
                    pyxel.blt(
                        gs_left_x[row_number],
                        gs_team_y[left_swarms],
                        0,
                        swarm_dict.get(gs_left_team),
                        0,
                        16,
                        16,
                    )
                    row_number += 1
        for right_swarms in self.spawned_right_swarms:
            if self.spawned_right_swarms[right_swarms]["g_stealers"]:
                row_number = 0
                for gs_right_team in self.spawned_right_swarms[right_swarms][
                    "g_stealers"
                ]:
                    pyxel.blt(
                        gs_right_x[row_number],
                        gs_img_y[6 - right_swarms],
                        0,
                        gs_img,
                        0,
                        16,
                        16,
                    )
                    pyxel.blt(
                        gs_right_x[row_number],
                        gs_team_y[6 - right_swarms],
                        0,
                        swarm_dict.get(gs_right_team),
                        0,
                        16,
                        16,
                    )
                    row_number += 1


#### # # # # # # #####
# ACTION CARD WINDOW #
#### # # # # # # #####
# ACTION#    #SUPPORT#   #MOVE + ACTION#
# red_team_ac_cards =   (16, 0),    (88, 0),    (160, 0)
# green_team_ac_cards = (16, 86),   (88, 86),   (160, 86)
# grey_team_ac_cards =  (16, 172),  (88, 172),  (160, 172)


class Action_cards:
    def __init__(self):
        self.all_action_cards = act_cards.all_sm_action_cards
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


class Roll_screen:
    def __init__(self):
        self.attacking_info = None
        ### DICE
        self.dice = Dice()

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            print("dice roll test")
            self.dice.dice_roll()
        if pyxel.btnp(pyxel.KEY_W):
            print("up pressed")

    def draw(self):
        self.dice.draw()


################################################
################## MAIN APP ####################
################################################
class App:
    def __init__(self):
        pyxel.init(screen_x, screen_y, title="SPACE HULK: DEATH ANGEL", fps=30)
        pyxel.load("sh_da.pyxres")
        pyxel.mouse(True)

        ### WINDOW STATES
        self.window_state = 0
        # 0 = Main Game Screen
        # 1 = Action Card Screen
        # 2 = Resolve Actions (Main Game Screen w/overlay for actions)
        # 3 = Attack/Defend Confrontation (Dice Roll)

        ### SPACE MARINES
        self.space_marines = Space_marines()

        self.location_and_spawns = Location_and_spawns(gs_deck)
        self.event_cards = Event_cards(event_deck)
        self.drawn_event_card = self.event_cards.draw_card()

        self.location_and_spawns.populate_blips()

        initial_spawns = self.location_and_spawns.gs_spawn_locs(self.drawn_event_card)
        self.location_and_spawns.populate_GS_spawns(initial_spawns)

        self.action_cards = Action_cards()
        self.ac_count = 0

        self.roll_screen = Roll_screen()
        self.atk_package = None

        pyxel.run(self.update, self.draw)

    # combat_teams = [
    #                 {'sm_name':'Lexicanium Calistarius',
    #                  'team_color': 13,
    #                  'visual': (0,0),
    #                  'attk_range': 2,
    #                  'facing': 'setup',
    #                  'formation_num': 0,
    #                  'status': 'alive',
    #                  'support_token': 0},

    def organize_acards(self):
        acards = self.action_cards.sort_card_numbers()
        # acards = {1: (8, 'attack_card'), 8: (3, 'support_card'), 17: (13, 'move_act_card')}
        return acards

    def update(self):
        if self.window_state == 0:  # Main Game Window
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            if pyxel.btnp(pyxel.KEY_Z):
                self.location_and_spawns.location_card_draw()
                self.drawn_event_card = self.event_cards.draw_card()
                self.location_and_spawns.gs_spawn_locs(self.drawn_event_card)
            if pyxel.btnp(pyxel.KEY_N) and self.window_state == 0:
                self.window_state = 1  # Opens Action Card Window
        elif self.window_state == 1:
            self.action_cards.update()
            if pyxel.btnp(pyxel.KEY_N) and self.action_cards.confirm_choices == 0:
                self.window_state = 0
            if self.action_cards.confirm_choices == 2:
                self.window_state = 2  # Starts Resolve Action Phase
        if self.window_state == 2:
            actions = App.organize_acards(self)
            a_list = [a for a, v in actions.items()]
            # card_dict = {17: (8, 'attack_card'), 16: (3, 'attack_card'), 15: (13, 'attack_card')}
            total_actions = len(actions)
            sm = self.space_marines.combat_teams

            # TODO: CUE UP 1st ACTION CARD AND FLIP BETWEEN SM SELECTIONS WITH ORANGE BOX
            # add selection WASD, ENTER into each card type to control selectors
            if self.ac_count <= total_actions and pyxel.btnp(pyxel.KEY_RETURN):

                cardtype = actions.get(a_list[self.ac_count])[1]
                cardteam = actions.get(a_list[self.ac_count])[0]

                if cardtype == "attack_card":
                    lgs = self.location_and_spawns.spawned_left_swarms
                    rgs = self.location_and_spawns.spawned_right_swarms
                    attacking_marines = [s for s in sm if 
                                         s["team_color"] == cardteam]

                    attack_values = self.space_marines.attack_prep(
                        attacking_marines, lgs, rgs)

                    self.space_marines.atk_info_sort(attack_values)


                elif cardtype == "support_card":
                    # self.space_marines.support(supporting_marines)
                    print("support")
                else:
                    if cardtype == "move_act_card":
                        # self.space_marines.move_action(move_marines) #action_marines?
                        print("action+move")
            
                self.ac_count += 1
            self.space_marines.update()
                

    def draw(self):
        if self.window_state == 0:
            pyxel.clip()
            pyxel.cls(0)
            ## GRID
            if draw_grid == "Y":
                build_grid(screen_x, screen_y)
            ##################################

            self.space_marines.draw()
            self.location_and_spawns.draw()
        if self.window_state == 1:
            self.action_cards.draw()
        if self.window_state == 2:
            pyxel.clip()
            pyxel.cls(0)
            self.location_and_spawns.draw()
            self.space_marines.draw()
            self.roll_screen.draw()

            # TODO


###############################################################################
App()
