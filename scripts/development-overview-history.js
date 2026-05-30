/**
 * Interactive org activity charts (Chart.js) for the development overview.
 */
(function () {
  const HISTORY_URL = "./history.json";
  const CHART_CDN =
    "https://cdn.jsdelivr.net/npm/chart.js@4.4.9/dist/chart.umd.min.js";

  const THEME = {
    grid: "#30363d",
    muted: "#8b949e",
    fg: "#e6edf3",
    panel: "#161b22",
    font: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
  };

  const CHARTS = [
    { key: "open_prs", label: "Open PRs", color: "#58a6ff" },
    { key: "prs_closed", label: "Closed PRs (total)", color: "#3fb950" },
    { key: "issues_open", label: "Open issues", color: "#d29922" },
    { key: "issues_closed", label: "Closed issues (total)", color: "#a371f7" },
  ];

  /** @type {{ version?: number, org?: string, points: Array<Record<string, unknown>> }} */
  let committed = { points: [] };
  /** @type {Record<string, unknown> | null} */
  let livePoint = null;
  /** @type {Map<string, import("chart.js").Chart>} */
  const instances = new Map();
  /** @type {Promise<void> | null} */
  let chartReady = null;

  function esc(s) {
    const el = document.createElement("span");
    el.textContent = String(s);
    return el.innerHTML;
  }

  function parseAt(at) {
    const t = Date.parse(String(at));
    return Number.isFinite(t) ? t : 0;
  }

  function fmtShortDate(at) {
    const d = new Date(parseAt(at));
    if (!Number.isFinite(d.getTime())) return "?";
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  }

  function fmtLongDate(at) {
    const d = new Date(parseAt(at));
    if (!Number.isFinite(d.getTime())) return String(at);
    return d.toLocaleString(undefined, {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function mergedPoints() {
    const byDay = new Map();
    for (const p of committed.points || []) {
      if (!p.at) continue;
      const day = String(p.at).slice(0, 10);
      const prev = byDay.get(day);
      if (!prev || parseAt(p.at) >= parseAt(prev.at)) byDay.set(day, { ...p });
    }
    if (livePoint?.at) {
      const day = String(livePoint.at).slice(0, 10);
      const prev = byDay.get(day);
      if (!prev || parseAt(livePoint.at) >= parseAt(prev.at)) {
        byDay.set(day, { ...prev, ...livePoint });
      }
    }
    return [...byDay.values()].sort((a, b) => parseAt(a.at) - parseAt(b.at));
  }

  function ensureChartJs() {
    if (window.Chart) return Promise.resolve();
    if (chartReady) return chartReady;
    chartReady = new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[src="${CHART_CDN}"]`);
      if (existing) {
        existing.addEventListener("load", () => resolve(), { once: true });
        existing.addEventListener("error", () => reject(new Error("Chart.js load failed")), {
          once: true,
        });
        if (window.Chart) resolve();
        return;
      }
      const script = document.createElement("script");
      script.src = CHART_CDN;
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error("Chart.js load failed"));
      document.head.appendChild(script);
    });
    return chartReady;
  }

  function chartOptions(spec) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "nearest", axis: "x", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: THEME.panel,
          titleColor: THEME.fg,
          bodyColor: THEME.muted,
          borderColor: THEME.grid,
          borderWidth: 1,
          padding: 10,
          displayColors: false,
          callbacks: {
            title: (items) => fmtLongDate(items[0]?.label),
            label: (ctx) => `${spec.label}: ${ctx.parsed.y.toLocaleString()}`,
          },
        },
      },
      scales: {
        x: {
          grid: { color: THEME.grid },
          border: { color: THEME.grid },
          ticks: {
            color: THEME.muted,
            font: { family: THEME.font, size: 10 },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 6,
            callback: (_value, index, ticks) => {
              const raw = ticks[index]?.label;
              return raw ? fmtShortDate(raw) : "";
            },
          },
        },
        y: {
          beginAtZero: true,
          grid: { color: THEME.grid },
          border: { color: THEME.grid },
          ticks: {
            color: THEME.muted,
            font: { family: THEME.font, size: 10 },
            precision: 0,
          },
        },
      },
      elements: {
        point: {
          radius: 2,
          hoverRadius: 5,
          hitRadius: 14,
          hoverBorderWidth: 2,
        },
        line: { tension: 0.25, borderWidth: 2 },
      },
    };
  }

  function destroyCharts() {
    for (const chart of instances.values()) chart.destroy();
    instances.clear();
  }

  function renderChartCanvas(spec, points) {
    const values = points
      .map((p) => ({ at: p.at, v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
      .filter((row) => row.v !== null);

    const id = `history-chart-${spec.key}`;
    if (values.length === 0) {
      return `<div class="history-chart"><h3>${esc(spec.label)}</h3><p class="history-empty">No data yet</p></div>`;
    }

    const last = values[values.length - 1];
    return `<div class="history-chart">
      <div class="history-chart-head">
        <h3>${esc(spec.label)}</h3>
        <span class="history-latest" style="color:${spec.color}">${last.v.toLocaleString()}</span>
      </div>
      <div class="history-canvas-wrap"><canvas id="${id}" aria-label="${esc(spec.label)} over time"></canvas></div>
    </div>`;
  }

  async function paintCharts() {
    const grid = document.getElementById("history-charts");
    const status = document.getElementById("history-status");
    if (!grid) return;

    const points = mergedPoints();
    destroyCharts();
    grid.innerHTML = CHARTS.map((spec) => renderChartCanvas(spec, points)).join("");

    if (status) {
      const n = points.length;
      const sources = livePoint ? "committed snapshots + live API" : "committed snapshots";
      status.textContent =
        n > 0
          ? `${n} day${n === 1 ? "" : "s"} of data (${sources}). Hover charts for values. Run refresh-development-overview.sh to append offline snapshots.`
          : "Run refresh-development-overview.sh to seed history, or wait for live GitHub API counts.";
    }

    if (!points.length) return;

    try {
      await ensureChartJs();
    } catch {
      if (status) status.textContent += " Chart.js failed to load — static fallback unavailable.";
      return;
    }

    for (const spec of CHARTS) {
      const values = points
        .map((p) => ({ at: p.at, v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
        .filter((row) => row.v !== null);
      if (!values.length) continue;

      const canvas = document.getElementById(`history-chart-${spec.key}`);
      if (!canvas) continue;

      const fill = spec.color + "22";
      const chart = new window.Chart(canvas, {
        type: "line",
        data: {
          labels: values.map((row) => row.at),
          datasets: [
            {
              label: spec.label,
              data: values.map((row) => row.v),
              borderColor: spec.color,
              backgroundColor: fill,
              pointBackgroundColor: spec.color,
              pointBorderColor: spec.color,
              pointHoverBackgroundColor: THEME.fg,
              pointHoverBorderColor: spec.color,
              fill: true,
            },
          ],
        },
        options: chartOptions(spec),
      });
      instances.set(spec.key, chart);
    }
  }

  async function loadCommitted() {
    try {
      const res = await fetch(HISTORY_URL, { cache: "no-store" });
      if (res.ok) committed = await res.json();
    } catch {
      committed = { points: [] };
    }
    await paintCharts();
  }

  function updateLive(point) {
    livePoint = point;
    paintCharts();
  }

  window.DevelopmentOverviewHistory = { updateLive, paint: paintCharts, mergedPoints };

  loadCommitted();
})();
