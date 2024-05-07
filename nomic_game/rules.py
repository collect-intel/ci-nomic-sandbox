import csv

class GameRules:
    def __init__(self, filepath):
        self.rules = self.load_rules_from_csv(filepath)

    def load_rules_from_csv(self, filepath):
        # Initialize an empty dictionary to store the rules
        rules_dict = {}
        
        # Open the CSV file and parse it
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Checking if the row is not empty
                    try:
                        rule_number, rule_description = self.parse_rule(row[0])
                        rules_dict[rule_number] = rule_description
                    except ValueError as e:
                        raise ValueError(f"Error parsing row: {row} - {e}")

        return rules_dict

    def parse_rule(self, rule_text):
        """Parse a single rule text to extract the number and description.

        Args:
            rule_text (str): The text of the rule including its number and description.

        Returns:
            tuple: A tuple containing the rule number (int) and rule description (str).

        Raises:
            ValueError: If the rule text is malformed.
        """
        # Split the rule text based on the first space after the period, assuming "number. description"
        parts = rule_text.split(' ', 1)
        if len(parts) != 2:
            raise ValueError("Rule text does not contain a valid number and description")

        rule_number_part, rule_description = parts
        # Ensure the rule number ends with a period and strip it off
        if not rule_number_part.endswith('.'):
            raise ValueError("Rule number must end with a period")
        rule_number = rule_number_part[:-1]

        # Attempt to convert the rule number to an integer
        if not rule_number.isdigit():
            raise ValueError("Rule number is not a valid integer")

        return int(rule_number), rule_description.strip()

    def get_rule(self, rule_number):
        # Retrieve a specific rule by number
        return self.rules.get(rule_number, "Rule not found")

    def add_rule(self, rule_number, rule_description):
        # Add or update a rule
        self.rules[rule_number] = rule_description

    def delete_rule(self, rule_number):
        # Delete a rule if it exists
        if rule_number in self.rules:
            del self.rules[rule_number]
