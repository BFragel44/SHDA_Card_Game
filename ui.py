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
    def __init__(self, facing, sm_formation, sm_tokens, gs_formation, gs_swarm_num):
        self.facing = facing
        self.sm_formation_num = sm_formation
        self.sm_tokens = sm_tokens
        self.gs_formation_num = gs_formation
        self.gs_swarm_num = gs_swarm_num
        self.dice = Dice()
        self.dice.roll_result = None
        self.gs_anim_x = 150
        self.gs_sprite_u = 32
        self.gs_sprite_h = 32
        self.gs_anim_y = 45
        self.gs_sprite_v = 64
        self.gs_hit = False
        self.hit_values = None
        self.sound_played = False

    def re_roll(self):
        pyxel.cls(0)
        self.sm_tokens -= 1
        self.dice.roll_phase = 0
        self.dice.roll_anim_counter = 0
        self.dice.roll_result = None
        self.gs_anim_x = 150
        self.gs_sprite_u = 32
        self.gs_sprite_h = 32
        self.gs_anim_y = 45
        self.gs_sprite_v = 64
        self.gs_hit = False
        self.sound_played = False
        self.dice = Dice()


    def hit_miss_update(self):
        hit = [1, 2, 3]
        miss = [0, 4, 5, 6]
        if self.dice.roll_result in hit:
            self.gs_sprite_u = 96
            self.gs_sprite_h = 16
            self.gs_anim_y = 62
            self.gs_hit = True
            self.hit_values = [self.facing, self.gs_formation_num, 
                                self.gs_swarm_num]
            # pyxel.clip()
        elif self.dice.roll_result in miss:
            self.gs_sprite_u = 96
            self.gs_sprite_v = 80
####
# Main Update Method
    def screen_update(self):
        self.dice.dice_update()
        if self.dice.roll_phase == 2:
            self.hit_miss_update()
        elif self.dice.roll_phase == 3:
            if self.sm_tokens > 0:
                # print("re-roll phase")
                pass


    def roll_ui_draw(self):
        # 197 x 197 mini screen ((12.31 pyxres blocks tall/wide))
        pyxel.cls(0)
        pyxel.clip(20, 20, 217, 217)
        pyxel.rectb(20, 20, 217, 217, 8)
        # Support Token text:
        pyxel.text(60, 80, f"Support Tokens: {self.sm_tokens}", 7)
        # SM sprite:
        pyxel.blt(45, 45, 0, 0, 64, 32, 32, 0)
        # GS sprite:
        pyxel.blt(self.gs_anim_x, self.gs_anim_y, 0, self.gs_sprite_u, 
                  self.gs_sprite_v, 64, self.gs_sprite_h, 0)
    
    def roll_sprites_draw(self):
        if self.dice.roll_anim_counter < 50:
            # GS movement and muzzle flash
            self.gs_anim_x -= 1.5
            if self.dice.roll_anim_counter % 5 == 0:
                # SM muzzle flash and SFX
                pyxel.play(0, 13, loop=False)
                pyxel.blt(75, 53, 0, 48, 16, 16, 16, 0)

    def roll_result_sfx(self):
        hit = [1, 2, 3]
        miss = [0, 4, 5, 6]
        sample = [14, 15]
        if self.dice.roll_result in hit:
            # Hit SFX
            sample = sample[0]
        elif self.dice.roll_result in miss:
            # Miss SFX
            sample = sample[1]
        if not self.sound_played and pyxel.play_pos(1) is None:
            self.sound_played = True
            pyxel.play(1, sample, loop=False)
            self.dice.roll_phase = 3

    def post_roll_options(self):
        # PROCEED OPTION BOX
        pyxel.rectb(109, 110, 40, 10, 8)
        pyxel.text(115, 112, "Proceed", 7)
        # RE-ROLL OPTION BOX
        if self.sm_tokens > 0 and self.gs_hit == False:
            pyxel.rectb(109, 125, 40, 10, 8)
            pyxel.text(114, 127, "Re-roll?", 7)
            # RE-ROLL BOX CLICKED
            if box_click(100, 125, 40, 10):
                print("Re-roll box clicked")
                self.re_roll()
                self.dice.roll_phase = 0
        # PROCEED BOX CLICKED
        if box_click(100, 110, 40, 10):
            print("Proceed box clicked")
            self.dice.roll_phase = 5
            

####
# Main Draw Method
    def screen_draw(self):
        self.roll_ui_draw()       
        self.dice.dice_draw()
        # DICE ROLLING
        if self.dice.roll_phase == 1:
            self.roll_sprites_draw()
        if self.dice.roll_phase == 2:
            self.roll_result_sfx()
        if self.dice.roll_phase == 3:
            self.post_roll_options()
            
            
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
        if self.roll_phase == 0 and box_click(
                                        self.dice_pos[0], self.dice_pos[1], 
                                        self.dice_pos[2], self.dice_pos[3]):
            self.roll_phase = 1      
        if self.roll_phase == 1:
            self.roll_anim_counter += 1
            if self.roll_anim_counter < 50:  
                self.u = self.sm_dice.get(self.roll_anim_counter % 6)
            elif self.roll_anim_counter == 50:
                self.dice_roll()
            else:
                self.roll_phase = 2
                print("dice roll complete")
      
    def dice_draw(self):
        pyxel.blt(self.dice_pos[0], self.dice_pos[1], 0, self.u, 48, 
                  self.dice_pos[2], self.dice_pos[3])
