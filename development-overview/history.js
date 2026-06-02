/**
 * Org activity time series for the development overview (committed history.json + live API).
 */
(function () {
  const HISTORY_URL = "./history.json";

  /** @type {{ version?: number, org?: string, points: Array<Record<string, unknown>> }} */
  let committed = { points: [] };
  /** @type {Record<string, unknown> | null} */
  let livePoint = null;

  const CHARTS = [
    { key: "open_prs", label: "Open PRs", color: "#58a6ff" },
    { key: "prs_closed", label: "Closed PRs (total)", color: "#3fb950" },
    { key: "issues_open", label: "Open issues", color: "#d29922" },
    { key: "issues_closed", label: "Closed issues (total)", color: "#a371f7" },
  ];

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

  function renderChart(points, spec) {
    const values = points
      .map((p) => ({ at: p.at, v: typeof p[spec.key] === "number" ? p[spec.key] : null }))
      .filter((row) => row.v !== null);
    const w = 280;
    const h = 120;
    const pad = { l: 36, r: 8, t: 8, b: 22 };
    const innerW = w - pad.l - pad.r;
    const innerH = h - pad.t - pad.b;

    if (values.length === 0) {
      return `<div class="history-chart"><h3>${esc(spec.label)}</h3><p class="history-empty">No data yet</p></div>`;
    }

    const ys = values.map((r) => r.v);
    let yMin = Math.min(...ys);
    let yMax = Math.max(...ys);
    if (yMin === yMax) {
      yMin = Math.max(0, yMin - 1);
      yMax = yMax + 1;
    }
    const yPad = (yMax - yMin) * 0.08 || 1;
    yMin = Math.max(0, yMin - yPad);
    yMax = yMax + yPad;

    const xScale = (i) => pad.l + (values.length === 1 ? innerW / 2 : (i / (values.length - 1)) * innerW);
    const yScale = (v) => pad.t + innerH - ((v - yMin) / (yMax - yMin)) * innerH;

    const coords = values.map((r, i) => `${xScale(i)},${yScale(r.v)}`).join(" ");
    const last = values[values.length - 1];
    const first = values[0];

    return `<div class="history-chart">
      <h3>${esc(spec.label)}</h3>
      <svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="${esc(spec.label)} over time">
        <line x1="${pad.l}" y1="${pad.t + innerH}" x2="${w - pad.r}" y2="${pad.t + innerH}" stroke="#30363d" />
        <line x1="${pad.l}" y1="${pad.t}" x2="${pad.l}" y2="${pad.t + innerH}" stroke="#30363d" />
        <text x="${pad.l - 4}" y="${pad.t + 4}" fill="#8b949e" font-size="9" text-anchor="end">${Math.round(yMax)}</text>
        <text x="${pad.l - 4}" y="${pad.t + innerH}" fill="#8b949e" font-size="9" text-anchor="end">${Math.round(yMin)}</text>
        <polyline fill="none" stroke="${spec.color}" stroke-width="2" points="${coords}" />
        <circle cx="${xScale(values.length - 1)}" cy="${yScale(last.v)}" r="3" fill="${spec.color}" />
        <text x="${pad.l}" y="${h - 4}" fill="#8b949e" font-size="9">${esc(fmtShortDate(first.at))}</text>
        <text x="${w - pad.r}" y="${h - 4}" fill="#8b949e" font-size="9" text-anchor="end">${esc(fmtShortDate(last.at))}</text>
        <text x="${w - pad.r}" y="${pad.t + 10}" fill="${spec.color}" font-size="10" text-anchor="end">${last.v.toLocaleString()}</text>
      </svg>
    </div>`;
  }

  function paint() {
    const grid = document.getElementById("history-charts");
    const status = document.getElementById("history-status");
    if (!grid) return;

    const points = mergedPoints();
    grid.innerHTML = CHARTS.map((spec) => renderChart(points, spec)).join("");

    if (status) {
      const n = points.length;
      const sources = livePoint ? "committed snapshots + live API" : "committed snapshots";
      status.textContent =
        n > 0
          ? `${n} day${n === 1 ? "" : "s"} of data (${sources}). Run refresh-development-overview.sh to append offline snapshots.`
          : "Run refresh-development-overview.sh to seed history, or wait for live GitHub API counts.";
    }
  }

  async function loadCommitted() {
    try {
      const res = await fetch(HISTORY_URL, { cache: "no-store" });
      if (res.ok) committed = await res.json();
    } catch {
      committed = { points: [] };
    }
    paint();
  }

  function updateLive(point) {
    livePoint = point;
    paint();
  }

  window.DevelopmentOverviewHistory = { updateLive, paint, mergedPoints };

  loadCommitted();
})();
