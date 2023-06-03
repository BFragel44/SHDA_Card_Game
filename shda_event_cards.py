import pandas as pd
import random
import pyxel

def create_event_deck():
    data = 'event_cards.csv'
    df = pd.read_csv(data)
    df['card_num'] = df.reset_index().index
    df.to_dict('dict')
    event_deck = df.to_dict('records')
    random.shuffle(event_deck)
    return event_deck

# #this is the FINAL, shuffled, location deck
event_deck = create_event_deck()


class Event_cards:
    def __init__(self, initial_deck):
        self.deck = initial_deck
        self.cards_drawn = 0
        self.current_card = []
        
    def draw_card(self):    
        #initial event card only spawns genestealers
        if self.cards_drawn < 1:
            self.current_card.append(self.deck.pop(0))
            self.cards_drawn += 1
        else:
            current_card = self.deck.pop(0)
            self.cards_drawn += 1
            # RESOLVE EVENT ON CARD AFTER INITIAL TURN

            
event_cards = Event_cards(event_deck)
event_cards.draw_card()

print(event_cards.current_card[0]['Card Name'])
print(event_cards.current_card[0]['L Spawn'])
print(event_cards.current_card[0]['R Spawn'])

example = [{'Card Name': 'Psychic Assault', 
            'Card Effect': 'INSTINCT: Choose 1 SM and ROLL a die. If you roll a 0 or 1, the SM is slain.', 
            'L Spawn': 'wt_red', 
            'R Spawn': 'wt_orange', 
            'GS Maneuver ': 'flank_arrow', 
            'GS Emblem': 'stingray', 
            'card_num': 26}]