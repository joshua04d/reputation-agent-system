# backend/api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import threading
import time

from backend.server import GameServer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"

# GLOBAL GAME STATE
game = {
    "running": False,
    "current_round": 0,
    "max_rounds": 0,
    "server": None
}


@app.post("/start-game")
def start_game(num_humans: int = 5, num_agents: int = 5, rounds: int = 50):

    if game["running"]:
        return {"status": "Game already running"}

    server = GameServer(verbose=False)

    # add humans
    for i in range(num_humans):
        server.add_player(f"Human_{i+1}")

    # add agents
    for i in range(num_agents):
        server.add_adaptive_agent(f"AI_{i+1}")

    game["server"] = server
    game["current_round"] = 0
    game["max_rounds"] = rounds
    game["running"] = True

    threading.Thread(target=run_game_loop).start()

    return {"status": "Game started"}


def run_game_loop():

    server = game["server"]

    while game["current_round"] < game["max_rounds"]:

        total_players = server.player_manager.get_total_players()

        fair_share = server.game_state.resource_pool / total_players

        # simulate humans
        import random
        for player in server.player_manager.get_all_humans():

            choice = fair_share * random.uniform(0.5, 1.5)

            server.submit_choice(player.player_id, choice)

        # agents act
        server.run_agent_turns()

        # process round
        server.process_round()

        game["current_round"] += 1

        time.sleep(1)  # 1 second per round

    game["running"] = False


@app.get("/game-status")
def game_status():

    return {
        "running": game["running"],
        "current_round": game["current_round"],
        "max_rounds": game["max_rounds"]
    }


@app.get("/players")
def get_players():

    file_path = os.path.join(DATA_DIR, "player_data.json")

    if os.path.exists(file_path):
        return json.load(open(file_path))

    return {"players": []}


@app.get("/history")
def get_history():

    file_path = os.path.join(DATA_DIR, "game_history.json")

    if os.path.exists(file_path):
        return json.load(open(file_path))

    return {"rounds": []}


@app.get("/explanations")
def get_explanations():

    file_path = os.path.join(DATA_DIR, "explanations.json")

    if os.path.exists(file_path):
        return json.load(open(file_path))

    return []
