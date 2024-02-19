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
        self.dice.roll_result = None
        self.gs_anim_x = 150
        self.gs_sprite_u = 32
        self.gs_sprite_h = 32
        self.gs_anim_y = 45
        self.gs_sprite_v = 64

    def screen_update(self):
        self.dice.dice_update()
        # DICE ROLLING (phase 1 probably not needed here...)
        # if self.dice.roll_phase == 1:
        #     pass
        if self.dice.roll_phase == 2:
            hit = [1, 2, 3]
            miss = [0, 4, 5, 6]
            if self.dice.roll_result in hit:
                self.gs_sprite_u = 96
                self.gs_sprite_h = 16
                self.gs_anim_y = 62
                # add in GS remove method
            elif self.dice.roll_result in miss:
                self.gs_sprite_u = 96
                self.gs_sprite_v = 80
            self.dice.roll_phase = 3

    def screen_draw(self):
        # 197 x 197 mini screen ((12.31 pyxres blocks tall/wide))
        pyxel.cls(0)
        pyxel.clip(20, 20, 217, 217)
        pyxel.rectb(20, 20, 217, 217, 8)
        # pyxel.blt(32, 45, 0, 0, 64, 191, 255)
        # SM and GS sprites:
        pyxel.blt(45, 45, 0, 0, 64, 32, 32)
        pyxel.blt(self.gs_anim_x, self.gs_anim_y, 0, self.gs_sprite_u, 
                  self.gs_sprite_v, 64, self.gs_sprite_h, 0)
        # DICE ROLLING
        if self.dice.roll_phase == 1:
            # GS movement
            self.gs_anim_x -= 1.5
            if self.dice.roll_anim_counter % 5 == 0:
                # muzzle flash and SFX
                pyxel.play(0, 13, loop=False)
                pyxel.blt(75, 53, 0, 48, 16, 16, 16, 0)
        if self.dice.roll_phase == 2:
            hit = [1, 2, 3]
            miss = [0, 4, 5, 6]
            if self.dice.roll_result in hit:
                # Hit SFX
                pyxel.play(0, 14, loop=False)
            elif self.dice.roll_result in miss:
                # Miss SFX
                pyxel.play(0, 15, loop=False)
        
        self.dice.dice_draw()


class Dice:
    def __init__(self, dice_default=112):
        self.u = dice_default
        self.sm_dice = {0: 0, 1: 16, 2: 32, 3: 48, 
                        4: 64, 5: 80, 6: 96, 7: 112}
        self.dice_pos = [120, 29, 16, 16] # [x, y, w, h]
        self.roll_result = None
        self.roll_anim_counter = 0
        self.roll_phase = 0


    def dice_roll(self):
        generate_roll = random.randint(0, 6)
        self.roll_result = generate_roll
        self.u = self.sm_dice.get(generate_roll)

    def dice_update(self):
        if self.roll_phase == 0 and box_click(self.dice_pos[0], 
                                            self.dice_pos[1], 
                                            self.dice_pos[2], 
                                            self.dice_pos[3]):
            self.roll_phase = 1
        
        if self.roll_phase == 1:
            self.roll_anim_counter += 1
            if self.roll_anim_counter < 50:  
                self.u = self.sm_dice.get(self.roll_anim_counter % 6)

            else:
                self.dice_roll()
                print(f"{self.roll_result = }")
                self.roll_phase = 2
            
    def dice_draw(self):
        pyxel.blt(self.dice_pos[0], self.dice_pos[1], 0, self.u, 48, 
                  self.dice_pos[2], self.dice_pos[3])