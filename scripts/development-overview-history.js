/**
 * Interactive org activity charts (Chart.js) — one point per calendar day.
 */
(function () {
  const HISTORY_URL = "./history.json";
  const CHART_CDN =
    "https://cdn.jsdelivr.net/npm/chart.js@4.4.9/dist/chart.umd.min.js";

  const METRIC_KEYS = [
    "open_prs",
    "ready_to_merge",
    "prs_closed",
    "issues_open",
    "issues_closed",
  ];

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

  function dayKey(at) {
    if (!at) return "";
    return String(at).slice(0, 10);
  }

  function fmtDayLabel(day) {
    const d = new Date(day + "T12:00:00Z");
    if (!Number.isFinite(d.getTime())) return day;
    return d.toLocaleDateString(undefined, {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  }

  function fmtShortDay(day) {
    const d = new Date(day + "T12:00:00Z");
    if (!Number.isFinite(d.getTime())) return day;
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  }

  function mergeDaily(prev, nxt) {
    const day = dayKey(nxt?.at || prev?.at);
    const out = { ...(prev || {}), ...(nxt || {}), at: day };
    for (const key of METRIC_KEYS) {
      if (typeof out[key] !== "number" && typeof prev?.[key] === "number") {
        out[key] = prev[key];
      }
    }
    return out;
  }

  /** Collapse intraday snapshots to one row per UTC calendar day. */
  function dailyPoints(raw) {
    const sorted = [...(raw || [])].sort((a, b) => dayKey(a.at).localeCompare(dayKey(b.at)));
    const byDay = new Map();
    for (const p of sorted) {
      const day = dayKey(p.at);
      if (!day) continue;
      byDay.set(day, mergeDaily(byDay.get(day), p));
    }
    return [...byDay.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([, p]) => p);
  }

  function mergedPoints() {
    const raw = [...(committed.points || [])];
    if (livePoint?.at) raw.push(livePoint);
    return dailyPoints(raw);
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
            title: (items) => fmtDayLabel(items[0]?.label),
            label: (ctx) => `${spec.label}: ${ctx.parsed.y.toLocaleString()}`,
          },
        },
      },
      scales: {
        x: {
          type: "category",
          grid: { color: THEME.grid },
          border: { color: THEME.grid },
          ticks: {
            color: THEME.muted,
            font: { family: THEME.font, size: 10 },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 8,
            callback: (value) => {
              const raw = this.getLabelForValue(value);
              return raw ? fmtShortDay(String(raw)) : "";
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
          radius: 3,
          hoverRadius: 6,
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
      .map((p) => ({ day: dayKey(p.at), v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
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
      <div class="history-canvas-wrap"><canvas id="${id}" aria-label="${esc(spec.label)} by day"></canvas></div>
    </div>`;
  }

  async function paintCharts() {
    const grid = document.getElementById("history-charts");
    const status = document.getElementById("history-status");
    if (!grid) return;

    const points = mergedPoints();
    const layoutKey = CHARTS.map((s) => s.key).join(",");
    const prevLayout = grid.dataset.layout;
    const sameLayout = prevLayout === layoutKey && grid.childElementCount === CHARTS.length;
    if (!sameLayout) {
      destroyCharts();
      grid.innerHTML = CHARTS.map((spec) => renderChartCanvas(spec, points)).join("");
      grid.dataset.layout = layoutKey;
    } else {
      for (const spec of CHARTS) {
        const values = points
          .map((p) => ({ day: dayKey(p.at), v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
          .filter((row) => row.v !== null);
        const latest = document.querySelector(`#history-chart-${spec.key}`)?.closest(".history-chart")?.querySelector(".history-latest");
        if (latest && values.length) latest.textContent = values[values.length - 1].v.toLocaleString();
      }
    }

    if (status) {
      const n = points.length;
      const sources = livePoint ? "committed snapshots + live API" : "committed snapshots";
      status.textContent =
        n > 0
          ? `${n} daily point${n === 1 ? "" : "s"} (${sources}). Hover charts for values. Run refresh-development-overview.sh once per day to append snapshots.`
          : "Run refresh-development-overview.sh to seed daily history, or wait for live GitHub API counts.";
    }

    if (!points.length) return;

    try {
      await ensureChartJs();
    } catch {
      if (status) status.textContent += " Chart.js failed to load.";
      return;
    }

    for (const spec of CHARTS) {
      const values = points
        .map((p) => ({ day: dayKey(p.at), v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
        .filter((row) => row.v !== null);
      if (!values.length) continue;

      const labels = values.map((row) => row.day);
      const data = values.map((row) => row.v);
      const existing = instances.get(spec.key);
      if (existing) {
        existing.data.labels = labels;
        existing.data.datasets[0].data = data;
        existing.update("none");
        continue;
      }

      const canvas = document.getElementById(`history-chart-${spec.key}`);
      if (!canvas) continue;

      const fill = spec.color + "22";
      const chart = new window.Chart(canvas, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: spec.label,
              data,
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
    if (!point) return;
    const day = dayKey(point.at) || new Date().toISOString().slice(0, 10);
    const next = { ...(livePoint || {}), at: day };
    for (const key of METRIC_KEYS) {
      if (typeof point[key] === "number") next[key] = point[key];
    }
    if (point.source) next.source = point.source;
    livePoint = next;
    paintCharts();
  }

  window.DevelopmentOverviewHistory = { updateLive, paint: paintCharts, mergedPoints, dailyPoints };

  loadCommitted();
})();
