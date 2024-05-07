import re
from utils.api_handler import OpenAISession


class GMActions:
    """Defines and interprets valid game manager actions."""

    ACTION_PATTERNS = {
        "prompt_player": re.compile(r"Prompt player (\d+): (.+)"),
        "add_rule": re.compile(r"Add Rule (\d+): (.+)"),
        "delete_rule": re.compile(r"Delete Rule (\d+)"),
        "update_rule": re.compile(r"Update Rule (\d+): (.+)"),
        "win_player": re.compile(r"Win Player (\d+): (.+)"),
        "lose_player": re.compile(r"Lose Player (\d+): (.+)"),
        "terminate_game": re.compile(r"Terminate Game: (.+)"),
        "update_state": re.compile(r"Update State: (.+)"),
    }

    @classmethod
    def interpret(cls, text):
        """Interpret the text to find all matching actions and parameters."""
        actions = []
        for line in text.split("\n"):
            for action, pattern in cls.ACTION_PATTERNS.items():
                match = pattern.match(line.strip())
                if match:
                    actions.append((action, match.groups()))
        return actions


class GMInterpreter:
    """Parses and executes actions from the game manager's replies."""

    def __init__(self, game_rules, game_state):
        self.game_rules = game_rules
        self.game_state = game_state

    def execute_actions(self, actions):
        """Execute a list of actions on the game state or rules."""
        results = []
        prompt_player_count = 0
        state_updated = False
        terminate_game = None

        for action, params in actions:
            if action == "prompt_player":
                if prompt_player_count == 0:
                    player_id, prompt = params
                    results.append(f"Send prompt to player {player_id}: {prompt}")
                    prompt_player_count += 1
            elif action == "add_rule":
                rule_number, rule_text = params
                self.game_rules.add_rule(int(rule_number), rule_text)
                results.append(f"Rule {rule_number} added.")
            elif action == "delete_rule":
                rule_number = int(params[0])
                self.game_rules.delete_rule(rule_number)
                results.append(f"Rule {rule_number} deleted.")
            elif action == "update_rule":
                rule_number, rule_text = params
                self.game_rules.update_rule(int(rule_number), rule_text)
                results.append(f"Rule {rule_number} updated.")
            elif action == "win_player":
                player_id, win_text = params
                results.append(f"Player {player_id} wins: {win_text}")
            elif action == "lose_player":
                player_id, lose_text = params
                results.append(f"Player {player_id} loses: {lose_text}")
            elif action == "terminate_game":
                terminate_game = f"Game terminated: {params[0]}"
            elif action == "update_state" and not state_updated:
                self.game_state.update(params[0])
                results.append(f"Game state updated.")
                state_updated = True

        if terminate_game:
            results.append(terminate_game)

        return results


class GameManager:
    def __init__(self, constitution, client_session=OpenAISession()):
        """Initialize the Game Manager with a constitution and an OpenAISession."""
        self.constitution = constitution
        self.client_session = client_session
        self.interpreter = GMInterpreter(GameRules(), GameState(""))

    def receive_gm_prompt(self, prompt):
        """Process response from the game manager LLM."""
        actions = GMActions.interpret(response)
        if actions:
            results = self.interpreter.execute_actions(actions)
            return "\n".join(results)
        return "No valid action found."
