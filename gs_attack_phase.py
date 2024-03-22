import pyxel
import ui
import shda_marines as sm

#### GENESTEALER ATTACK PHASE ####
# SUMMARY: Each SWARM attacks the marine it is ENGAGED with.  
# - - SWARM = All face-up GS on same side & position 
# - - ENGAGED = Same position (directly left or right of Marine) 

## 1. Each swarm attacks, starting with swarm closest to Formation top.
# - - START AT TOP LEFT, left side always attacks first 

## 2. roll dice:
# - - Result >= number of GS in swarm = MISS
# - - Result < number of GS in swarm = SLAIN 
# - - - SM is removed from Formation and Formation immediately SHIFTS. 


class ResolveGSAttackUI:
    def __init__(self, space_marines, location_and_spawns):
        self.phase_resolved = False
        self.space_marines = space_marines
        self.location_and_spawns = location_and_spawns
        self.click_phase = 0
        self.attack_queue = None
        self.gs_attack_roll = None

    def battle_rows_update(self):
        if self.attack_queue is None:
            self.attack_queue = []
        for marine in self.space_marines.combat_teams:
            left_swarm = self.location_and_spawns.spawned_left_swarms.get(marine['formation_num'], {}).get('g_stealers', [])
            right_swarm = self.location_and_spawns.spawned_right_swarms.get(marine['formation_num'], {}).get('g_stealers', [])
            if len(left_swarm) > 0:
                swarm_dir = 'LEFT'
                attack = {
                    'swarm': swarm_dir,
                    'swarm_size': len(left_swarm),
                    'facing': marine['facing'],
                    'formation_num': marine['formation_num'],
                    'back_attack': marine['facing'] != swarm_dir,
                    'sm': marine['sm_name']}
                self.attack_queue.append(attack)
            if len(right_swarm) > 0:
                swarm_dir = 'RIGHT'
                attack = {
                    'swarm': swarm_dir,
                    'swarm_size': len(right_swarm),
                    'facing': marine['facing'],
                    'formation_num': marine['formation_num'],
                    'back_attack': marine['facing'] != swarm_dir,
                    'sm': marine['sm_name']}

                self.attack_queue.append(attack)
        self.click_phase = 2
    
    ## Main UPDATE method
    def update(self):
        if self.click_phase == 1:
            self.battle_rows_update()
        # if self.click_phase == 2:
        #     pass
        if self.click_phase == 3:
            self.gs_attack_roll.update()
  
    def battle_rows_draw(self):
        gs_left_x = 52
        gs_right_x = 188
        gs_img_y = (40, 76, 112, 148, 184, 220)
        # draw rectangles around each gs and marine pairing in self.all_attacks
        for attack in self.attack_queue:
            print(attack)
            if attack['swarm'] == 'LEFT':
                # make separate box if left_GS > 0
                box_x = gs_left_x
                
            if attack['swarm'] == 'RIGHT':
                # make separate box if right_GS > 0
                box_x = gs_right_x

            pyxel.rectb(
                box_x-2,
                gs_img_y[attack['formation_num']]-2,
                19, 34, 9)
            # SM outline box
            pyxel.rectb(
                sm.sm_visual_dimms["card_border_x"]-2,
                sm.sm_visual_dimms["card_border_y"][attack['formation_num']]-2,
                sm.sm_visual_dimms["card_border_w"]+4,
                sm.sm_visual_dimms["card_border_h"]+4,
                9)
            if ui.phase_box_click():
                self.click_phase = 3
                if self.attack_queue:
                    current_attack = self.attack_queue.pop(0)
                    self.gs_attack_roll = ui.GsAttackRoll(current_attack)


    ## Main DRAW method
    def overlay_draw(self):
        if self.click_phase == 0:
            if ui.phase_box_click():
                self.click_phase = 1
        if self.click_phase == 2:
            if self.attack_queue:
                self.battle_rows_draw()
        if self.click_phase == 3:
            if self.gs_attack_roll:
                self.gs_attack_roll.draw()
