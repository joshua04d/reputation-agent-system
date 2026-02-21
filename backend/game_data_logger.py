# backend/game_data_logger.py

import json
import os


class GameDataLogger:

    def __init__(self):

        self.data_dir = "data"

        os.makedirs(self.data_dir, exist_ok=True)

        self.player_file = os.path.join(self.data_dir, "player_data.json")

        self.history_file = os.path.join(self.data_dir, "game_history.json")

        self.init_files()

    def init_files(self):

        with open(self.player_file, "w") as f:
            json.dump({"players": []}, f, indent=4)

        with open(self.history_file, "w") as f:
            json.dump({"rounds": []}, f, indent=4)

    # -----------------------------
    # Save player data
    # -----------------------------
    def save_players(self, player_manager, reputation_engine):

        players = []

        for player in player_manager.get_all_players():

            players.append({
                "player_id": player.player_id,
                "name": player.name,
                "is_agent": player.is_agent,
                "total_taken": player.total_taken,
                "reputation": reputation_engine.get_reputation(
                    player.player_id
                )
            })

        with open(self.player_file, "w") as f:

            json.dump({"players": players}, f, indent=4)

    # -----------------------------
    # Save round history
    # -----------------------------
    def log_round(
        self,
        round_number,
        resource_pool,
        fair_share,
        round_result,
        reputation_engine
    ):

        with open(self.history_file, "r") as f:

            data = json.load(f)

        round_entry = {
            "round": round_number,
            "resource_pool": resource_pool,
            "fair_share": fair_share,
            "players": []
        }

        for player_id, result in round_result.items():

            round_entry["players"].append({
                "player_id": player_id,
                "taken": result["taken"],
                "status": result["status"],
                "reputation": reputation_engine.get_reputation(player_id)
            })

        data["rounds"].append(round_entry)

        with open(self.history_file, "w") as f:

            json.dump(data, f, indent=4)
