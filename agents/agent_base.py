# agents/agent_base.py

class BaseAgent:
    def __init__(self, agent_id, reputation_engine):
        """
        Base class for all AI agents
        """

        self.agent_id = agent_id
        self.reputation_engine = reputation_engine

    def get_reputation(self, player_id):
        """
        Get reputation score of any player
        """
        return self.reputation_engine.get_reputation(player_id)

    def decide_take_amount(self, fair_share, player_reputations):
        """
        Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")
