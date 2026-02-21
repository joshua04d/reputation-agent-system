# reputation/reputation_engine.py

class ReputationEngine:
    def __init__(self):
        """
        Stores and manages reputation scores and player history
        """

        # Store reputation scores
        # format: {player_id: score}
        self.reputation_scores = {}

        # Store player history
        # format: {player_id: [ {round, taken, fair_share, fairness}, ... ] }
        self.player_history = {}

        # Default starting reputation
        self.default_reputation = 50

        # Score limits
        self.max_score = 100
        self.min_score = 0

    # -----------------------------
    # Initialize player reputation
    # -----------------------------
    def initialize_player(self, player_id):
        """
        Initialize reputation and history for new player
        """

        if player_id not in self.reputation_scores:
            self.reputation_scores[player_id] = self.default_reputation
            self.player_history[player_id] = []

    # -----------------------------
    # Update reputation after round
    # -----------------------------
    def update_reputation(self, player_id, amount_taken, fair_share, round_number):
        """
        Updates player reputation based on fairness
        """

        self.initialize_player(player_id)

        # Calculate fairness ratio
        fairness_ratio = amount_taken / fair_share if fair_share > 0 else 1

        # Determine fairness score change
        if fairness_ratio <= 1:
            # Fair behavior → increase reputation
            change = 2
            fairness = "fair"
        elif fairness_ratio <= 1.5:
            # Slightly greedy → small penalty
            change = -2
            fairness = "greedy"
        else:
            # Very greedy → big penalty
            change = -5
            fairness = "very_greedy"

        # Update reputation score
        new_score = self.reputation_scores[player_id] + change

        # Clamp score between min and max
        new_score = max(self.min_score, min(self.max_score, new_score))

        self.reputation_scores[player_id] = new_score

        # Store history
        self.player_history[player_id].append({
            "round": round_number,
            "taken": amount_taken,
            "fair_share": fair_share,
            "fairness": fairness,
            "score": new_score
        })

    # -----------------------------
    # Get reputation score
    # -----------------------------
    def get_reputation(self, player_id):
        """
        Returns player's reputation score
        """

        return self.reputation_scores.get(player_id, self.default_reputation)

    # -----------------------------
    # Get player history
    # -----------------------------
    def get_player_history(self, player_id):
        """
        Returns full behavior history of player
        """

        return self.player_history.get(player_id, [])

    # -----------------------------
    # Debug print reputation table
    # -----------------------------
    def print_all_reputations(self):

        print("\n--- Reputation Scores ---")

        for player_id, score in self.reputation_scores.items():
            print(f"Player {player_id}: {score}")
