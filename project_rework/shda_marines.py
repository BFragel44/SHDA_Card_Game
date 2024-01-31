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
        'support_tokens': 0,
        'team_id': 1,},

    {'sm_name':'Brother Scipio',
        'team_color': 13,
        'visual': (0, 16), 
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_tokens': 0,
        'team_id': 2,},

    {'sm_name':'Sargeant Gideon',
        'team_color': 3,
        'visual': (16, 0),  
        'attk_range': 0, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_tokens': 0,
        'team_id': 1,},

    {'sm_name':'Brother Noctis',
        'team_color': 3,
        'visual': (16, 16),              
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_tokens': 0,
        'team_id': 2,},

    {'sm_name':'Brother Leon',
        'team_color': 8,
        'visual': (32, 0),    
        'attk_range': 3, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_tokens': 0,
        'team_id': 1,},

    {'sm_name':'Brother Valencio',
        'team_color': 8,
        'visual': (32, 16),
        'attk_range': 2, 
        'facing': 'setup',
        'formation_num': 0,
        'status': 'alive',
        'support_tokens': 0,
        'team_id': 2,}]

sm_visual_dimms = {
    "name_x": 109,
    "name_y": (60, 96, 132, 168, 204, 240),
    "portrait_x": 120,
    "portrait_y": (40, 76, 112, 148, 184, 220),
    "left_arrow_x": 97,
    "right_arrow_x": 154,
    "arrow_y": (41, 77, 113, 149, 185, 221),
    "card_border_x": 96,
    "card_border_y": [40, 76, 112, 148, 184, 220],
    "card_border_w": 65,
    "card_border_h": 33}

def shuffle_deck(combat_teams):
    """
    Assigns random formation numbers to each marine and sets their facing direction.

    This function shuffles a list of formation numbers and assigns them to marines in the combat_teams list.
    If the formation number <= 3, the marine's facing direction is set to 'LEFT'.
    Otherwise, it's set to 'RIGHT'.

    Args:
        combat_teams (list): A list of dictionaries where each dictionary represents a marine.
                             Each dictionary must have 'formation_num' and 'facing' keys.

    Returns:
        list: The updated list of marines with assigned formation numbers and facing directions.
    """   
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
        self.test = 0

    def formation_update(self):
        pass


    def formation_draw(self):
        """
        Draws the marine formation on the main game layout
        """
        for roster_dict in self.combat_teams:
            y_val = roster_dict["formation_num"]
            col = roster_dict["team_color"]
            sm_face = roster_dict["visual"]
            sm_name = roster_dict["sm_name"].split(" ")
            single_y = sm_visual_dimms["arrow_y"][y_val - 1]
            attack_range = roster_dict["attk_range"]
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
            # sm attack range
            pyxel.text(sm_visual_dimms["portrait_x"] - 10,
                        sm_visual_dimms["portrait_y"][y_val - 1] + 2, f"{attack_range}", col)
            # SM Support Token Count
            pyxel.text(sm_visual_dimms["portrait_x"] + 24,
                        sm_visual_dimms["portrait_y"][y_val - 1] + 2, f"{roster_dict['support_tokens']}", col)
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
