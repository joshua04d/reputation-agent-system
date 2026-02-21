# backend/server.py

from backend.game.game_state import GameState
from backend.players import player
from backend.players.player_manager import PlayerManager
from backend.game.round_processor import RoundProcessor
from reputation.reputation_engine import ReputationEngine


class GameServer:

    def __init__(self):
        self.player_manager = PlayerManager()
        self.game_state = GameState()

        self.round_processor = RoundProcessor(
            self.game_state,
            self.player_manager
        )

        # NEW: Reputation engine
        self.reputation_engine = ReputationEngine()

        
    def add_player(self, name):

        player = self.player_manager.add_player(name)

        # Initialize reputation
        self.reputation_engine.initialize_player(player.player_id)

        return player


    def submit_choice(self, player_id, amount):

        # Store player choice
        self.game_state.add_player_choice(player_id, amount)

        total_players = self.player_manager.get_total_players()

        # Check if round complete
        if self.game_state.all_players_submitted(total_players):

            # Calculate fair share
            fair_share = self.game_state.resource_pool / total_players

            round_number = self.game_state.current_round

            # Process round
            result = self.round_processor.process_round()

            # NEW: Update reputation for each player
            for pid, data in result.items():

                amount_taken = data["taken"]

                self.reputation_engine.update_reputation(
                    player_id=pid,
                    amount_taken=amount_taken,
                    fair_share=fair_share,
                    round_number=round_number
                )

            return result

        return None