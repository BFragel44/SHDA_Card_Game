import random
import pandas as pd
import pyxel

## INITIAL LOCATION DECK CREATION
def create_location_deck():
    """
    ----------
    Parameters:
    None
    ----------
    Purpose:
    pulls location data from the CSV and sorts/shuffles each location into
    a main location deck - complete with the VOID LOCK on top to start.
    ----------
    Returns:
    final_locs
    """
    final_locs = []
    data = "project_rework\location_cards.csv"
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
        self.right_spawn_color, self.right_spawn_num = self.right_spawn_triangle.split("_")

        self.voidlock_spawns = {
            self.left_spawn_color: self.left_spawn_num,
            self.right_spawn_color: self.right_spawn_num,}
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
            i: {"terrain_color": None, "g_stealers": []} for i in range(6)}
        self.spawned_right_swarms = {
            i: {"terrain_color": None, "g_stealers": []} for i in range(6)}

        # self.spawned_left_swarms = {
        #     0: {"terrain_color": None, "g_stealers": []},
        #     1: {"terrain_color": None, "g_stealers": []},
        #     2: {"terrain_color": None, "g_stealers": []},
        #     3: {"terrain_color": None, "g_stealers": []},
        #     4: {"terrain_color": None, "g_stealers": []},
        #     5: {"terrain_color": None, "g_stealers": []},
        # }
        # self.spawned_right_swarms = {
        #     0: {"terrain_color": None, "g_stealers": []},
        #     1: {"terrain_color": None, "g_stealers": []},
        #     2: {"terrain_color": None, "g_stealers": []},
        #     3: {"terrain_color": None, "g_stealers": []},
        #     4: {"terrain_color": None, "g_stealers": []},
        #     5: {"terrain_color": None, "g_stealers": []},
        # }

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
                # self.gs_right_formation_num = key
                self.gs_right_formation_num.append(key)

    # self.spawned_left_swarms = {0: {'terrain_color': None, 'g_stealers': []},
    # self.left_gs_cards = ['Stingray', 'Claw', 'Claw']

    ####
    def _draw(self):
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
