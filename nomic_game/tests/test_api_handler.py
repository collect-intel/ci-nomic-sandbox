import unittest
from unittest.mock import patch, MagicMock
from utils.api_handler import OpenAISession, Role


class TestOpenAISession(unittest.TestCase):
    def setUp(self):
        """Set up test case dependencies and mocks."""
        self.mock_openai_client = MagicMock()
        self.mock_openai_chat_completions = MagicMock()
        self.mock_openai_client.chat.completions.create = (
            self.mock_openai_chat_completions
        )

        # Set up to return a structured mock response that supports attribute access
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Mocked API Response"))
        ]
        self.mock_openai_chat_completions.return_value = mock_response

        patcher = patch(
            "utils.api_handler.OpenAIClient.get_instance",
            return_value=self.mock_openai_client,
        )
        self.addCleanup(patcher.stop)
        patcher.start()

        self.session = OpenAISession()

    def test_add_context(self):
        """Test adding context."""
        context = "Context message."

        # Act
        self.session.add_context(context)

        # Assert
        self.assertIn({"role": "system", "content": context}, self.session.messages)

    def test_send_prompt(self):
        """Test sending a prompt."""
        prompt = "What is your next action?"
        role = Role.USER

        # Act
        response = self.session.send_prompt(prompt, role)

        # Adjust this to include the assistant's response in the expected messages
        expected_messages = [
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": "Mocked API Response",
            },  # This line reflects the response added to messages
        ]

        # Assert
        self.mock_openai_chat_completions.assert_called_once_with(
            model=self.session.model, messages=expected_messages
        )
        self.assertIn("Mocked API Response", response)

        # Additional checks to ensure that all messages are correctly appended
        self.assertEqual(len(self.session.messages), len(expected_messages))
        for message, expected_message in zip(self.session.messages, expected_messages):
            self.assertEqual(message, expected_message)


if __name__ == "__main__":
    unittest.main()
