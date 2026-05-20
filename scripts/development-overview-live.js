/**
 * Live PR merge queue via GitHub public API (browser only — no Actions cron).
 * Search API: 10 req/min. Core API (commit status): 60 req/hr — one PR per 90s.
 */
const ORG = "li-langverse";
const SEARCH_MS = 120_000;
const ECO_MS = 300_000;
const CI_TICK_MS = 90_000;
const SEARCH_URL = `https://api.github.com/search/issues?q=org:${ORG}+is:open+is:pr&per_page=100&sort=updated`;
const ECO_STATS_URL = "./ecosystem-stats.json";

/** @type {{ lines_of_code?: number, packages?: number, issues_open?: number, prs_closed?: number, generated_at?: string }} */
let ecosystemSnapshot = {};

/** @type {Map<string, { ci: string, ready: boolean }>} */
const ciCache = new Map();
let prs = [];
let ciIndex = 0;

const GH_HEADERS = { Accept: "application/vnd.github+json" };

function ciClass(ci) {
  return `ci-${ci === "pass" ? "pass" : ci === "fail" ? "fail" : ci === "pending" ? "pending" : "none"}`;
}

function esc(s) {
  const el = document.createElement("span");
  el.textContent = s;
  return el.innerHTML;
}

function prKey(repo, number) {
  return `${repo}#${number}`;
}

function repoFromApiUrl(repositoryUrl) {
  const parts = repositoryUrl.split("/");
  return parts[parts.length - 1] || repositoryUrl;
}

function mapSearchItem(item) {
  const repo = repoFromApiUrl(item.repository_url);
  const key = prKey(repo, item.number);
  const cached = ciCache.get(key);
  return {
    repo,
    number: item.number,
    title: item.title,
    url: item.pull_request?.html_url || item.html_url,
    base: "main",
    draft: Boolean(item.draft),
    ci: cached?.ci ?? "…",
    ready: cached?.ready ?? false,
    _key: key,
  };
}

function fmtNum(n) {
  if (n === undefined || n === null || Number.isNaN(n)) return "—";
  return Number(n).toLocaleString();
}

function renderEcosystemMetrics(live = {}) {
  const loc = live.lines_of_code ?? ecosystemSnapshot.lines_of_code;
  const packages = live.packages ?? ecosystemSnapshot.packages;
  const issues = live.issues_open ?? ecosystemSnapshot.issues_open;
  const closedPrs = live.prs_closed ?? ecosystemSnapshot.prs_closed;
  const asOf = live.generated_at ?? ecosystemSnapshot.generated_at;
  const asOfEl = document.getElementById("eco-as-of");
  if (asOfEl && asOf) asOfEl.textContent = asOf;

  return [
    ["Lines of code", fmtNum(loc)],
    ["Package repos", fmtNum(packages)],
    ["Open issues", fmtNum(issues)],
    ["Closed PRs", fmtNum(closedPrs)],
  ]
    .map(
      ([label, value]) =>
        `<div class="metric-card"><p class="label">${esc(label)}</p><p class="value">${esc(value)}</p></div>`
    )
    .join("");
}

function paintEcosystem(live = {}) {
  const el = document.getElementById("ecosystem-metrics");
  if (el) el.innerHTML = renderEcosystemMetrics(live);
}

async function searchCount(query) {
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=1`;
  const data = await ghGet(url);
  return typeof data.total_count === "number" ? data.total_count : null;
}

async function loadEcosystemSnapshot() {
  try {
    const res = await fetch(ECO_STATS_URL, { cache: "no-store" });
    if (res.ok) ecosystemSnapshot = await res.json();
  } catch {
    /* static HTML fallback */
  }
  paintEcosystem();
}

async function refreshEcosystemLive() {
  try {
    const [issuesOpen, prsClosed] = await Promise.all([
      searchCount(`org:${ORG} is:issue is:open`),
      searchCount(`org:${ORG} is:pr is:closed`),
    ]);
    paintEcosystem({
      issues_open: issuesOpen ?? undefined,
      prs_closed: prsClosed ?? undefined,
      generated_at: new Date().toISOString().slice(0, 16) + "Z",
    });
  } catch {
    paintEcosystem();
  }
}

function renderMetrics(list) {
  const open = list.length;
  const drafts = list.filter((p) => p.draft).length;
  const ready = list.filter((p) => p.ready).length;
  const blocked = list.filter((p) => !p.ready && !p.draft && p.ci === "fail").length;
  return [
    ["Ready to merge", ready],
    ["Open PRs", open],
    ["Drafts", drafts],
    ["CI failing", blocked],
  ]
    .map(
      ([label, value]) =>
        `<div class="metric-card"><p class="label">${esc(label)}</p><p class="value">${esc(String(value))}</p></div>`
    )
    .join("");
}

function renderPrTable(list) {
  const sorted = [...list].sort(
    (a, b) => Number(b.ready) - Number(a.ready) || a.repo.localeCompare(b.repo)
  );
  return sorted
    .map((p) => {
      const title = p.title.length > 72 ? `${p.title.slice(0, 69)}…` : p.title;
      const draft = p.draft ? ` <span class="ci-none">(draft)</span>` : "";
      return `<tr>
        <td>${esc(p.repo)}</td>
        <td><a href="${esc(p.url)}">#${p.number}</a></td>
        <td><a href="${esc(p.url)}">${esc(title)}</a>${draft}</td>
        <td class="mono">${esc(p.base)}</td>
        <td class="${ciClass(p.ci)}">${esc(p.ci)}</td>
        <td>${p.ready ? "yes" : "—"}</td>
      </tr>`;
    })
    .join("");
}

function paint() {
  document.getElementById("live-metrics").innerHTML = renderMetrics(prs);
  document.getElementById("live-pr-body").innerHTML = renderPrTable(prs);
}

async function ghGet(url) {
  const res = await fetch(url, { headers: GH_HEADERS });
  if (res.status === 403) {
    const reset = res.headers.get("x-ratelimit-reset");
    throw new Error(
      `GitHub rate limit — retry after ${reset ? new Date(Number(reset) * 1000).toLocaleTimeString() : "later"}`
    );
  }
  if (!res.ok) throw new Error(`GitHub API ${res.status}`);
  return res.json();
}

async function refreshSearch() {
  const statusEl = document.getElementById("live-status");
  try {
    const data = await ghGet(SEARCH_URL);
    prs = (data.items || []).map(mapSearchItem);
    paint();
    statusEl.textContent = `live · ${prs.length} open PRs · search every ${SEARCH_MS / 1000}s · CI ~${CI_TICK_MS / 1000}s/PR`;
  } catch (e) {
    statusEl.textContent = `live unavailable: ${e.message}`;
  }
}

function statusToCi(state) {
  if (state === "success") return "pass";
  if (state === "failure" || state === "error") return "fail";
  if (state === "pending") return "pending";
  return "none";
}

async function refreshOneCi() {
  if (!prs.length) return;
  const p = prs[ciIndex % prs.length];
  ciIndex += 1;
  if (p.draft) {
    ciCache.set(p._key, { ci: "draft", ready: false });
    const row = prs.find((x) => x._key === p._key);
    if (row) {
      row.ci = "draft";
      row.ready = false;
    }
    paint();
    return;
  }
  try {
    const pull = await ghGet(`https://api.github.com/repos/${ORG}/${p.repo}/pulls/${p.number}`);
    const sha = pull.head?.sha;
    if (!sha) return;
    const status = await ghGet(
      `https://api.github.com/repos/${ORG}/${p.repo}/commits/${sha}/status`
    );
    const ci = statusToCi(status.state);
    const ready = ci === "pass";
    ciCache.set(p._key, { ci, ready });
    const row = prs.find((x) => x._key === p._key);
    if (row) {
      row.ci = ci;
      row.ready = ready;
    }
    paint();
  } catch {
    /* rate limit or network */
  }
}

loadEcosystemSnapshot().then(refreshEcosystemLive);
setInterval(refreshEcosystemLive, ECO_MS);
refreshSearch();
setInterval(refreshSearch, SEARCH_MS);
setInterval(refreshOneCi, CI_TICK_MS);
