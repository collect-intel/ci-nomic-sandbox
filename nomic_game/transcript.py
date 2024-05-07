import csv
import time
from datetime import datetime

class Transcript:
    def __init__(self):
        """Initialize the transcript as an empty list to store entries."""
        self.entries = []

    def get(self):
        """Retrieve the current transcript entries sorted by timestamp.

        Returns:
            list of tuple: The current contents of the transcript.
        """
        return sorted(self.entries, key=lambda x: x[1])  # Sort by timestamp

    def append(self, tick, text):
        """Append a new entry to the transcript with current timestamp.

        Args:
            tick (int): The current game tick.
            text (str): The entry text to be appended.
        """
        timestamp = datetime.now()  # Get the current time
        self.entries.append((tick, timestamp, text))

    def write_to_csv(self, filepath):
        """Write the transcript to a CSV file sorted by timestamp.

        Args:
            filepath (str): The path to the file where the transcript should be saved.
        """
        sorted_entries = self.get()
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tick', 'Timestamp', 'Text'])
            for entry in sorted_entries:
                writer.writerow(entry)

    def write_txt_only(self, filepath):
        """Write only the text of each transcript entry to a text file, sorted by timestamp.

        Args:
            filepath (str): The path to the file where the text should be saved.
        """
        sorted_entries = self.get()
        with open(filepath, 'w') as file:
            for _, _, text in sorted_entries:
                file.write(text + "\n")

# Example usage:
if __name__ == "__main__":
    transcript = Transcript()
    transcript.append(1, "First game action")
    transcript.append(1, "Second game action")
    transcript.write_to_csv('game_transcript.csv')
    transcript.write_txt_only('game_transcript.txt')
