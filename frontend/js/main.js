const API = "http://127.0.0.1:8000";

let chart;

async function startGame() {

    const humans = document.getElementById("humans").value;
    const agents = document.getElementById("agents").value;
    const rounds = document.getElementById("rounds").value;

    await fetch(`${API}/start-game?num_humans=${humans}&num_agents=${agents}&rounds=${rounds}`, {
        method: "POST"
    });

}

async function updateDashboard() {

    const status = await fetch(`${API}/game-status`).then(r => r.json());

    document.getElementById("status").innerHTML =
        `Round ${status.current_round} / ${status.max_rounds}`;

    const players = await fetch(`${API}/players`).then(r => r.json());

    document.getElementById("players").innerHTML =
        players.players.map(p =>
            `${p.name}: ${p.reputation}`
        ).join("<br>");

    const explanations = await fetch(`${API}/explanations`).then(r => r.json());

    document.getElementById("explanations").innerHTML =
        explanations.slice(-5).map(e =>
            `Round ${e.round}: ${e.explanation}`
        ).join("<br>");

    updateChart();

}

async function updateChart() {

    const history = await fetch(`${API}/history`).then(r => r.json());

    const labels = history.rounds.map(r => r.round);

    const data = history.rounds.map(r => {

        let sum = 0;

        r.players.forEach(p => sum += p.reputation);

        return sum / r.players.length;
    });

    if (!chart) {

        chart = new Chart(
            document.getElementById("chart"),
            {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Avg Reputation",
                        data: data
                    }]
                }
            }
        );

    } else {

        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.update();
    }
}

setInterval(updateDashboard, 1000);