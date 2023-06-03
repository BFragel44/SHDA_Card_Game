import random
# here is an efficient data structure for the Action Dice described below:

class ActionDie:
    def __init__(self):
        self.faces = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "skull",
            "skull",
            "skull",
        ]

    def roll(self):
        return random.choice(self.faces)

    def is_hit(self, space_marine):
        if self.roll() == "💀":
            return True
        else:
            return False

    def is_kill(self, genestealer_swarm, space_marine):
        if int(self.roll()) <= len(genestealer_swarm):
            return True
        else:
            return False


# This data structure is efficient because it uses a single class to represent the action die. 
# This makes it easy to access and manipulate the die, and it also makes the code more readable and maintainable.

# The ActionDie class stores the faces of the die. 
# The roll() method randomly selects a face from the die. 
# The is_hit() method returns True if the roll is a skull, and False otherwise. 
# The is_kill() method returns True if the roll is less than or equal to the number of genestealers in the swarm, and False otherwise.


# here is an efficient data structure for the Support Tokens described below:
class SupportToken:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"SupportToken({self.value})"

    def add_value(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def is_empty(self):
        return self.value == 0


# This data structure is efficient because it uses a single class to represent a support token. 
# This makes it easy to access and manipulate the token, and it also makes the code more readable and maintainable.

# The SupportToken class stores the value of the token. 
# The add_value() method adds a value to the token. 
# The get_value() method returns the value of the token. 
# The is_empty() method returns True if the token is empty, and False otherwise.

