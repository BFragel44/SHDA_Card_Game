# Sure, here is an efficient data structure for the game's Space Marine cards:

class SpaceMarineCard:

    def __init__(self, color, attack_range, facing_direction):
        self.color = color
        self.attack_range = attack_range
        self.facing_direction = facing_direction

    def __repr__(self):
        return f"SpaceMarineCard({self.color}, {self.attack_range}, {self.facing_direction})"


class CombatTeam:

    def __init__(self, color, space_marine_cards):
        self.color = color
        self.space_marine_cards = space_marine_cards

    def __repr__(self):
        return f"CombatTeam({self.color}, {self.space_marine_cards})"


class Formation:

    def __init__(self, combat_teams):
        self.combat_teams = combat_teams

    def __repr__(self):
        return f"Formation({self.combat_teams})"

# This data structure is efficient because it uses a single class for each type of object in the game. 
# This makes it easy to access and manipulate the objects, and it also makes the code more readable and maintainable.

# The SpaceMarineCard class stores the color, attack range, and facing direction of a Space Marine card. 
# The CombatTeam class stores the color and space marine cards of a Combat Team. 
# The Formation class stores the combat teams of a Formation.
