from backend.server import GameServer


server = GameServer()

p1 = server.add_player("Joshua")
p2 = server.add_player("Alice")
p3 = server.add_player("Bob")


print("Round 1")

print(server.submit_choice(p1.player_id, 20))
print(server.submit_choice(p2.player_id, 30))

result = server.submit_choice(p3.player_id, 40)

print(result)
