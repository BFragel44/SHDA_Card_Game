import random
import pandas as pd

######################################################### EVENT DECK CREATION
def create_event_deck():
    """
    ----------
    Parameters:
    None
    ----------
    Purpose:
    creates the EVENT deck for the start of play.
    ----------
    Returns:
    event_deck
    """
    data = "event_cards.csv"
    df = pd.read_csv(data)
    df["card_num"] = df.reset_index().index
    df.to_dict("dict")
    event_deck = df.to_dict("records")
    random.shuffle(event_deck)
    return event_deck


# #this is the initial, shuffled, Event deck
event_deck = create_event_deck()

###########################################################
class Event_cards:
    def __init__(self, initial_deck):
        self.deck = initial_deck
        self.cards_drawn = 0
        self.current_card = []
        self.discard = []

    def draw_card(self):
        # initial event card only spawns genestealers
        if self.cards_drawn < 1:
            self.current_card.append(self.deck.pop(0))
            self.cards_drawn += 1
        else:
            prev_card = self.current_card.pop(0)
            self.discard.append(prev_card)
            self.current_card.append(self.deck.pop(0))
            self.cards_drawn += 1
        return self.current_card
        # RESOLVE EVENT ON CARD AFTER INITIAL TURN

    def draw(self):
        pass
        # TODO Will need another screen to show card and description