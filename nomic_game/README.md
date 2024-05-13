# Nomic Game Engine

## Overview
This Nomic Game Engine simulates a game of Nomic with LLM agents, where the primary activity involves changing the rules as the game progresses. This engine specifically supports game sessions with LLMs both as players and as the Game Manager.

## Key Features
- **Dynamic Rule Change**: Allows players to propose and vote on changes to mutable rules or to introduce new rules.
- **Automated Game Manager**: Manages rule proposals, voting outcomes, and enforces game rules and state changes.
- **Game State Management**: Maintains and updates the game state, including tracking player scores and rule changes.
- **Transcript Management**: Logs all game actions and communications for review and replay.
- **LLM Integration**: Designed to work with LLMs, facilitating AI-driven player and game manager interactions.

## Directory Structure
```
nomic_game/
│
├── client_session/ # Manages sessions for players and the Game Manager.
│ ├── client_session.py # Abstract base class for sessions.
│ └── openai_session.py # Implements session handling for interaction with OpenAI.
│
├── config/ # Configuration files for setting up the game rules and player details.
│ └── game_config.json
│
├── data/ # Data files that provide contexts and immutable/mutable rules for the game.
│ ├── context/
│ │ ├── gm_objective.txt
│ │ ├── nomic_game_context.txt
│ │ └── player_objective.txt
│ ├── constitutions/
│ │ ├── gm/
│ │ └── player/
│ └── rules/
│ ├── game_rules.csv
│ └── locked_rules.txt
│
├── tests/ # Contains unit tests for the various components of the game.
│ ├── test_game_manager.py
│ ├── test_player.py
│ ├── test_rules.py
│ ├── test_state.py
│ └── test_transcript.py
│
├── utils/ # Utilities for setting up the game environment and managing outputs.
│ ├── context_maker.py
│ ├── output_utils.py
│ └── prompt_sender.py
│
├── game.py # Central game logic.
├── game_engine.py # Coordinates game initialization and cycles.
├── game_manager.py # Processes and applies game rules.
├── output_manager.py # Handles all file outputs related to game data.
├── player.py # Defines player behavior and interactions.
├── rules.py # Manages game rules.
├── state.py # Maintains current game state.
└── transcript.py # Manages recording of game actions and dialogue.
```

## Setup and Running
1. **Clone the Repository**: Clone this repository to your machine or development environment.
2. **Configure the Game**:
   - Modify `config/game_config.json` to adjust player settings, game rules, and other parameters.
   - Edit `.txt` and `.csv` files within the `data/` directory to customize game rules and contexts.
3. **Set Up Environment**:
   - Ensure all Python dependencies are installed: `pip install -r requirements.txt`
   - Set your OpenAI API key in a `.env` file: `OPENAI_API_KEY='your-api-key-here'`
4. **Run Tests**: Validate the setup by executing: `python -m unittest discover -s tests`
5. **Start the Game**: Launch the game engine with: `python main.py`

## Modifying Game Configuration
To alter the game's behavior or rule set, modify the `game_config.json` and associated `.txt` and `.csv` files:
- **JSON Configuration**: Change player settings, game flow controls, and linked data files.
- **Rule Files**: Update `game_rules.csv` to adjust or add new mutable and immutable rules.
- **Context Files**: Edit text files like `gm_objective.txt` to change the narrative or instructions provided to the LLMs.

