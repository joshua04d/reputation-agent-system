# backend/players/player_manager.py

from backend.players.player import Player


class PlayerManager:

    def __init__(self):
        """
        Manages all players in the game (human and AI)
        """

        # format: {player_id: Player}
        self.players = {}

        self.next_player_id = 1

    # -----------------------------
    # Add human player
    # -----------------------------
    def add_player(self, name):

        player_id = self.next_player_id

        player = Player(
            player_id=player_id,
            name=name,
            is_agent=False,
            agent=None
        )

        self.players[player_id] = player

        self.next_player_id += 1

        return player

    # -----------------------------
    # Add AI agent player
    # -----------------------------
    def add_agent_player(self, name, agent):

        player_id = self.next_player_id

        player = Player(
            player_id=player_id,
            name=name,
            is_agent=True,
            agent=agent
        )

        self.players[player_id] = player

        self.next_player_id += 1

        return player

    # -----------------------------
    # Get player by ID
    # -----------------------------
    def get_player(self, player_id):

        return self.players.get(player_id)

    # -----------------------------
    # Get all players
    # -----------------------------
    def get_all_players(self):

        return list(self.players.values())

    # -----------------------------
    # Get total players count
    # -----------------------------
    def get_total_players(self):

        return len(self.players)

    # -----------------------------
    # Get only AI agents
    # -----------------------------
    def get_all_agents(self):

        return [p for p in self.players.values() if p.is_agent]

    # -----------------------------
    # Get only human players
    # -----------------------------
    def get_all_humans(self):

        return [p for p in self.players.values() if not p.is_agent]
