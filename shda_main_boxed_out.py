import pyxel
import random
import shda_marines as marines

# https://github.com/kitao/pyxel
# https://opensource.com/article/17/12/game-python-add-a-player
# https://images-cdn.fantasyflightgames.com/ffg_content/death-angel/minisite/support/death-angel-rulebook-web.pdf
# https://cf.geekdo-images.com/wgVoDUrcLEf3mAYSb55bAw__imagepagezoom/img/ZolOCJCryFNHg3kgaK8sTf93_m0=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic5794897.jpg
# https://boardgamegeek.com/boardgame/71721/space-hulk-death-angel-card-game/forums/66     
# https://cf.geekdo-images.com/n4yO7c7uX4a5xRMtjoZE7w__imagepagezoom/img/lAdcGzBGz_XxV3IapPB7j2xlbDI=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic826186.jpg

# https://github.com/CaffeinatedTech/Python_Nibbles/blob/012d023b4d39e56b1131c13908cbbb9f64d14e7c/main.py#L42
# https://www.youtube.com/watch?v=Qg16VhEo2Qs


screen_x = 257 #16 16-pixel chunks wide
screen_y = 257 #16 16-pixel chunks wide

sm_dice = {0:0, 1:16, 2:32, 3:48, 4:64, 5:80, 6:96, 7:112}

sm_deck = marines.shuffle_deck(marines.combat_teams)

GREY = 13
GREEN = 3
RED = 8

# handles all dice rolls and placement
class Dice:
    def __init__(self, dice_default=112):
        self.x = 75
        self.y = 10
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
        pyxel.blt(self.x, self.y, self.img_page, self.u,self.v, self.w, self.h)

##############################
 
# border_x = 96
# border_y = 40
# border_w = 65
# border_h = 33
# portrait_x = 120 # border_x + 24
# portrait_y = 42  # border_y + 2
# name_x = 109  # border_x + 13
# name_y = 60   # border_y + 20


       
class Space_marines:
    def __init__(self):
        self.combat_teams = sm_deck
        self.card_border_x = 96
        self.card_border_y = (40, 76, 112, 148, 184, 220)
        self.card_border_w = 65
        self.card_border_h = 33
        self.name_x = 109
        self.name_y = (60, 96, 132, 168, 204, 240)
        self.portrait_x = 120
        self.portrait_y = (40, 76, 112, 148, 184, 220)
        self.left_arrow_x = 97   # border_x + 1
        self.right_arrow_x = 154 # left_x + 57
        self.arrow_y = (41,77,113,149,185,221)   # border_y + 1 = 41 (41,77,113,149,185,221)
        
    
    def draw(self):
        for marine in self.combat_teams:
            y_val = marine['formation_num']
            col = marine['team_color']
            sm_face = marine['visual']
            sm_name = marine['sm_name'].split(" ")
            single_y = self.arrow_y[y_val-1]
# card border            
            pyxel.rectb(self.card_border_x, 
                        self.card_border_y[y_val-1],              
                        self.card_border_w, 
                        self.card_border_h, 
                        col)
# portrait        
            pyxel.blt(self.portrait_x+1,                             
                      self.portrait_y[y_val-1], 
                      0, 
                      sm_face[0], 
                      sm_face[1], 
                      15, 
                      16)     
# portrait border
            pyxel.rectb(self.portrait_x,                      
                        self.portrait_y[y_val-1], 
                        17, 
                        17, 
                        col)                 
# SM name 1            
            pyxel.text(self.name_x,                                 
                       self.name_y[y_val-1], 
                       f'{sm_name[0]}', 
                       col)                            
# SM name 2            
            pyxel.text(self.name_x-2, 
                       self.name_y[y_val-1]+6, 
                       f'{sm_name[1]}', 
                       col)  
# facing arrows           
            if marine['facing'] == 'LEFT':
                pyxel.blt(self.left_arrow_x, single_y, 0, 0, 32, 6, 6)              # left ARROW 1
                pyxel.blt(self.left_arrow_x, single_y+7, 0, 0, 32, 6, 6)            # 2 
                pyxel.blt(self.left_arrow_x, single_y+14, 0, 0, 32, 6, 6)           # 3
            else:
                pyxel.blt(self.right_arrow_x, single_y, 0, 10, 32, 6, 6)            # right ARROW 1
                pyxel.blt(self.right_arrow_x, single_y+7, 0, 10, 32, 6, 6)          # 2
                pyxel.blt(self.right_arrow_x, single_y+14, 0, 10, 32, 6, 6)         # 3       
                
###############################################################################
class App:
    def __init__(self):
        pyxel.init(screen_x, screen_y, title="SPACE HULK: DEATH ANGEL", fps=30)
        pyxel.load('sh_da.pyxres')
        pyxel.mouse(True)
        self.dice = Dice()
        
        self.space_marines = Space_marines()
        
        
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.dice_value = self.dice.dice_roll()       
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            print("click")


    def draw(self):
        pyxel.cls(0)


## GRID
        for i in range(0,257):
            if i % 4 == 0:
                if i == 128:
                    pyxel.line(i, 0, i, 256, 9)
                    pyxel.line(0, i, 256, i, 9)
                else:
                    pyxel.line(i, 0, i, 256, 2)
                    pyxel.line(0, i, 256, i, 2)
#######                   
        self.dice.draw()
        
        self.space_marines.draw()

#######



####### librarian card test

        # border_x = 96
        # border_y = 40
        # border_w = 65
        # border_h = 33
        # portb_x = border_x + 24
        # portb_y = border_y + 2
        # name_x = border_x + 13
        # name_y = border_y + 20
        
        # left_x = border_x + 1
        # left_y = border_y + 1
        # right_x = left_x + 57
        # right_y = left_y 
        
        
        # #####
        # pyxel.rectb(border_x, border_y, border_w, border_h, 7)     # card border
        # pyxel.blt(portb_x+1, portb_y, 0, 0, 0, 15, 16)               # portrait
        # pyxel.rectb(portb_x, portb_y, 17, 17, GREY)                 # portrait border

        # pyxel.text(name_x, name_y, "LEX", 7)                             # SM name
        # pyxel.text(name_x-2, name_y+6, "CAL", 7)  
            
        
        # pyxel.blt(left_x, left_y, 0, 0, 32, 6, 6)                  # left ARROW
        # pyxel.blt(left_x, left_y+7, 0, 0, 32, 6, 6)                  # left ARROW
        # pyxel.blt(left_x, left_y+14, 0, 0, 32, 6, 6)                  # left ARROW
        
        # pyxel.blt(right_x, right_y, 0, 10, 32, 6, 6)               # right ARROW
        # pyxel.blt(right_x, right_y+7, 0, 10, 32, 6, 6)               # right ARROW
        # pyxel.blt(right_x, right_y+14, 0, 10, 32, 6, 6)               # right ARROW
        
        # #formation 2
        # pyxel.rectb(border_x, 76, border_w, border_h, 9) #border_y+36,
        # #formation 3
        # pyxel.rectb(border_x, 112, border_w, border_h, 10)
        # #formation 4
        # pyxel.rectb(border_x, 148, border_w, border_h, 11)
        # #formation 5
        # pyxel.rectb(border_x, 184, border_w, border_h, 12)
        # #formation 6  
        # pyxel.rectb(border_x, 220, border_w, border_h, 13)

###############################################################################
####### GS Placement visual draft #######

#         gs_img = (0,96,0)
        
#         tails = (0,112,0)
#         skulls = (0,128,0)
#         claws = (0,144,0)
#         stingray = (0,160,0)        


#         spawn_left_x = border_x - 92
#         gs_left_x = spawn_left_x + 48
#         gs_right_x = spawn_left_x + 185
# ##LEFT##        
# #formation 1

#         pyxel.blt(gs_left_x, border_y, 0, 96, 0, 16, 16) # GS spawn L portrait 1
#         pyxel.blt(gs_left_x, border_y+17, 0, 112, 0, 16, 16) # GS spawn team 1
#         pyxel.rectb(spawn_left_x, border_y, border_w, border_h, 7) # GS SPAWN rect    

# #formation 2
#         pyxel.blt(gs_left_x, border_y+36, 0, 96, 0, 16, 16) # GS spawn L portrait
#         pyxel.blt(gs_left_x, border_y+53, 0, 128, 0, 16, 16) # GS spawn team 1
#         pyxel.rectb(spawn_left_x, 76, border_w, border_h, 9) 
    
# #formation 3
#         pyxel.rectb(spawn_left_x, 112, border_w, border_h, 10)
#         #formation 4
#         pyxel.rectb(spawn_left_x, 148, border_w, border_h, 11)
#         #formation 5
#         pyxel.rectb(spawn_left_x, 184, border_w, border_h, 12)
#         #formation 6  
#         pyxel.rectb(spawn_left_x, 220, border_w, border_h, 13)
# ##RIGHT##
#         spawn_right_x = border_x + 92
        
# #formation 1
#         pyxel.blt(gs_right_x, border_y, 0, 96, 0, 16, 16) # GS spawn R portrait
#         pyxel.blt(gs_right_x, border_y+17, 0, 144, 0, 16, 16) # GS spawn team 1       
#         pyxel.rectb(spawn_right_x, border_y, border_w, border_h, 7)
# #formation 2
#         pyxel.blt(gs_right_x, border_y+36, 0, 96, 0, 16, 16) # GS spawn R portrait
#         pyxel.blt(gs_right_x, border_y+53, 0, 160, 0, 16, 16) # GS spawn team 1
#         pyxel.rectb(spawn_right_x, 76, border_w, border_h, 9) 
# #formation 3
#         pyxel.rectb(spawn_right_x, 112, border_w, border_h, 10)
# #formation 4
#         pyxel.rectb(spawn_right_x, 148, border_w, border_h, 11)
# #formation 5
#         pyxel.rectb(spawn_right_x, 184, border_w, border_h, 12)
# #formation 6  
#         pyxel.rectb(spawn_right_x, 220, border_w, border_h, 13)


# rect([[1-x, 2-y]], [[3-w, 4-h]], [[5-col]])
# Draw a rectangle of width w, height h and color col from (x, y).

# rectb(x, y, w, h, col)
# Draw the outline of a rectangle of width w, height h and color col from (x, y).

###############################################################################
####### Blip decks and Location card visual draft ####### 
        # pyxel.rectb(96, 4, 65, 33, 7)     # LOCATION card border
        # pyxel.text(111, 30, "VOID LOCK", 7)
        # # pyxel.rectb(spawn_left_x, 4, 65, 33, 7)     # BLIP LEFT card border
        # pyxel.blt(spawn_left_x+17, 4, 0, 192, 48, 32, 32) # BLIP VISUAL
        # pyxel.text(spawn_left_x+32, 18, "6", 7)
        
        # # pyxel.rectb(spawn_right_x, 4, 65, 33, 7)     # BLIP RIGHT card border
        # pyxel.blt(spawn_left_x+200, 4, 0, 192, 48, 32, 32) # BLIP VISUAL
        # pyxel.text(spawn_left_x+214, 18, "6", 7)
        
###############################################################################
####### Terrain & Danger level placement draft #######
        # (img page, x, y)
              
#         artefact = (1, 96, 0)
#         corridor = (1, 0, 0) 
#         danger_green = (0, 128, 48)
        
#         control_panel = (1, 48, 0)        
#         door = (1, 112, 0)
#         danger_yellow = (0, 144, 48)
        
#         dark_corner = (1, 32, 0)        
#         prom_tank = (1, 64, 0)
#         danger_orange = (0, 160, 48)
        
#         vent_duct = (1,16,0)
#         spore_chim = (1, 80, 0)
#         danger_red = (0, 176, 48)


#         terrain_left_x = spawn_left_x + 71
#         terrain_right_x = spawn_right_x - 22
#         danger_y =  border_y+17

# ##LEFT, 1
#         pyxel.blt(terrain_left_x, border_y, 1, 0, 0, 16, 16) #corridor
#         pyxel.blt(spawn_left_x + 71, danger_y, 0, 128, 48, 16, 16) #corridor danger level = GREEN       
# ##LEFT, 2
#         pyxel.blt(terrain_left_x, border_y+36, 1, 96, 0, 16, 16) #artefact
#         pyxel.blt(spawn_left_x + 71, danger_y+36, 0, 128, 48, 16, 16)       
# ##LEFT, 3
#         pyxel.blt(terrain_left_x, border_y+(36*2), 1, 80, 0, 16, 16) #spore chimney
#         pyxel.blt(spawn_left_x + 71, danger_y+(36*2), 0, 176, 48, 16, 16)
# ##LEFT, 4
#         pyxel.blt(terrain_left_x, border_y+(36*3), 1, 64, 0, 16, 16) #prom tank
#         pyxel.blt(spawn_left_x + 71, danger_y+(36*3), 0, 160, 48, 16, 16)
# ##LEFT, 5
#         pyxel.blt(terrain_left_x, border_y+(36*4), 1, 48, 0, 16, 16) #control panel
#         pyxel.blt(spawn_left_x + 71, danger_y+(36*4), 0, 144, 48, 16, 16)
# ##LEFT, 6
#         pyxel.blt(terrain_left_x, border_y+(36*5), 1, 32, 0, 16, 16) #dark corner
#         pyxel.blt(spawn_left_x + 71, danger_y+(36*5), 0, 160, 48, 16, 16)


# ##RIGHT, 1
#         pyxel.blt(terrain_right_x, border_y, 1, 112, 0, 16, 16) #door
#         pyxel.blt(terrain_right_x, danger_y, 0, 144, 48, 16, 16)                
# ##RIGHT, 2
#         pyxel.blt(terrain_right_x, border_y+36, 1, 16, 0, 16, 16) #vent_duct
#         pyxel.blt(terrain_right_x, danger_y+36, 0, 176, 48, 16, 16)
# ##RIGHT, 3
#         pyxel.blt(terrain_right_x, border_y+(36*2), 1, 80, 0, 16, 16) #spore chimney
#         pyxel.blt(terrain_right_x, danger_y+(36*2), 0, 176, 48, 16, 16)
# ##RIGHT, 4
#         pyxel.blt(terrain_right_x, border_y+(36*3), 1, 96, 0, 16, 16) #artefact
#         pyxel.blt(terrain_right_x, danger_y+(36*3), 0, 128, 48, 16, 16)
# ##RIGHT, 5
#         pyxel.blt(terrain_right_x, border_y+(36*4), 1, 64, 0, 16, 16) #prom tank
#         pyxel.blt(terrain_right_x, danger_y+(36*4), 0, 160, 48, 16, 16)
# ##RIGHT, 6
#         pyxel.blt(terrain_right_x, border_y+(36*5), 1, 48, 0, 16, 16) #control panel
#         pyxel.blt(terrain_right_x, danger_y+(36*5), 0, 144, 48, 16, 16)
        

###############################################################################
  
App()