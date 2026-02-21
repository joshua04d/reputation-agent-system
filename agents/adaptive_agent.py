# agents/adaptive_agent.py

from agents.agent_base import BaseAgent
from explainer.explanation_engine import ExplanationEngine


class AdaptiveAgent(BaseAgent):

    def __init__(self, agent_id, reputation_engine):

        super().__init__(agent_id, reputation_engine)

        self.explainer = ExplanationEngine()

        self.last_explanation = ""


    def decide_take_amount(self, fair_share, player_reputations):

        avg_rep = sum(player_reputations.values()) / len(player_reputations)

        # Decision logic
        if avg_rep >= 70:

            decision = fair_share * 0.8

        elif avg_rep >= 50:

            decision = fair_share

        elif avg_rep >= 30:

            decision = fair_share * 1.2

        else:

            decision = fair_share * 1.5


        # Generate explanation
        explanation = self.explainer.explain_decision(
            agent_id=self.agent_id,
            decision=decision,
            fair_share=fair_share,
            avg_reputation=avg_rep
        )

        self.last_explanation = explanation

        return decision


    def get_last_explanation(self):

        return self.last_explanation
