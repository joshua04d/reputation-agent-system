from backend.server import GameServer

server = GameServer()

p1 = server.add_player("Joshua")   # fair player
p2 = server.add_player("Alice")    # greedy player
p3 = server.add_player("Bob")      # inconsistent player


# Round 1
server.submit_choice(p1.player_id, 20)
server.submit_choice(p2.player_id, 60)
server.submit_choice(p3.player_id, 10)

# Round 2
server.submit_choice(p1.player_id, 22)
server.submit_choice(p2.player_id, 70)
server.submit_choice(p3.player_id, 80)

# Round 3
server.submit_choice(p1.player_id, 24)
server.submit_choice(p2.player_id, 50)
server.submit_choice(p3.player_id, 15)

server.reputation_engine.print_all_reputations()

# print("\nDetailed history:")
# print(server.reputation_engine.player_history)
