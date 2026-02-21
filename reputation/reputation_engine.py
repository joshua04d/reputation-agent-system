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
        # Base fairness change
        new_score = self.reputation_scores[player_id] + change
        
        # Add consistency bonus/penalty
        consistency_change = self.calculate_consistency_score(player_id)
        new_score += consistency_change
        
        # Add recovery bonus
        recovery_change = self.calculate_recovery_score(player_id)
        new_score += recovery_change


        # Clamp score between min and max
        new_score = max(self.min_score, min(self.max_score, new_score))

        self.reputation_scores[player_id] = new_score

        # Store history
        self.player_history[player_id].append({
        "round": round_number,
        "taken": amount_taken,
        "fair_share": fair_share,
        "fairness": fairness,
        "score": new_score,
        "consistency_change": consistency_change,
        "recovery_change": recovery_change
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


    # -----------------------------
    # Calculates consistency based on variation in behavior Lower variation = higher consistency
    # -----------------------------


    def calculate_consistency_score(self, player_id):

        history = self.player_history.get(player_id, [])

        if len(history) < 2:
            return 0

        takes = [entry["taken"] for entry in history]

        avg = sum(takes) / len(takes)

        variance = sum((x - avg) ** 2 for x in takes) / len(takes)

        # Convert variance into score impact
        if variance < 25:
            return 2
        elif variance < 100:
            return 0
        else:
            return -2


    # -----------------------------
    # Rewards player if they improve after greedy behavior
    # -----------------------------

    def calculate_recovery_score(self, player_id):


        history = self.player_history.get(player_id, [])

        if len(history) < 2:
            return 0

        last = history[-1]
        previous = history[-2]

        if previous["fairness"] in ["greedy", "very_greedy"] and last["fairness"] == "fair":
            return 3

        return 0
