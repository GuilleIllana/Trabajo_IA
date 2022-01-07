class Cell:
    # Attributes
    discovered = False
    state = 9
    heuristic_value = 0
    undiscovered_neighbours = 8

    def __init__(self, discovered=False, state=9, heuristic_value=-1):
        self.discovered = discovered
        self.state = state
        self.heuristic_value = heuristic_value
        return

    def update_state(self, state):
        self.state = state

    def update_nneighbours(self, nneighbours):
        self.undiscovered_neighbours = nneighbours
