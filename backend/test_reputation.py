from reputation.reputation_engine import ReputationEngine

engine = ReputationEngine()

# Simulate 3 rounds
engine.update_reputation(player_id=1, amount_taken=20, fair_share=25, round_number=1)
engine.update_reputation(player_id=1, amount_taken=30, fair_share=25, round_number=2)
engine.update_reputation(player_id=1, amount_taken=50, fair_share=25, round_number=3)

# Print results
engine.print_all_reputations()

print("\nHistory:")
print(engine.get_player_history(1))
