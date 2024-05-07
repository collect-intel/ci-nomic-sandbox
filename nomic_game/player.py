from utils.api_handler import OpenAISession


class Player:
    def __init__(self, constitution, client_session=OpenAISession()):
        """Initialize the Player with a constitution and an OpenAISession."""
        self.constitution = constitution
        self.client_session = client_session
        self.active = True
