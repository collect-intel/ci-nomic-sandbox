class GameState:
    def __init__(self, initial_state=""):
        """Initialize the game state with an initial value.

        Args:
            initial_state (str): The initial state of the game.
        """
        self.state = initial_state

    def get_state(self):
        """Retrieve the current state of the game.

        Returns:
            str: The current game state.
        """
        return self.state

    def update_state(self, new_state):
        """Update the game state with a new value.

        Args:
            new_state (str): The new state of the game to be set.
        """
        self.state = new_state
