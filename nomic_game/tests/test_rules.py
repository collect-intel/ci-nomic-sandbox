import unittest
from unittest.mock import patch, mock_open
from rules import GameRules

class TestGameRules(unittest.TestCase):
    def setUp(self):
        # Mock data that mimics the CSV file's content
        self.csv_data = "1. This is the first rule\n2. This is the second rule\n3. This is the third rule"
        # Create a mock open object with csv_data
        m_open = mock_open(read_data=self.csv_data)
        # Start patching 'open'
        self.mock_open = patch('builtins.open', m_open).start()
        # Initialize GameRules with the mocked open function
        self.game_rules = GameRules("test_rules.csv")
        # Ensure that patching is stopped after the test
        self.addCleanup(patch.stopall)

    def test_load_rules_from_csv(self):
        # Reload rules to check if they are loaded correctly
        rules = self.game_rules.load_rules_from_csv("test_rules.csv")
        self.assertEqual(len(rules), 3)
        self.assertEqual(rules[1], "This is the first rule")
        self.assertEqual(rules[2], "This is the second rule")
        self.assertEqual(rules[3], "This is the third rule")

    def test_parse_rule(self):
        rule_number, rule_description = self.game_rules.parse_rule("1. This is a rule")
        self.assertEqual(rule_number, 1)
        self.assertEqual(rule_description, "This is a rule")

    def test_parse_rule_invalid_format(self):
        with self.assertRaises(ValueError):
            self.game_rules.parse_rule("Invalid rule format")

    def test_parse_rule_invalid_number(self):
        with self.assertRaises(ValueError):
            self.game_rules.parse_rule("ABC. Invalid rule number")

    def test_get_rule(self):
        self.game_rules.rules = {1: "Rule 1", 2: "Rule 2"}
        self.assertEqual(self.game_rules.get_rule(1), "Rule 1")
        self.assertEqual(self.game_rules.get_rule(3), "Rule not found")

    def test_add_rule(self):
        self.game_rules.add_rule(4, "New rule")
        self.assertEqual(self.game_rules.get_rule(4), "New rule")

    def test_delete_rule(self):
        self.game_rules.rules = {1: "Rule 1", 2: "Rule 2"}
        self.game_rules.delete_rule(1)
        self.assertEqual(self.game_rules.get_rule(1), "Rule not found")
        self.assertEqual(self.game_rules.get_rule(2), "Rule 2")

if __name__ == "__main__":
    unittest.main()
