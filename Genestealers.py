import random

def gs_deck_create():
    """
    ----------
    Parameters:
    None
    ----------
    Purpose:
    creates the Genestealer deck for the start of play.
    ----------
    Returns:
    gs_raw_deck
    """
    gs_icons = ["tails", "skulls", "stingray", "claws"]
    gs_raw_deck = []
    for g in gs_icons:
        for i in range(11):
            gs_raw_deck.append(g)
    random.shuffle(gs_raw_deck)
    return gs_raw_deck

###########################################################
class Gene_deck:
    def __init__(self, gs_deck, loc_num_left=6, loc_num_right=6):
        self.deck = gs_deck
        self.loc_left = loc_num_left
        self.loc_right = loc_num_right
        self.left_num = 0
        self.right_num = 0
        self.left_cards = []
        self.right_cards = []

    def populate_blips(self):
        self.left_cards = [self.deck.pop(i) for i in range(self.loc_left)]
        self.left_num = len(self.left_cards)
        self.right_cards = [self.deck.pop(i) for i in range(self.loc_right)]
        self.right_num = len(self.right_cards)

    def draw(self):
        pyxel.text(36, 18, f"{self.left_num}", 7)
        pyxel.text(218, 18, f"{self.right_num}", 7)