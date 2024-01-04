import random

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
                 'support_token': 0,
                 'team_id': 1,
                 },
            
                {'sm_name':'Brother Scipio',
                 'team_color': 13,
                 'visual': (0, 16), 
                 'attk_range': 2, 
                 'facing': 'setup',
                 'formation_num': 0,
                 'status': 'alive',
                 'support_token': 0,
                 'team_id': 2,
                 },

                {'sm_name':'Sargeant Gideon',
                'team_color': 3,
                'visual': (16, 0),  
                'attk_range': 0, 
                'facing': 'setup',
                'formation_num': 0,
                'status': 'alive',
                'support_token': 0,
                'team_id': 1,
                },

                {'sm_name':'Brother Noctis',
                'team_color': 3,
                'visual': (16, 16),              
                'attk_range': 2, 
                'facing': 'setup',
                'formation_num': 0,
                'status': 'alive',
                'support_token': 0,
                'team_id': 2,
                },

                {'sm_name':'Brother Leon',
                'team_color': 8,
                'visual': (32, 0),    
                'attk_range': 3, 
                'facing': 'setup',
                'formation_num': 0,
                'status': 'alive',
                'support_token': 0,
                'team_id': 1,
                },

                {'sm_name':'Brother Valencio',
                'team_color': 8,
                'visual': (32, 16),             
                'attk_range': 2, 
                'facing': 'setup',
                'formation_num': 0,
                'status': 'alive',
                'support_token': 0,
                'team_id': 2,
                }]


# shuffle the cards
def shuffle_deck(combat_teams):
    formation_numbers = [1,2,3,4,5,6]
    random.shuffle(formation_numbers)
    
    for marine in combat_teams:   
        num = formation_numbers.pop(0)
        set_formation = {'formation_num': num}
        marine.update(set_formation)
        if num <= 3:
            set_facing = {'facing': 'LEFT'}
            marine.update(set_facing)
        else:
            set_facing = {'facing': 'RIGHT'}
            marine.update(set_facing)
    return(combat_teams)
    
            
# print(shuffle_deck(combat_teams))
    





