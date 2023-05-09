class GameStateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.__name__] = state

    def set_initial_state(self, state):
        self.add_state(state)
        self.current_state = state

    def change_state(self, state_name):
        if self.current_state.__name__ != state_name:
            self.current_state = self.states[state_name]

    def update(self):
        self.current_state.update(self)

    def draw(self):
        self.current_state.draw(self)