# experiments/experiment_runner.py

import csv
import os

from simulations.simulation_runner import SimulationRunner


class ExperimentRunner:

    def __init__(self):

        self.results_dir = "data/experiments"

        os.makedirs(self.results_dir, exist_ok=True)

        self.results_file = os.path.join(
            self.results_dir,
            "experiment_results.csv"
        )

        self.init_results_file()

    def init_results_file(self):

        with open(self.results_file, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "experiment_name",
                "num_humans",
                "num_agents",
                "num_rounds",
                "cooperation_rate",
                "final_avg_reputation"
            ])

    def run_experiment(
        self,
        experiment_name,
        num_humans,
        num_agents,
        num_rounds
    ):

        print(f"\nRunning experiment: {experiment_name}")

        sim = SimulationRunner(
            num_humans=num_humans,
            num_agents=num_agents,
            num_rounds=num_rounds
        )

        sim.run_simulation()

        cooperation_rate = sim.cooperation_count / sim.num_rounds

        final_avg_rep = sim.avg_reputation_per_round[-1]

        self.save_result(
            experiment_name,
            num_humans,
            num_agents,
            num_rounds,
            cooperation_rate,
            final_avg_rep
        )

    def save_result(
        self,
        experiment_name,
        num_humans,
        num_agents,
        num_rounds,
        cooperation_rate,
        final_avg_rep
    ):

        with open(self.results_file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                experiment_name,
                num_humans,
                num_agents,
                num_rounds,
                cooperation_rate,
                final_avg_rep
            ])

    def run_all_experiments(self):

        # Experiment 1: Balanced system
        self.run_experiment(
            "balanced_system",
            num_humans=5,
            num_agents=5,
            num_rounds=100
        )

        # Experiment 2: AI only
        self.run_experiment(
            "ai_only",
            num_humans=0,
            num_agents=10,
            num_rounds=100
        )

        # Experiment 3: Human only
        self.run_experiment(
            "human_only",
            num_humans=10,
            num_agents=0,
            num_rounds=100
        )

        # Experiment 4: Agent dominated
        self.run_experiment(
            "agent_dominated",
            num_humans=2,
            num_agents=8,
            num_rounds=100
        )

        print("\nAll experiments completed")
