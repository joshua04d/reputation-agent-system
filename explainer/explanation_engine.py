# explainer/explanation_engine.py

class ExplanationEngine:

    def __init__(self):
        """
        Generates human-readable explanations for agent decisions
        """
        pass


    def explain_decision(
        self,
        agent_id,
        decision,
        fair_share,
        avg_reputation
    ):
        """
        Generate explanation for agent decision
        """

        ratio = decision / fair_share if fair_share > 0 else 1

        # High trust environment
        if avg_reputation >= 70:

            explanation = (
                f"Agent {agent_id} observed high average reputation "
                f"({avg_reputation:.2f}), indicating a trustworthy environment. "
                f"Therefore, it cooperated by taking less than fair share ({decision:.2f})."
            )

        # Moderate trust
        elif avg_reputation >= 50:

            explanation = (
                f"Agent {agent_id} observed moderate average reputation "
                f"({avg_reputation:.2f}). It maintained fair behavior "
                f"by taking approximately fair share ({decision:.2f})."
            )

        # Low trust
        elif avg_reputation >= 30:

            explanation = (
                f"Agent {agent_id} detected lower average reputation "
                f"({avg_reputation:.2f}), suggesting reduced trust. "
                f"It acted defensively by increasing its share ({decision:.2f})."
            )

        # Very low trust
        else:

            explanation = (
                f"Agent {agent_id} observed very low average reputation "
                f"({avg_reputation:.2f}), indicating an untrustworthy environment. "
                f"It prioritized self-preservation by taking more resources ({decision:.2f})."
            )

        return explanation
