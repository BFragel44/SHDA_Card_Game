import pyxel
import random

select_box = [96, 4, 65, 33,]

def box_click(x: int, y: int, w: int, h: int):
    """
    Helper function that returns True if
    mouse click is registered within the
    boundaries.

    Args:
        x (int): rectangle x value
        y (int): rectangle y value
        w (int): rectangle width value
        h (int): rectangle height value

    Returns:
        boolean: True if mouse click registers within boundaries
    """    
    x2 = x+w
    y2 = y+h
    if (pyxel.mouse_x > x and 
        pyxel.mouse_x < x2 and 
        pyxel.mouse_y > y and 
        pyxel.mouse_y < y2):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True
    return False

def phase_box_click():
    """
    Helper function that returns True if
    mouse click is registered within the
    boundaries of the "Phase Box".

    Returns:
        boolean: True if mouse click registers within boundaries
    """
    x = select_box[0]
    y = select_box[1]
    w = select_box[2]
    h = select_box[3]
    x2 = x+w
    y2 = y+h
    if box_click(x, y, w, h):
        return True
    return False


class RollScreen:
    def __init__(self, facing, sm_formation, gs_formation):
        self.facing = facing
        self.sm_formation_num = sm_formation
        self.gs_formation_num = gs_formation
        self.dice = Dice()

    def screen_update(self):
        self.dice.dice_update()

    def screen_draw(self):
        pyxel.cls(0)
        pyxel.clip(20, 20, 217, 217)
        pyxel.rectb(20, 20, 217, 217, 8)
        self.dice.dice_draw()


class Dice:
    def __init__(self, dice_default=112):
        self.sm_dice = {0: 0, 1: 16, 2: 32, 3: 48, 
                        4: 64, 5: 80, 6: 96, 7: 112}
        self.u = dice_default
        self.dice_pos = [120, 25, 16, 16] # [x, y, w, h]

    def dice_roll(self):
        generate_roll = random.randint(0, 6)
        self.u = self.sm_dice.get(generate_roll)

    def dice_update(self):
        if box_click(self.dice_pos[0], self.dice_pos[1], 
                     self.dice_pos[2], self.dice_pos[3]):
            self.dice_roll()

    def dice_draw(self):
        pyxel.blt(self.dice_pos[0], self.dice_pos[1], 0, self.u, 48, 
                  self.dice_pos[2], self.dice_pos[3])