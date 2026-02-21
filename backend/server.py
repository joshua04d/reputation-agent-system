# backend/server.py

from backend.game.game_state import GameState
from backend.players.player_manager import PlayerManager
from backend.game.round_processor import RoundProcessor
from reputation.reputation_engine import ReputationEngine
from agents.adaptive_agent import AdaptiveAgent


class GameServer:

    def __init__(self):
        """
        Main controller for the entire game system
        """

        # Player manager
        self.player_manager = PlayerManager()

        # Game state
        self.game_state = GameState()

        # Round processor
        self.round_processor = RoundProcessor(
            self.game_state,
            self.player_manager
        )

        # Reputation engine
        self.reputation_engine = ReputationEngine()

    # -----------------------------
    # Add human player
    # -----------------------------
    def add_player(self, name):

        player = self.player_manager.add_player(name)

        # Initialize reputation
        self.reputation_engine.initialize_player(player.player_id)

        return player

    # -----------------------------
    # Add adaptive AI agent
    # -----------------------------
    def add_adaptive_agent(self, name):
        """
        Adds an adaptive AI agent as a player
        """

        agent_id = self.player_manager.next_player_id

        agent = AdaptiveAgent(
            agent_id=agent_id,
            reputation_engine=self.reputation_engine
        )

        player = self.player_manager.add_agent_player(
            name=name,
            agent=agent
        )

        # Initialize reputation
        self.reputation_engine.initialize_player(player.player_id)

        return player

    # -----------------------------
    # Submit human player choice
    # -----------------------------
    def submit_choice(self, player_id, amount):

        # Store player choice
        self.game_state.add_player_choice(player_id, amount)

        total_players = self.player_manager.get_total_players()

        # Check if round complete
        if self.game_state.all_players_submitted(total_players):

            return self.process_round()

        return None

    # -----------------------------
    # Run AI agent turns
    # -----------------------------
    def run_agent_turns(self):

        total_players = self.player_manager.get_total_players()

        fair_share = self.game_state.resource_pool / total_players

        player_reps = self.reputation_engine.reputation_scores

        for player in self.player_manager.get_all_agents():

            decision = player.agent.decide_take_amount(
                fair_share,
                player_reps
            )

            decision = max(0, decision)

            self.game_state.add_player_choice(
                player.player_id,
                decision
            )

    # -----------------------------
    # Process round and update reputation
    # -----------------------------
    def process_round(self):

        total_players = self.player_manager.get_total_players()

        fair_share = self.game_state.resource_pool / total_players

        round_number = self.game_state.current_round

        result = self.round_processor.process_round()

        # Update reputation
        for pid, data in result.items():

            amount_taken = data["taken"]

            self.reputation_engine.update_reputation(
                player_id=pid,
                amount_taken=amount_taken,
                fair_share=fair_share,
                round_number=round_number
            )

        return result
