# backend/players/player_manager.py

from backend.players.player import Player


class PlayerManager:
    def __init__(self):
        """
        Manages all players in game
        """

        # Dictionary of players
        # format: {player_id: Player}
        self.players = {}

        self.next_player_id = 1

    def add_player(self, name):
        """
        Adds new player to game
        """

        player_id = self.next_player_id

        player = Player(player_id, name)

        self.players[player_id] = player

        self.next_player_id += 1

        return player

    def get_player(self, player_id):
        return self.players.get(player_id)

    def get_all_players(self):
        return list(self.players.values())

    def get_total_players(self):
        return len(self.players)
