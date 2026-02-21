# backend/data_logger.py

import csv
import json
import os


class DataLogger:

    def __init__(self):

        self.data_dir = "data"

        os.makedirs(self.data_dir, exist_ok=True)

        self.reputation_file = os.path.join(self.data_dir, "reputation_history.csv")

        self.explanation_file = os.path.join(self.data_dir, "explanations.json")

        # Initialize files
        self.init_reputation_file()

        self.explanations = []

    def init_reputation_file(self):

        with open(self.reputation_file, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "round",
                "player_id",
                "reputation"
            ])

    def log_reputation(self, round_num, reputation_scores):

        with open(self.reputation_file, "a", newline="") as f:

            writer = csv.writer(f)

            for player_id, score in reputation_scores.items():

                writer.writerow([
                    round_num,
                    player_id,
                    score
                ])

    def log_explanation(self, round_num, agent_id, explanation):

        self.explanations.append({
            "round": round_num,
            "agent_id": agent_id,
            "explanation": explanation
        })

    def save_explanations(self):

        with open(self.explanation_file, "w") as f:

            json.dump(self.explanations, f, indent=4)
