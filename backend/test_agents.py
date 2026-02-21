from reputation.reputation_engine import ReputationEngine
from agents.adaptive_agent import AdaptiveAgent

# Create reputation engine
rep_engine = ReputationEngine()

# Initialize players
rep_engine.initialize_player(1)
rep_engine.initialize_player(2)
rep_engine.initialize_player(3)

# Manually set reputation for testing
rep_engine.reputation_scores[1] = 80
rep_engine.reputation_scores[2] = 60
rep_engine.reputation_scores[3] = 20

# Create agent
agent = AdaptiveAgent(agent_id=99, reputation_engine=rep_engine)

# Get player reputations
player_reps = rep_engine.reputation_scores

fair_share = 25

decision = agent.decide_take_amount(fair_share, player_reps)

print("Agent decision:", decision)
