# context_maker utility for creating Player and GM context for their LLM
from typing import Literal
import os


CONSTITUTION_DESCRIPTIONS = {
    "player": "This is a code of conduct you are expected to follow while playing the game",
    "gm": "This is a code of conduct you are expected to follow as the Game Manager for this game",
}


def add_starting_context(config, client_session, role: Literal["player", "gm"]):
    """Add starting context to the client session from configuration.

    Args:
        config (dict): Configuration dictionary containing context settings.
        client_session (OpenAISession): The session object for the player or GM.
        role (str): The role ('player' or 'gm') to fetch context for.

    Raises:
        FileNotFoundError: If the context file does not exist.
        ValueError: If the context file is empty.
        IOError: If there's an issue reading the file.
    """
    for role in ["all", role]:
        for context in config["starting_context"][role]:
            path = context["path"]
            # Check if the file exists
            if not os.path.exists(path):
                raise FileNotFoundError(f"No such file: {path}")

            with open(path, "r") as file:
                context_text = (
                    file.read().strip()
                )  # Use strip to remove leading/trailing whitespace

                # Ensure the file is not empty
                if not context_text:
                    raise ValueError(f"Context file is empty: {path}")

                client_session.add_context(context_text, context["description"])


def add_constitution_context(
    constitution, client_session, role: Literal["player", "gm"]
):
    """Add constitution context to the client session.

    Args:
            constitution (str): The constitution text to add as context.
            client_session (OpenAISession): The session object for the player or GM.
    """
    client_session.add_context(constitution, CONSTITUTION_DESCRIPTIONS[role])
