import json
from state import GameState as State
from rules import GameRules as Rules
from game_manager import GameManager
from player import Player
from utils.api_handler import OpenAISession
from utils import context_maker


class Game:
    DEFAULT_TICK_MAX = 100
    GM_TRY_MAX = 3
    DEFAULT_PLAYER_CONSTITUTION_PATH = (
        "data/constitutions/player/default_constitution.txt"
    )
    DEFAULT_CONFIG_PATH = "config/game_config.json"

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.load_config(config_path)
        self.state = State("")
        self.rules = Rules(self.config["rules_filepath"])
        self.gm = None
        self.players = {}
        self.winners = {}
        self.losers = {}
        self.active = False

    def load_config(self, config_path):
        """Load game configuration from a JSON file and handle defaults."""
        with open(config_path, "r") as file:
            config = json.load(file)

        # Set defaults if not specified in the config file
        config["default_max_ticks"] = config.get(
            "default_max_ticks", Game.DEFAULT_TICK_MAX
        )
        config["gm_try_max"] = config.get("gm_try_max", Game.GM_TRY_MAX)

        self.config = config

    def initialize_players(self):
        """Initialize players based on the game configuration."""
        for player_config in self.config["players"]:
            player_number = player_config["number"]
            constitution_path = player_config.get(
                "constitution", Game.DEFAULT_PLAYER_CONSTITUTION_PATH
            )
            player_constitution = self.load_constitution(constitution_path)
            player = Player(
                constitution=player_constitution, client_session=OpenAISession()
            )
            context_maker.add_starting_context(
                self.config, player.client_session, "player"
            )
            context_maker.add_constitution_context(
                player_constitution, player.client_session, "player"
            )
            self.players[player_number] = player

    def initialize_gm(self):
        """Initialize the game manager."""
        constitution_path = self.config["game_manager"]
        gm_constitution = self.load_constitution(constitution_path)
        gm = GameManager(constitution=gm_constitution, client_session=OpenAISession())
        context_maker.add_starting_context(self.config, gm.client_session, "gm")
        context_maker.add_constitution_context(gm_constitution, gm.client_session, "gm")
        self.gm = gm

    def load_constitution(self, constitution_path):
        """Load a constitution text file."""
        with open(constitution_path, "r") as file:
            return file.read()

    # for each gm prompt, share: prompt: active players list, valid gm actions, next action prompt
    # when rules change, share: context: New Rules: {rules} (to everyone)
    # when state changes, share: context: New State: {state} (to everyone)
    # possibly, when transcript changes, share: Transcript Updated: {transcript} (to everyone)

    def list_active_players(self):
        # Sort the dictionary by player number and generate the list of active players
        active_players = sorted(
            player_num for player_num, player in players_dict.items() if player.active
        )
        # Format the list into the desired string output if there are active players
        if active_players:
            player_list = "\n".join(
                f"Player {player_num}" for player_num in active_players
            )
            return f"Currently Active Players:\n{player_list}"
        else:
            return "Currently Active Players:\nNone"

    def get_begin_game_prompt(self):
        return self.start_gm_prompt

    def send_gm_prompt(self, prompt):
        # bundle prompt with game state, rules, and player information
        return self.gm.receive_gm_response(prompt)

    def resend_gm_prompt(self, prompt):
        # send prompt again, but with clarification text added
        pass

    def is_valid_gm_response(self, response):
        pass

    def interpret_gm(self, response):
        # GM will only give PLAYER_TRY_MAX tries, but will log this inside GM, not the Game's responsibility
        pass

    def is_terminated(self):
        return not self.active

    def send_player_prompt(self, prompt):
        pass

    def interpret_player(self, response):
        pass


class GameEngine:
    def __init__(self, game=Game()):
        self.game = game
        self.transcript = Transcript()

        self.transcript.append(0, "Game Engine initialized")

    def run(max_num_ticks=Game.DEFAULT_TICK_MAX):
        game = self.game
        game.initialize_gm()
        game.initialize_players()
        # TODO: figure out begin game prompt
        next_gm_prompt = game.get_begin_game_prompt()
        self.transcript.append(0, f"Game to GM: {next_gm_prompt}")

        # TODO: fill in the remaining game functions
        for tick in range(max_num_ticks):

            gm_response = game.send_gm_prompt(next_gm_prompt)

            for i in range(GM_TRY_MAX):
                if game.is_valid_gm_response(gm_response):
                    next_player_prompt = game.interpret_gm(gm_response)
                    break
                else:
                    gm_response = game.resend_gm_prompt(next_gm_prompt)

            if game.is_terminated():
                self.transcript.append(tick, f"GM to Game: {gm_response}")
                break

            player = next_player_prompt.player
            player_prompt = next_player_prompt.prompt
            self.transcript.append(tick, f"GM to {player}: {player_prompt}")
            player_response = game.send_player_prompt(player, player_prompt)
            next_gm_prompt = game.interpret_player(player, player_response)

        if not game.is_terminated() and tick == max_num_ticks - 1:
            self.transcript.append(tick, "Game terminated due to max tick limit")
