from simulations.simulation_runner import SimulationRunner

sim = SimulationRunner(
    num_humans=5,
    num_agents=5,
    num_rounds=100
)

sim.run_simulation()
