# utils/api_handler.py
import os
from openai import OpenAI
import uuid
from dotenv import load_dotenv
from enum import Enum, auto


class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class OpenAIClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = OpenAI()
        return cls._instance


class OpenAISession:
    """Class to manage an individual OpenAI API session using a shared client."""

    def __init__(self):
        load_dotenv()
        self.client = OpenAIClient.get_instance()
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.messages = []

    def add_context(self, context, description=None):
        """Add context to the session."""
        context = description + ":\n" + context if description else context
        self.messages.append({"role": Role.SYSTEM.value, "content": context})

    def send_prompt(self, prompt, role=Role.USER):
        """Send a prompt to this session and return the response."""
        if not isinstance(role, Role):
            raise ValueError("Invalid role type. Must be a 'Role' enum.")

        # Send the prompt to the OpenAI API
        self.messages.append({"role": role.value, "content": prompt})
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages
        )
        response_content = response.choices[0].message.content

        # Append the response from the assistant to the messages
        self.messages.append(
            {"role": Role.ASSISTANT.value, "content": response_content}
        )

        return response_content
