/** Poll status.json for live PR merge queue (GitHub Pages). */
const POLL_MS = 60_000;

function ciClass(ci) {
  return `ci-${ci === "pass" ? "pass" : ci === "fail" ? "fail" : ci === "pending" ? "pending" : "none"}`;
}

function esc(s) {
  const el = document.createElement("span");
  el.textContent = s;
  return el.innerHTML;
}

function renderMetrics(metrics) {
  const cards = [
    ["Ready to merge", metrics.ready_to_merge],
    ["Open PRs", metrics.open_prs],
    ["Blocked / needs work", metrics.blocked],
    ["Live docs", `${metrics.repos_with_live_docs} / ${metrics.repos_total}`],
  ];
  return cards
    .map(
      ([label, value]) =>
        `<div class="metric-card"><p class="label">${esc(label)}</p><p class="value">${esc(String(value))}</p></div>`
    )
    .join("");
}

function renderPrTable(prs) {
  const readyFirst = [...prs].sort((a, b) => Number(b.ready) - Number(a.ready) || a.repo.localeCompare(b.repo));
  return readyFirst
    .map((p) => {
      const title = p.title.length > 72 ? `${p.title.slice(0, 69)}…` : p.title;
      return `<tr>
        <td>${esc(p.repo)}</td>
        <td><a href="${esc(p.url)}">#${p.number}</a></td>
        <td><a href="${esc(p.url)}">${esc(title)}</a></td>
        <td class="mono">${esc(p.base)}</td>
        <td class="${ciClass(p.ci)}">${esc(p.ci)}</td>
        <td>${p.ready ? "yes" : "—"}</td>
      </tr>`;
    })
    .join("");
}

async function loadStatus() {
  const base = new URL("./status.json", window.location.href);
  base.searchParams.set("t", String(Date.now()));
  const res = await fetch(base.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error(`status.json ${res.status}`);
  return res.json();
}

async function refresh() {
  const statusEl = document.getElementById("live-status");
  try {
    const data = await loadStatus();
    document.getElementById("live-metrics").innerHTML = renderMetrics(data.metrics);
    document.getElementById("live-pr-body").innerHTML = renderPrTable(data.pull_requests);
    const at = new Date(data.generated_at);
    statusEl.textContent = `live · updated ${at.toLocaleString()} · polls every ${POLL_MS / 1000}s`;
  } catch (e) {
    statusEl.textContent = `live unavailable: ${e.message}`;
  }
}

refresh();
setInterval(refresh, POLL_MS);
