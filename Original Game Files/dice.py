import pyxel
import random


screen_x = 256 #16 16-pixel chunks wide
screen_y = 256 #16 16-pixel chunks wide


sm_dice = {0:0, 1:16, 2:32, 3:48, 4:64, 5:80, 6:96, 7:112}


# handles all dice rolls and placement
class Dice:
    def __init__(self, dice_default=112):
        self.x = 128 #90 --pushing this off to the side/bottom while other game objects are created.
        self.y = 240 #10 --^^^^
        self.img_page = 0
        self.w = 16
        self.h = 16
        self.u = dice_default
        self.v = 48

    def dice_roll(self):
        generate_roll = random.randint(0, 6)
        print(generate_roll)        
        self.u = sm_dice.get(generate_roll)

    
    def draw(self):
        pyxel.blt(self.x, 
                  self.y, 
                  self.img_page, 
                  self.u,
                  self.v, 
                  self.w, 
                  self.h)


###############################################################################
###############################################################################
class App:
    def __init__(self):
        pyxel.init(screen_x, screen_y)
        pyxel.load('sh_da.pyxres')
        self.dice = Dice()
        
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.dice_value = self.dice.dice_roll()       


    def draw(self):
        pyxel.cls(0)
        
        self.dice.draw()
  
App()
###############################################################################
###############################################################################
