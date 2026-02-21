# backend/server.py

from backend.game.game_state import GameState
from backend.players.player_manager import PlayerManager
from backend.game.round_processor import RoundProcessor


class GameServer:

    def __init__(self):

        self.player_manager = PlayerManager()

        self.game_state = GameState()

        self.round_processor = RoundProcessor(
            self.game_state,
            self.player_manager
        )

    def add_player(self, name):

        player = self.player_manager.add_player(name)

        return player

    def submit_choice(self, player_id, amount):

        self.game_state.add_player_choice(player_id, amount)

        total_players = self.player_manager.get_total_players()

        if self.game_state.all_players_submitted(total_players):

            result = self.round_processor.process_round()

            return result

        return None
