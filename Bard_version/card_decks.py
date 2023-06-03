# here is an efficient data structure for the action cards described below:
class ActionCard:
    def __init__(self, color, role, special_ability):
        self.color = color
        self.role = role
        self.special_ability = special_ability

    def __repr__(self):
        return f"ActionCard({self.color}, {self.role}, {self.special_ability})"

# This data structure is efficient because it uses a single class for each type of action card. 
# This makes it easy to access and manipulate the action cards, and it also makes the code more readable and maintainable.

# The ActionCard class stores the color, role, and special ability of an action card. 
# The color is used to identify the combat team that the action card belongs to. 
# The role is the type of action that the action card can be used to perform. 
# The special ability is a unique ability that can only be used by this action card.

# here is an efficient data structure for the Genestealer cards described below:

class GenestealerCard:
    def __init__(self, class_, icon):
        self.class_ = class_
        self.icon = icon

    def __repr__(self):
        return f"GenestealerCard({self.class_}, {self.icon})"


class BroodLordCard:
    def __init__(self):
        pass

    def __repr__(self):
        return "BroodLordCard()"


class GenestealerDeck:
    def __init__(self):
        self.genestealer_cards = []
        self.brood_lord_cards = []

        for i in range(36):
            self.genestealer_cards.append(GenestealerCard(i % 3, i // 3))
        self.brood_lord_cards.append(BroodLordCard())

    def __repr__(self):
        return f"GenestealerDeck({self.genestealer_cards}, {self.brood_lord_cards})"
    

class BlipPile:
    def __init__(self, genestealer_deck):
        self.genestealer_cards = []
        self.genestealer_deck = genestealer_deck

    def __repr__(self):
        return f"BlipPile({self.genestealer_cards})"

    def spawn(self):
        if len(self.genestealer_cards) > 0:
            genestealer_card = self.genestealer_cards.pop()
            return genestealer_card
        else:
            return None


class Location:
    def __init__(self, blip_piles):
        self.blip_piles = blip_piles

    def __repr__(self):
        return f"Location({self.blip_piles})"

    def spawn_genestealers(self, number):
        genestealers = []
        for i in range(number):
            genestealer = self.blip_piles[i % 2].spawn()
            if genestealer is not None:
                genestealers.append(genestealer)
        return genestealers

# This data structure is efficient because it uses a single class for each type of genestealer card. 
# This makes it easy to access and manipulate the genestealer cards, and it also makes the code more readable and maintainable.

# The GenestealerCard class stores the class and icon of a genestealer card. 
# The BroodLordCard class is a special type of genestealer card that can only be used by special event cards. 
# The GenestealerDeck class stores the genestealer cards in the game. The BlipPile class stores the genestealer cards in a blip pile. 
# The Location class stores the blip piles on either side of the location.


# here is an efficient data structure for the Location cards described below:
class LocationCard:
    def __init__(self, terrain_icons, blip_pile_sizes, exception_text):
        self.terrain_icons = terrain_icons
        self.blip_pile_sizes = blip_pile_sizes
        self.exception_text = exception_text

    def __repr__(self):
        return f"LocationCard({self.terrain_icons}, {self.blip_pile_sizes}, {self.exception_text})"


class LocationDeck:
    def __init__(self, location_cards):
        self.location_cards = location_cards

    def __repr__(self):
        return f"LocationDeck({self.location_cards})"

    def draw(self):
        if len(self.location_cards) > 0:
            location_card = self.location_cards.pop()
            return location_card
        else:
            return None


class VoidLockCard:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players

    def __repr__(self):
        return f"VoidLockCard({self.number_of_players})"


class LocationManager:
    def __init__(self, location_decks):
        self.location_decks = location_decks

    def __repr__(self):
        return f"LocationManager({self.location_decks})"

    def get_next_location(self):
        for location_deck in self.location_decks:
            location_card = location_deck.draw()
            if location_card is not None:
                return location_card
        return None

# This data structure is efficient because it uses a single class for each type of location card. 
# This makes it easy to access and manipulate the location cards, and it also makes the code more readable and maintainable.

# The LocationCard class stores the terrain icons, blip pile sizes, and exception text of a location card. 
# The LocationDeck class stores the location cards in a deck. 
# The VoidLockCard class is a special type of location card that is always the first location in the game. 
# The LocationManager class manages the location decks and provides a method to get the next location.


# here is an efficient data structure for the Terrain cards described below:
class TerrainCard:
    def __init__(self, icon, spawn_rate, special_action):
        self.icon = icon
        self.spawn_rate = spawn_rate
        self.special_action = special_action

    def __repr__(self):
        return f"TerrainCard({self.icon}, {self.spawn_rate}, {self.special_action})"


class TerrainDeck:
    def __init__(self, terrain_cards):
        self.terrain_cards = terrain_cards

    def __repr__(self):
        return f"TerrainDeck({self.terrain_cards})"

    def draw(self):
        if len(self.terrain_cards) > 0:
            terrain_card = self.terrain_cards.pop()
            return terrain_card
        else:
            return None


class TerrainManager:
    def __init__(self, terrain_decks):
        self.terrain_decks = terrain_decks

    def __repr__(self):
        return f"TerrainManager({self.terrain_decks})"

    def get_next_terrain(self):
        for terrain_deck in self.terrain_decks:
            terrain_card = terrain_deck.draw()
            if terrain_card is not None:
                return terrain_card
        return None

# This data structure is efficient because it uses a single class for each type of terrain card. 
# This makes it easy to access and manipulate the terrain cards, and it also makes the code more readable and maintainable.

# The TerrainCard class stores the icon, spawn rate, and special action of a terrain card. 
# The TerrainDeck class stores the terrain cards in a deck. 
# The TerrainManager class manages the terrain decks and provides a method to get the next terrain card.


# here is an efficient data structure for the Event cards described below:
class EventCard:
    def __init__(self, exception_text, spawn_icons, movement_icons):
        self.exception_text = exception_text
        self.spawn_icons = spawn_icons
        self.movement_icons = movement_icons

    def __repr__(self):
        return f"EventCard({self.exception_text}, {self.spawn_icons}, {self.movement_icons})"


class EventDeck:
    def __init__(self, event_cards):
        self.event_cards = event_cards

    def __repr__(self):
        return f"EventDeck({self.event_cards})"

    def draw(self):
        if len(self.event_cards) > 0:
            event_card = self.event_cards.pop()
            return event_card
        else:
            return None


class EventManager:
    def __init__(self, event_decks):
        self.event_decks = event_decks

    def __repr__(self):
        return f"EventManager({self.event_decks})"

    def get_next_event(self):
        for event_deck in self.event_decks:
            event_card = event_deck.draw()
            if event_card is not None:
                return event_card
        return None

# This data structure is efficient because it uses a single class for each type of event card. 
# This makes it easy to access and manipulate the event cards, and it also makes the code more readable and maintainable.

# The EventCard class stores the exception text, spawn icons, and movement icons of an event card. 
# The EventDeck class stores the event cards in a deck. The EventManager class manages the event decks and provides a method to get the next event.

