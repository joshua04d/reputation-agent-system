# backend/game/game_state.py

class GameState:
    def __init__(self, max_players=4, max_rounds=20, initial_pool=100):
        """
        Stores the current state of the game
        """

        # Game configuration
        self.max_players = max_players
        self.max_rounds = max_rounds
        self.initial_pool = initial_pool

        # Dynamic state
        self.current_round = 1
        self.resource_pool = initial_pool

        # Player choices for current round
        # format: {player_id: amount_taken}
        self.player_choices = {}

        # Game status
        self.game_active = True

    def reset_round(self):
        """
        Clears player choices for next round
        """
        self.player_choices = {}

    def add_player_choice(self, player_id, amount):
        """
        Stores a player's choice for current round
        """
        if not self.game_active:
            raise Exception("Game is not active")

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        self.player_choices[player_id] = amount

    def all_players_submitted(self, total_players):
        """
        Checks if all players submitted their choices
        """
        return len(self.player_choices) == total_players

    def advance_round(self):
        """
        Moves game to next round
        """
        self.current_round += 1

        if self.current_round > self.max_rounds:
            self.game_active = False

        self.reset_round()

    def get_total_taken(self):
        """
        Returns total amount taken this round
        """
        return sum(self.player_choices.values())
