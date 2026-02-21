# backend/test_game.py

from backend.server import GameServer

# Create server
server = GameServer()

print("\n=== INITIALIZING GAME ===")

# Add 5 human players
h1 = server.add_player("Joshua")
h2 = server.add_player("Alice")
h3 = server.add_player("Bob")
h4 = server.add_player("Charlie")
h5 = server.add_player("David")

# Add 5 AI agents
ai1 = server.add_adaptive_agent("AI_1")
ai2 = server.add_adaptive_agent("AI_2")
ai3 = server.add_adaptive_agent("AI_3")
ai4 = server.add_adaptive_agent("AI_4")
ai5 = server.add_adaptive_agent("AI_5")

# Show players
print("\nPlayers:")
for player in server.player_manager.get_all_players():
    print(f"ID: {player.player_id}, Name: {player.name}, AI: {player.is_agent}")

# Helper function
def run_round(round_num, human_choices):

    print(f"\n=== ROUND {round_num} ===")

    total_players = server.player_manager.get_total_players()
    fair_share = server.game_state.resource_pool / total_players

    print(f"Resource Pool: {server.game_state.resource_pool}")
    print(f"Fair Share: {fair_share:.2f}")

    # Humans submit choices
    server.submit_choice(h1.player_id, human_choices[0])
    server.submit_choice(h2.player_id, human_choices[1])
    server.submit_choice(h3.player_id, human_choices[2])
    server.submit_choice(h4.player_id, human_choices[3])
    server.submit_choice(h5.player_id, human_choices[4])

    # AI agents decide
    server.run_agent_turns()

    # Process round
    result = server.process_round()

    print("\nRound Result:")
    for pid, data in result.items():
        player = server.player_manager.get_player(pid)
        print(f"{player.name}: took {data['taken']} ({data['status']})")

    # Print reputation
    print("\nReputation Scores:")
    server.reputation_engine.print_all_reputations()


# ROUND 1: Mostly fair behavior
run_round(1, [9, 10, 11, 8, 10])

# ROUND 2: Mixed behavior
run_round(2, [12, 15, 9, 20, 10])

# ROUND 3: Some greedy players
run_round(3, [8, 30, 10, 5, 25])

# ROUND 4: Recovery behavior
run_round(4, [10, 12, 9, 11, 10])

# FINAL HISTORY SUMMARY
print("\n=== FINAL HISTORY SUMMARY ===")

for player in server.player_manager.get_all_players():

    print(f"\n{player.name} (ID {player.player_id}):")

    history = server.reputation_engine.get_player_history(player.player_id)

    for entry in history:
        print(
            f"Round {entry['round']} | "
            f"Took {entry['taken']} | "
            f"Fairness: {entry['fairness']} | "
            f"Score: {entry['score']}"
        )
