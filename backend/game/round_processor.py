# backend/game/round_processor.py


class RoundProcessor:
    def __init__(self, game_state, player_manager):
        """
        Handles round calculations
        """

        self.game_state = game_state
        self.player_manager = player_manager

    def process_round(self):
        """
        Processes round result
        """

        total_taken = self.game_state.get_total_taken()
        pool = self.game_state.resource_pool

        result = {}

        if total_taken <= pool:

            # Successful round
            for player_id, amount in self.game_state.player_choices.items():

                player = self.player_manager.get_player(player_id)

                player.total_taken += amount

                result[player_id] = {
                    "taken": amount,
                    "status": "success"
                }

        else:

            # Pool exceeded → penalty
            for player_id in self.game_state.player_choices:

                result[player_id] = {
                    "taken": 0,
                    "status": "penalty"
                }

        # Move to next round
        self.game_state.advance_round()

        return result
