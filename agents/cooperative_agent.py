# agents/cooperative_agent.py

from agents.agent_base import BaseAgent


class CooperativeAgent(BaseAgent):

    def decide_take_amount(self, fair_share, player_reputations):
        """
        Cooperative agent always behaves fairly
        """

        return fair_share * 0.9
