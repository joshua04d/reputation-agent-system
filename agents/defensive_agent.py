# agents/defensive_agent.py

from agents.agent_base import BaseAgent


class DefensiveAgent(BaseAgent):

    def decide_take_amount(self, fair_share, player_reputations):

        avg_rep = sum(player_reputations.values()) / len(player_reputations)

        if avg_rep < 40:
            # low trust environment → defensive
            return fair_share * 1.2
        else:
            return fair_share
