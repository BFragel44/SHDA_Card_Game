# Sure, here is the code for the remaining steps of the Setup phase:


def setup():
    # Set the 2 Brood Lord cards aside for later use.
    brood_lord_cards = []
    for i in range(2):
        brood_lord_cards.append(BroodLordCard())

    # Shuffle the 36 Genestealer cards and put them face-down at the top of the play area in a reserve pile.
    genestealer_cards = []
    for i in range(36):
        genestealer_cards.append(GenestealerCard())
    random.shuffle(genestealer_cards)
    genestealer_pile = BlipPile(genestealer_cards)

    # Select the appropriate number of Combat Teams per player, and then give each player their corresponding colour-coded Combat Team Token(s), Space Marine cards, and Action cards. Put away the remaining Space Marine and Action cards.
    number_of_players = 1
    combat_teams_per_player = 3
    combat_teams = []
    for i in range(number_of_players):
        combat_teams.append(CombatTeam(combat_teams_per_player))
        combat_teams[i].color = "red"
        for j in range(combat_teams_per_player):
            combat_teams[i].space_marines.append(SpaceMarineCard())
            combat_teams[i].action_cards.append(ActionCard())
    for i in range(len(combat_teams)):
        for j in range(len(combat_teams[i].space_marines)):
            combat_teams[i].space_marines[j].position = i
    for i in range(len(combat_teams)):
        for j in range(len(combat_teams[i].action_cards)):
            combat_teams[i].action_cards[j].position = i

    # Select the Void Lock card for the number of Space Marines and put it in the current Location slot.
    void_lock_cards = []
    for i in range(4):
        void_lock_cards.append(VoidLockCard(i + 6))
    void_lock_card = void_lock_cards[number_of_players - 1]
    current_location = Location(void_lock_card)

    # Separate the other Location cards into piles based on the numbers on their backs.
    location_cards = []
    for i in range(4):
        location_cards.append(Location(i + 2))
    for i in range(4):
        location_cards.append(Location(i + 6))
    for i in range(4):
        location_cards.append(Location(i + 10))
    for i in range(4):
        location_cards.append(Location(i + 14))

    # Shuffle each of those piles.
    for location_pile in location_cards:
        random.shuffle(location_pile)

    # Create an ordered, face down deck from them drawing from each small deck as described on the bottom of the Void Lock card, and then put the remaining Locations away.
    ordered_location_deck = []
    for location_number in void_lock_card.locations:
        for location_pile in location_cards:
            if len(location_pile) > 0:
                ordered_location_deck.append(location_pile.pop())

    # Collect all Space Marine cards that are in the game and shuffle them. Place them in a vertical line down from the Void Lock, creating the Formation (this represents a top view of the marines in a room/corridor). Make the top half of the Formation face left and the bottom half face right.
    space_marines = []
    for i in range(36):
        space_marines.append(SpaceMarineCard())
    random.shuffle(space_marines)
    formation = []
    for i in range(6):
        formation.append(space_marines.pop())
    for i in range(6):
        formation.append(space_marines.pop())
    formation.reverse()
