# backend/players/player.py

class Player:
    def __init__(self, player_id, name, is_agent=False, agent=None):
        """
        Represents a player (human or AI agent)
        """

        self.player_id = player_id
        self.name = name

        # Agent-related properties
        self.is_agent = is_agent
        self.agent = agent

        # Game tracking
        self.total_taken = 0
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
        Add current choice to total taken
        """

        self.total_taken += self.current_choice

    def reset_choice(self):
        """
        Clear current round choice
        """

        self.current_choice = 0

    def is_ai(self):
        """
        Returns True if player is an AI agent
        """

        return self.is_agent
