/* ─── frontend/js/main.js ──────────────────────────────────────────────────
   Reputation Agent System — Dashboard Logic
   Polls FastAPI backend and drives all live UI updates
──────────────────────────────────────────────────────────────────────────── */

const API = "http://127.0.0.1:8000";

/* ── State ── */
let repChart = null;
let poolChart = null;
let currentFilter = "all";
let explanationCount = 0;
let lastExplanationIndex = 0;
let isRunning = false;

/* ── Chart colour palette for individual players ── */
const PLAYER_COLORS = [
  "#3b82f6","#a855f7","#22c55e","#f59e0b","#ef4444",
  "#06b6d4","#ec4899","#84cc16","#f97316","#8b5cf6",
  "#14b8a6","#eab308","#e879f9","#fb923c","#4ade80"
];

/* ═══════════════════════════════════════════════
   CHARTS  (Chart.js 4)
═══════════════════════════════════════════════ */

const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 400 },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "rgba(15,23,42,0.92)",
      borderColor: "rgba(255,255,255,0.1)",
      borderWidth: 1,
      titleColor: "#94a3b8",
      bodyColor: "#f1f5f9",
      padding: 10,
      callbacks: {
        label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)}`
      }
    }
  },
  scales: {
    x: {
      ticks: { color: "#475569", font: { family: "JetBrains Mono", size: 10 } },
      grid: { color: "rgba(255,255,255,0.04)" }
    },
    y: {
      ticks: { color: "#475569", font: { family: "JetBrains Mono", size: 10 } },
      grid: { color: "rgba(255,255,255,0.04)" }
    }
  }
};

function initRepChart() {
  const ctx = document.getElementById("rep-chart").getContext("2d");
  repChart = new Chart(ctx, {
    type: "line",
    data: { labels: [], datasets: [] },
    options: {
      ...chartDefaults,
      scales: {
        ...chartDefaults.scales,
        y: {
          ...chartDefaults.scales.y,
          min: 0,
          max: 100,
          ticks: {
            ...chartDefaults.scales.y.ticks,
            callback: v => v
          }
        }
      }
    }
  });
}

function initPoolChart() {
  const ctx = document.getElementById("pool-chart").getContext("2d");
  poolChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [],
      datasets: [{
        label: "Resource Pool",
        data: [],
        backgroundColor: "rgba(245,158,11,0.25)",
        borderColor: "#f59e0b",
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      ...chartDefaults,
      plugins: { ...chartDefaults.plugins, legend: { display: false } }
    }
  });
}

/* ── Update Reputation Chart (one dataset per player) ── */
function updateRepChart(history, players) {
  if (!repChart) return;

  const labels = history.map(r => `R${r.round}`);

  // Build player ID → name map
  const nameMap = {};
  players.forEach(p => { nameMap[p.player_id] = p.name; });

  // Collect all player IDs that appear across rounds
  const pidSet = new Set();
  history.forEach(r => r.players.forEach(p => pidSet.add(p.player_id)));
  const pids = [...pidSet];

  // Update datasets
  repChart.data.labels = labels;
  repChart.data.datasets = pids.map((pid, i) => {
    const color = PLAYER_COLORS[i % PLAYER_COLORS.length];
    const data = history.map(r => {
      const entry = r.players.find(p => p.player_id === pid);
      return entry ? entry.reputation : null;
    });
    return {
      label: nameMap[pid] || `Player ${pid}`,
      data,
      borderColor: color,
      backgroundColor: color + "22",
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 4,
      tension: 0.4,
      spanGaps: true
    };
  });

  repChart.update("none");
  updateRepLegend(pids, players);
}

/* ── Update Pool Chart ── */
function updatePoolChart(history) {
  if (!poolChart) return;
  const last20 = history.slice(-20);
  poolChart.data.labels = last20.map(r => `R${r.round}`);
  poolChart.data.datasets[0].data = last20.map(r => r.resource_pool);
  poolChart.update("none");
}

/* ── Legend ── */
function updateRepLegend(pids, players) {
  const el = document.getElementById("rep-legend");
  if (!el || pids.length === 0) return;

  // Show only first 6 + "…"
  const shown = pids.slice(0, 6);
  const nameMap = {};
  players.forEach(p => { nameMap[p.player_id] = p.name; });

  el.innerHTML = shown.map((pid, i) =>
    `<div class="legend-item">
       <div class="legend-dot" style="background:${PLAYER_COLORS[i % PLAYER_COLORS.length]}"></div>
       <span>${nameMap[pid] || `P${pid}`}</span>
     </div>`
  ).join("") + (pids.length > 6 ? `<span class="legend-item" style="color:var(--text-3)">+${pids.length - 6} more</span>` : "");
}

/* ═══════════════════════════════════════════════
   STAT CARDS
═══════════════════════════════════════════════ */

function animateStat(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove("fade-update");
  void el.offsetWidth; // force reflow
  el.textContent = value;
  el.classList.add("fade-update");
}

function updateStats(status, players, history) {
  animateStat("stat-round", status.current_round > 0 ? status.current_round : "—");
  animateStat("stat-players", players.length > 0 ? players.length : "—");

  if (players.length > 0) {
    const avgRep = players.reduce((s, p) => s + p.reputation, 0) / players.length;
    animateStat("stat-rep", avgRep.toFixed(1));
  }

  if (history.length > 0) {
    const lastRound = history[history.length - 1];
    animateStat("stat-pool", lastRound.resource_pool.toFixed(0));
  }

  // Round badge
  document.getElementById("round-badge").textContent =
    status.current_round > 0
      ? `Round ${status.current_round} / ${status.max_rounds}`
      : "Round — / —";
}

/* ═══════════════════════════════════════════════
   PLAYER TABLE
═══════════════════════════════════════════════ */

function setFilter(filter, btn) {
  currentFilter = filter;
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  // re-render with last known players (stored globally)
  if (window._lastPlayers) renderPlayerTable(window._lastPlayers);
}

function repColor(score) {
  if (score >= 70) return "#22c55e";
  if (score >= 50) return "#3b82f6";
  if (score >= 30) return "#f59e0b";
  return "#ef4444";
}

function getLastStatus(pid, history) {
  for (let i = history.length - 1; i >= 0; i--) {
    const entry = history[i].players.find(p => p.player_id === pid);
    if (entry && entry.status) return entry.status;
  }
  return null;
}

function renderPlayerTable(players) {
  window._lastPlayers = players;
  const tbody = document.getElementById("player-tbody");

  let filtered = players;
  if (currentFilter === "human") filtered = players.filter(p => !p.is_agent);
  if (currentFilter === "agent") filtered = players.filter(p => p.is_agent);

  // Sort: descending reputation
  filtered = [...filtered].sort((a, b) => b.reputation - a.reputation);

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="6">No players match this filter</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map((p, idx) => {
    const rank = idx + 1;
    const rankClass = rank <= 3 ? ` rank--${rank}` : "";
    const color = repColor(p.reputation);
    const status = getLastStatus(p.player_id, window._lastHistory || []);
    const statusChip = status
      ? `<span class="status-chip status-chip--${status}">${status.replace("_", " ")}</span>`
      : `<span style="color:var(--text-3);font-size:0.75rem">—</span>`;

    return `
      <tr>
        <td><span class="rank${rankClass}">#${rank}</span></td>
        <td style="font-weight:600">${p.name}</td>
        <td>
          <span class="type-badge type-badge--${p.is_agent ? 'agent' : 'human'}">
            ${p.is_agent ? '🤖 AI' : '👤 Human'}
          </span>
        </td>
        <td>
          <div class="rep-bar-wrap">
            <div class="rep-bar-bg">
              <div class="rep-bar-fill" style="width:${p.reputation}%;background:${color}"></div>
            </div>
            <span class="rep-val" style="color:${color}">${p.reputation.toFixed(0)}</span>
          </div>
        </td>
        <td style="font-family:var(--mono);font-size:0.82rem">${p.total_taken.toFixed(1)}</td>
        <td>${statusChip}</td>
      </tr>`;
  }).join("");
}

/* ═══════════════════════════════════════════════
   EXPLANATION FEED
═══════════════════════════════════════════════ */

function renderExplanations(explanations) {
  const feed = document.getElementById("explain-feed");
  const countEl = document.getElementById("explain-count");
  explanationCount = explanations.length;
  countEl.textContent = `${explanationCount} event${explanationCount !== 1 ? "s" : ""}`;

  if (explanations.length === 0) {
    feed.innerHTML = `
      <div class="explain-empty">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <p>AI explanations will appear here once the simulation starts</p>
      </div>`;
    return;
  }

  // Show newest 30, newest on top
  const shown = explanations.slice(-30).reverse();

  if (lastExplanationIndex === explanations.length) return; // no change
  lastExplanationIndex = explanations.length;

  feed.innerHTML = shown.map(e => `
    <div class="explain-item">
      <div class="explain-meta">
        <span class="explain-round">Round ${e.round}</span>
        <span class="explain-agent">Agent ${e.agent_id ?? e.agent_id ?? "?"}</span>
      </div>
      <p class="explain-text">${e.explanation}</p>
    </div>`
  ).join("");
}

/* ═══════════════════════════════════════════════
   LIVE BADGE & CLOCK
═══════════════════════════════════════════════ */

function updateLiveBadge(running) {
  const badge = document.getElementById("live-badge");
  const text  = document.getElementById("live-text");
  badge.className = "live-badge";
  if (running) {
    badge.classList.add("live-badge--live");
    text.textContent = "LIVE";
    isRunning = true;
  } else if (isRunning) {
    badge.classList.add("live-badge--done");
    text.textContent = "DONE";
  } else {
    badge.classList.add("live-badge--idle");
    text.textContent = "IDLE";
  }
}

function updateClock() {
  const now = new Date();
  document.getElementById("header-clock").textContent =
    now.toLocaleTimeString("en-US", { hour12: false });
}

/* ═══════════════════════════════════════════════
   START GAME
═══════════════════════════════════════════════ */

async function startGame() {
  const btn = document.getElementById("start-btn");
  const humans = document.getElementById("humans").value;
  const agents = document.getElementById("agents").value;
  const rounds = document.getElementById("rounds").value;

  btn.disabled = true;
  btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Starting…`;

  try {
    const res = await fetch(
      `${API}/start-game?num_humans=${humans}&num_agents=${agents}&rounds=${rounds}`,
      { method: "POST" }
    );
    const data = await res.json();
    console.log("Start game response:", data);

    // Reset state
    lastExplanationIndex = 0;
    isRunning = false;
    window._lastHistory = [];
    window._lastPlayers = [];

    // Clear charts
    if (repChart)  { repChart.data.labels = [];  repChart.data.datasets = [];  repChart.update("none"); }
    if (poolChart) { poolChart.data.labels = []; poolChart.data.datasets[0].data = []; poolChart.update("none"); }

  } catch (err) {
    console.error("Failed to start game:", err);
    alert("⚠️ Could not connect to the backend. Make sure FastAPI is running on port 8000.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Simulation`;
  }
}

/* ═══════════════════════════════════════════════
   MAIN POLLING LOOP
═══════════════════════════════════════════════ */

async function safeFetch(url) {
  try {
    const res = await fetch(url);
    return await res.json();
  } catch {
    return null;
  }
}

async function updateDashboard() {
  const [status, playersData, history, explanations] = await Promise.all([
    safeFetch(`${API}/game-status`),
    safeFetch(`${API}/players`),
    safeFetch(`${API}/history`),
    safeFetch(`${API}/explanations`)
  ]);

  if (!status) return; // backend not available

  const players  = playersData?.players  || [];
  const rounds   = history?.rounds       || [];
  const explains = explanations          || [];

  window._lastHistory = rounds;

  updateLiveBadge(status.running);
  updateStats(status, players, rounds);
  renderPlayerTable(players);
  renderExplanations(explains);
  updateRepChart(rounds, players);
  updatePoolChart(rounds);
}

/* ═══════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════ */

function init() {
  initRepChart();
  initPoolChart();
  updateClock();
  setInterval(updateClock, 1000);
  updateDashboard();
  setInterval(updateDashboard, 2000);
}

document.addEventListener("DOMContentLoaded", init);