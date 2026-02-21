# simulations/simulation_runner.py
import matplotlib.pyplot as plt
import random
from backend.server import GameServer
from backend.data_logger import DataLogger


class SimulationRunner:

    def __init__(self, num_humans=5, num_agents=5, num_rounds=10):

        self.num_humans = num_humans
        self.num_agents = num_agents
        self.num_rounds = num_rounds

        self.server = GameServer()

        self.humans = []
        self.agents = []

        # Metrics
        self.cooperation_count = 0
        self.penalty_count = 0
        self.avg_reputation_per_round = []

        self.logger = DataLogger()

    # -----------------------------
    # Setup players
    # -----------------------------
    def setup_players(self):

        for i in range(self.num_humans):
            player = self.server.add_player(f"Human_{i+1}")
            self.humans.append(player)

        for i in range(self.num_agents):
            agent = self.server.add_adaptive_agent(f"AI_{i+1}")
            self.agents.append(agent)

    # -----------------------------
    # Generate human behavior
    # -----------------------------
    def generate_human_choice(self, fair_share):

        behavior_type = random.choice([
            "fair",
            "greedy",
            "cooperative",
            "random"
        ])

        if behavior_type == "fair":
            return fair_share

        elif behavior_type == "greedy":
            return fair_share * random.uniform(1.2, 1.8)

        elif behavior_type == "cooperative":
            return fair_share * random.uniform(0.5, 0.9)

        else:
            return fair_share * random.uniform(0.3, 2.0)

    # -----------------------------
    # Run single round
    # -----------------------------
    def run_round(self, round_num):

        total_players = self.server.player_manager.get_total_players()

        fair_share = self.server.game_state.resource_pool / total_players

        # Humans make decisions
        for human in self.humans:

            choice = self.generate_human_choice(fair_share)

            self.server.submit_choice(human.player_id, choice)

        # AI agents decide
        self.server.run_agent_turns()

        # Process round
        result = self.server.process_round()

        # Track cooperation vs penalty
        penalties = sum(1 for r in result.values() if r["status"] == "penalty")

        if penalties > 0:
            self.penalty_count += 1
        else:
            self.cooperation_count += 1

        # Track average reputation
        reputations = self.server.reputation_engine.reputation_scores.values()

        avg_rep = sum(reputations) / len(reputations)

        self.avg_reputation_per_round.append(avg_rep)

        self.logger.log_reputation(
            round_num,
            self.server.reputation_engine.reputation_scores
        )

    # -----------------------------
    # Run full simulation
    # -----------------------------
    def run_simulation(self):

        print("\nStarting simulation...")

        self.setup_players()

        for round_num in range(1, self.num_rounds + 1):

            self.run_round(round_num)

            if round_num % 10 == 0:
                print(f"Completed round {round_num}")

        print("\nSimulation complete")

        self.print_results()

    # -----------------------------
    # Print metrics
    # -----------------------------
    def print_results(self):

        print("\n=== SIMULATION RESULTS ===")

        print(f"Total Rounds: {self.num_rounds}")
        print(f"Cooperation Rounds: {self.cooperation_count}")
        print(f"Penalty Rounds: {self.penalty_count}")

        cooperation_rate = self.cooperation_count / self.num_rounds

        print(f"Cooperation Rate: {cooperation_rate:.2f}")

        final_avg_rep = self.avg_reputation_per_round[-1]

        print(f"Final Average Reputation: {final_avg_rep:.2f}")

    # -----------------------------
    # Run full simulation
    # -----------------------------
    def run_simulation(self):

        print("\nStarting simulation...")

        self.setup_players()

        for round_num in range(1, self.num_rounds + 1):

            self.run_round(round_num)

            if round_num % 10 == 0:
                print(f"Completed round {round_num}")

        print("\nSimulation complete")

        self.print_results()

        self.logger.save_explanations()

        # FIX: Call graph function here
        self.plot_reputation_graph()


    # -----------------------------
    # Print metrics
    # -----------------------------
    def print_results(self):

        print("\n=== SIMULATION RESULTS ===")

        print(f"Total Rounds: {self.num_rounds}")
        print(f"Cooperation Rounds: {self.cooperation_count}")
        print(f"Penalty Rounds: {self.penalty_count}")

        cooperation_rate = self.cooperation_count / self.num_rounds

        print(f"Cooperation Rate: {cooperation_rate:.2f}")

        final_avg_rep = self.avg_reputation_per_round[-1]

        print(f"Final Average Reputation: {final_avg_rep:.2f}")


    # -----------------------------
    # Plot reputation graph
    # -----------------------------
    def plot_reputation_graph(self):

        plt.figure(figsize=(10, 5))

        plt.plot(self.avg_reputation_per_round, linewidth=2)

        plt.title("Average Reputation vs Time")
        plt.xlabel("Round")
        plt.ylabel("Average Reputation")

        plt.grid(True)

        plt.show()
