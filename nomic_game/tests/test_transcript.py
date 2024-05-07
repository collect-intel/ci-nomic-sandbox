import unittest
from unittest.mock import patch, mock_open, call
from transcript import Transcript
from datetime import datetime

class TestTranscript(unittest.TestCase):
    def setUp(self):
        """Initialize a new Transcript instance for each test."""
        self.transcript = Transcript()

    def test_initial_state(self):
        """Test the initial state of the transcript is empty."""
        self.assertEqual(self.transcript.get(), [])

    def test_append_single_entry(self):
        """Test appending a single entry to the transcript."""
        with patch('transcript.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 1, 1, 12, 0)
            self.transcript.append(1, "Player 1 moved.")
            self.assertEqual(self.transcript.get(), [(1, datetime(2021, 1, 1, 12, 0), "Player 1 moved.")])

    def test_append_multiple_entries(self):
        """Test appending multiple entries to the transcript."""
        with patch('transcript.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 1, 1, 12, 0)
            self.transcript.append(1, "Player 1 moved.")
            mock_datetime.now.return_value = datetime(2021, 1, 1, 12, 1)
            self.transcript.append(2, "Player 2 moved.")
            self.assertEqual(self.transcript.get(), [
                (1, datetime(2021, 1, 1, 12, 0), "Player 1 moved."),
                (2, datetime(2021, 1, 1, 12, 1), "Player 2 moved.")
            ])

    @patch('builtins.open', new_callable=mock_open)
    def test_write_to_csv(self, mock_file):
        """Test writing the transcript to a CSV file."""
        self.transcript.entries = [
            (1, datetime(2021, 1, 1, 12, 0), "Game started."),
            (2, datetime(2021, 1, 1, 12, 1), "Player 1 moved.")
        ]
        self.transcript.write_to_csv("game_transcript.csv")
        
        # Verify the open call was made correctly
        mock_file.assert_called_once_with("game_transcript.csv", 'w', newline='')

        # Get the mock file handle
        handle = mock_file()

        # Prepare the expected calls to the write method
        expected_calls = [
            call('Tick,Timestamp,Text\r\n'),
            call('1,2021-01-01 12:00:00,Game started.\r\n'),
            call('2,2021-01-01 12:01:00,Player 1 moved.\r\n')
        ]

        # Verify that write was called exactly as expected
        handle.write.assert_has_calls(expected_calls, any_order=False)

        # Optionally, check that the number of calls matches the expected number
        self.assertEqual(handle.write.call_count, len(expected_calls))


    @patch('builtins.open', new_callable=mock_open)
    def test_write_txt_only(self, mock_file):
        """Test writing only text to a text file."""
        self.transcript.entries = [
            (1, datetime(2021, 1, 1, 12, 0), "Game started."),
            (2, datetime(2021, 1, 1, 12, 1), "Player 1 moved.")
        ]
        self.transcript.write_txt_only("game_transcript.txt")
        
        # Check that the file was opened correctly
        mock_file.assert_called_once_with("game_transcript.txt", 'w')
        
        # Get the mock file handle
        handle = mock_file()

        # Prepare the expected calls to the write method
        expected_calls = [
            call("Game started.\n"),
            call("Player 1 moved.\n")
        ]

        # Verify that write was called exactly as expected
        handle.write.assert_has_calls(expected_calls, any_order=False)
        
        # Optionally, verify the total number of calls matches the expected number
        self.assertEqual(handle.write.call_count, len(expected_calls))


if __name__ == "__main__":
    unittest.main()
