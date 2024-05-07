import unittest
from state import GameState

class TestGameState(unittest.TestCase):
    def setUp(self):
        # Initialize with a default state
        self.game_state = GameState("Game has started. Waiting for players.")

    def test_initial_state(self):
        # Test the initial state of the game
        self.assertEqual(self.game_state.get_state(), "Game has started. Waiting for players.")

    def test_get_state(self):
        # Test getting the current state
        self.assertEqual(self.game_state.get_state(), "Game has started. Waiting for players.")

    def test_update_state(self):
        # Test updating the state
        self.game_state.update_state("First round complete. Updating scores.")
        self.assertEqual(self.game_state.get_state(), "First round complete. Updating scores.")

    def test_update_state_with_empty_string(self):
        # Test updating the state with an empty string
        self.game_state.update_state("")
        self.assertEqual(self.game_state.get_state(), "")

    def test_update_state_with_null(self):
        # Test updating the state with None
        self.game_state.update_state(None)
        self.assertEqual(self.game_state.get_state(), None)

if __name__ == "__main__":
    unittest.main()
