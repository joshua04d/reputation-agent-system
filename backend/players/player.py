# backend/players/player.py

class Player:
    def __init__(self, player_id, name):
        """
        Represents a player in the game
        """

        self.player_id = player_id
        self.name = name

        # Total resources taken across game
        self.total_taken = 0

        # Current round choice
        self.current_choice = 0

    def make_choice(self, amount):
        """
        Player selects amount to take
        """
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        self.current_choice = amount

    def finalize_choice(self):
        """
        Add current choice to total
        """
        self.total_taken += self.current_choice

    def reset_choice(self):
        """
        Clear current round choice
        """
        self.current_choice = 0
