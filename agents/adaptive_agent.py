# agents/adaptive_agent.py

from agents.agent_base import BaseAgent


class AdaptiveAgent(BaseAgent):

    def decide_take_amount(self, fair_share, player_reputations):

        avg_rep = sum(player_reputations.values()) / len(player_reputations)

        if avg_rep >= 70:
            # very high trust → reward cooperation
            return fair_share * 0.8

        elif avg_rep >= 50:
            # moderate trust → neutral
            return fair_share

        elif avg_rep >= 30:
            # low trust → defensive
            return fair_share * 1.2

        else:
            # very low trust → greedy survival mode
            return fair_share * 1.5
