import itertools
import random
import pyxel

## GENERAL SCREEN SETUP
screen_x = 256 #16 16-pixel chunks wide
screen_y = 256 #16 16-pixel chunks wide


## INITIAL GS MAIN DECK CREATION
def gs_deck_create():
    initial_deck = list(itertools.product(range(1,10),['Tail','Skull','Stingray','Claw']))
    random.shuffle(initial_deck)
    return initial_deck

gs_deck = gs_deck_create()    
# [(7, 'Tail'), (6, 'Stingray'), (5, 'Skull'),...


class Gene_deck:
#TODO ROOM NAME NEEDS TO BE ADDED IN BY WHICH CURRENT ROOM IT IS    
    def __init__(self, gs_deck, loc_num_left=6, loc_num_right=6, current_room ="VOID LOCK"): 
        self.deck = gs_deck
        self.loc_left = loc_num_left
        self.loc_right = loc_num_right
        self.left_num = 0
        self.right_num = 0
        self.left_cards = []
        self.right_cards = []
        self.current_room = current_room

## 1. Populate the blip decks and show number in each sensor img
    def populate_blips(self):
        self.left_cards = [self.deck.pop(i) for i in range(self.loc_left)]
        self.left_num = len(self.left_cards)   
        
        self.right_cards = [self.deck.pop(i) for i in range(self.loc_right)]
        self.right_num = len(self.right_cards)
 
 
    def draw(self):
        pyxel.text(36, 18,f"{self.left_num}", 7)
        pyxel.text(218, 18, f"{self.right_num}", 7)


## MAIN GAME LOOP      
class App:
    def __init__(self):
        pyxel.init(screen_x, screen_y)
        pyxel.load('sh_da.pyxres')
        pyxel.mouse(True)
        self.gene_deck = Gene_deck(gs_deck)
        self.gene_deck.populate_blips()  

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        

    def draw(self):
        pyxel.cls(0)



###############################################################################
####### Blip decks and Location card visual draft ####### 
        pyxel.rectb(96, 4, 65, 33, 7)     # LOCATION card border
        pyxel.text(111, 30, self.gene_deck.current_room, 7)
        pyxel.blt(21, 4, 0, 192, 48, 32, 32) # LBLIP VISUAL
        pyxel.blt(204, 4, 0, 192, 48, 32, 32) # RBLIP VISUAL 
        self.gene_deck.draw() 
        
        
###############################################################################
####### GS Placement visual draft #######

        gs_img = (0,96,0)
        tails = (0,112,0)
        skulls = (0,128,0)
        claws = (0,144,0)
        stingray = (0,160,0)        


        spawn_left_x = 4    #border_x - 92
        gs_left_x = (52, 35, 18, 1)     #spawn_left_x + 48
        gs_right_x = (188, 205, 222, 239)
        gs_img_y = (40, 76, 112, 148, 184, 220)
        gs_team_y = (57, 93, 129, 165, 201, 237)

# ##LEFT##        
# #formation 1

        # R to L
        pyxel.blt(gs_left_x[0], gs_img_y[0], 0, 96, 0, 16, 16) # GS spawn L portrait 1
        pyxel.blt(gs_left_x[1], gs_img_y[0], 0, 96, 0, 16, 16) # GS spawn L portrait 2
        pyxel.blt(gs_left_x[2], gs_img_y[0], 0, 96, 0, 16, 16) # GS spawn L portrait 3
        pyxel.blt(gs_left_x[3], gs_img_y[0], 0, 96, 0, 16, 16) # GS spawn L portrait 4
        pyxel.blt(gs_left_x[0], gs_team_y[0], 0, 112, 0, 16, 16)  # GS spawn team 1
        pyxel.blt(gs_left_x[1], gs_team_y[0], 0, 112, 0, 16, 16)  # GS spawn team 1
        pyxel.blt(gs_left_x[2], gs_team_y[0], 0, 112, 0, 16, 16)  # GS spawn team 1
        pyxel.blt(gs_left_x[3], gs_team_y[0], 0, 112, 0, 16, 16)  # GS spawn team 1
        
        for b in gs_img_y:
            pyxel.rectb(spawn_left_x, b, 64, 33, 7)      # GS SPAWN rect 


# ##RIGHT##       
# #formation 1

        # L to R
        pyxel.blt(gs_right_x[0], gs_img_y[0], 0, 96, 0, 16, 16)    # GS spawn R portrait 1
        pyxel.blt(gs_right_x[1], gs_img_y[0], 0, 96, 0, 16, 16)    # GS spawn R portrait 2
        pyxel.blt(gs_right_x[2], gs_img_y[0], 0, 96, 0, 16, 16)    # GS spawn R portrait 3
        pyxel.blt(gs_right_x[3], gs_img_y[0], 0, 96, 0, 16, 16)    # GS spawn R portrait 4
        pyxel.blt(gs_right_x[0], gs_team_y[0], 0, 144, 0, 16, 16)     # GS spawn team 1
        pyxel.blt(gs_right_x[1], gs_team_y[0], 0, 144, 0, 16, 16)     # GS spawn team 2
        pyxel.blt(gs_right_x[2], gs_team_y[0], 0, 144, 0, 16, 16)     # GS spawn team 3
        pyxel.blt(gs_right_x[3], gs_team_y[0], 0, 144, 0, 16, 16)     # GS spawn team 4
        
        for x in gs_img_y:
            pyxel.rectb(gs_right_x[0], x, 64, 33, 7)         # GS SPAWN rect   

# WHAT DO I NEED TO SPAWN GENESTEALERS?
# 1. MATCH TERRAIN DANGER COLOR TO EVENT CARD
# 2. GET GS CARDS FROM L AND R BLIP PILES AND POPULATE ACCORDING TO THE EVENT CARD



####        
App()        
####
       