/**
 * Live PR merge queue via GitHub public API (browser only — no Actions cron).
 * Search API: 10 req/min unauthenticated. Requests are staggered with retry/backoff.
 */
const ORG = "li-langverse";
const SEARCH_MS = 120_000;
const ECO_MS = 600_000;
const CI_TICK_MS = 90_000;
const SEARCH_GAP_MS = 7_000;
const ECO_CACHE_MS = 600_000;
const ECO_CACHE_KEY = "li-dev-overview-eco-live-v1";
const SEARCH_URL = `https://api.github.com/search/issues?q=org:${ORG}+is:open+is:pr&per_page=100&sort=updated`;
const ECO_STATS_URL = "./ecosystem-stats.json";

/** @type {{ lines_of_code?: number, org_repositories?: number, packages?: number, issues_open?: number, issues_closed?: number, prs_closed?: number, generated_at?: string }} */
let ecosystemSnapshot = {};

/** @type {Map<string, { ci: string, ready: boolean }>} */
const ciCache = new Map();
let prs = [];
let ciIndex = 0;

const GH_HEADERS = { Accept: "application/vnd.github+json" };

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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

function orgReposFromSnapshot(snap) {
  if (snap.org_repositories != null) return snap.org_repositories;
  if (snap.packages != null) return snap.packages;
  return undefined;
}

function readEcoCache() {
  try {
    const raw = sessionStorage.getItem(ECO_CACHE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed?.fetchedAt || Date.now() - parsed.fetchedAt > ECO_CACHE_MS) return null;
    return parsed.data || null;
  } catch {
    return null;
  }
}

function writeEcoCache(data) {
  try {
    sessionStorage.setItem(
      ECO_CACHE_KEY,
      JSON.stringify({ fetchedAt: Date.now(), data })
    );
  } catch {
    /* quota / private mode */
  }
}

function renderEcosystemMetrics(live = {}) {
  const loc = live.lines_of_code ?? ecosystemSnapshot.lines_of_code;
  const orgRepos = live.org_repositories ?? orgReposFromSnapshot(ecosystemSnapshot);
  const issues = live.issues_open ?? ecosystemSnapshot.issues_open;
  const closedIssues = live.issues_closed ?? ecosystemSnapshot.issues_closed;
  const closedPrs = live.prs_closed ?? ecosystemSnapshot.prs_closed;
  const asOf = live.generated_at ?? ecosystemSnapshot.generated_at;
  const asOfEl = document.getElementById("eco-as-of");
  if (asOfEl && asOf) asOfEl.textContent = asOf;

  const statusEl = document.getElementById("eco-live-status");
  if (statusEl) {
    statusEl.textContent = live._status || "";
  }

  return [
    ["Lines of code", fmtNum(loc)],
    ["Org repositories", fmtNum(orgRepos)],
    ["Open issues", fmtNum(issues)],
    ["Closed issues", fmtNum(closedIssues)],
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

async function ghGet(url, attempt = 0) {
  const res = await fetch(url, { headers: GH_HEADERS });
  if ((res.status === 403 || res.status === 429) && attempt < 3) {
    const reset = res.headers.get("x-ratelimit-reset");
    const retryAfter = res.headers.get("retry-after");
    let waitMs = 60_000;
    if (reset) {
      waitMs = Math.max(5_000, Number(reset) * 1000 - Date.now() + 1_000);
    } else if (retryAfter) {
      waitMs = Math.max(5_000, Number(retryAfter) * 1000);
    }
    waitMs = Math.min(waitMs, 900_000);
    await sleep(waitMs);
    return ghGet(url, attempt + 1);
  }
  if (res.status === 403 || res.status === 429) {
    const reset = res.headers.get("x-ratelimit-reset");
    throw new Error(
      `GitHub rate limit — retry after ${reset ? new Date(Number(reset) * 1000).toLocaleTimeString() : "later"}`
    );
  }
  if (!res.ok) throw new Error(`GitHub API ${res.status}`);
  return res.json();
}

async function fetchOrgRepositoryCount() {
  try {
    let total = 0;
    for (let page = 1; page <= 10; page += 1) {
      const repos = await ghGet(
        `https://api.github.com/orgs/${ORG}/repos?per_page=100&page=${page}`
      );
      if (!Array.isArray(repos) || !repos.length) break;
      total += repos.length;
      if (repos.length < 100) break;
      await sleep(SEARCH_GAP_MS);
    }
    return total || null;
  } catch {
    return null;
  }
}

async function searchCount(query) {
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=1`;
  const data = await ghGet(url);
  return typeof data.total_count === "number" ? data.total_count : null;
}

async function searchCountsSequential(queries) {
  /** @type {Record<string, number | null>} */
  const out = {};
  const errors = [];
  for (const [key, query] of queries) {
    try {
      out[key] = await searchCount(query);
    } catch (err) {
      out[key] = null;
      errors.push(err instanceof Error ? err.message : String(err));
    }
    await sleep(SEARCH_GAP_MS);
  }
  return { out, errors };
}

async function loadEcosystemSnapshot() {
  try {
    const res = await fetch(ECO_STATS_URL, { cache: "no-store" });
    if (res.ok) ecosystemSnapshot = await res.json();
  } catch {
    /* static HTML fallback */
  }
  const cached = readEcoCache();
  if (cached) {
    paintEcosystem({ ...cached, _status: "cached · GitHub refresh soon" });
  } else {
    paintEcosystem();
  }
}

async function refreshEcosystemLive(force = false) {
  if (!force) {
    const cached = readEcoCache();
    if (cached) {
      paintEcosystem({ ...cached, _status: "cached · next GitHub refresh soon" });
      const at = cached.generated_at || new Date().toISOString().slice(0, 10);
      window.DevelopmentOverviewHistory?.updateLive({
        at,
        source: "cached",
        ...(typeof cached.open_prs === "number" ? { open_prs: cached.open_prs } : {}),
        ...(typeof cached.prs_closed === "number" ? { prs_closed: cached.prs_closed } : {}),
        ...(typeof cached.issues_open === "number" ? { issues_open: cached.issues_open } : {}),
        ...(typeof cached.issues_closed === "number" ? { issues_closed: cached.issues_closed } : {}),
      });
      return;
    }
  }

  const at = new Date().toISOString().slice(0, 10);
  const { out, errors } = await searchCountsSequential([
    ["issues_open", `org:${ORG} is:issue is:open`],
    ["issues_closed", `org:${ORG} is:issue is:closed`],
    ["prs_closed", `org:${ORG} is:pr is:closed`],
    ["open_prs", `org:${ORG} is:pr is:open`],
  ]);

  const orgRepos = await fetchOrgRepositoryCount();

  const live = {
    issues_open: out.issues_open ?? undefined,
    issues_closed: out.issues_closed ?? undefined,
    prs_closed: out.prs_closed ?? undefined,
    open_prs: out.open_prs ?? undefined,
    org_repositories: orgRepos ?? undefined,
    generated_at: at,
  };

  const got = Object.entries(out).filter(([, v]) => typeof v === "number").length;
  let status = got ? `live · ${got}/4 GitHub counts` : "";
  if (errors.length) {
    status = `${status}${status ? " · " : ""}${errors[0]}`.trim();
  }

  paintEcosystem({ ...live, _status: status });

  const historyPoint = { at, source: got ? "live-api" : "partial-live" };
  if (typeof out.open_prs === "number") historyPoint.open_prs = out.open_prs;
  if (typeof out.prs_closed === "number") historyPoint.prs_closed = out.prs_closed;
  if (typeof out.issues_open === "number") historyPoint.issues_open = out.issues_open;
  if (typeof out.issues_closed === "number") historyPoint.issues_closed = out.issues_closed;
  if (Object.keys(historyPoint).length > 2) {
    window.DevelopmentOverviewHistory?.updateLive(historyPoint);
  }

  if (got > 0) {
    writeEcoCache({ ...live, open_prs: out.open_prs ?? undefined });
  }
}

function renderMetrics(list) {
  const open = openPrTotal || list.length;
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

async function searchAllIssues(query) {
  const items = [];
  for (let page = 1; page <= 10; page += 1) {
    const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=100&page=${page}&sort=updated`;
    const data = await ghGet(url);
    items.push(...(data.items || []));
    if (items.length >= (data.total_count || 0) || (data.items || []).length < 100) break;
    await sleep(SEARCH_GAP_MS);
  }
  return items;
}

let openPrTotal = 0;

async function refreshSearch() {
  const statusEl = document.getElementById("live-status");
  try {
    const data = await ghGet(SEARCH_URL);
    openPrTotal = typeof data.total_count === "number" ? data.total_count : (data.items || []).length;
    prs = (data.items || []).map(mapSearchItem);
    paint();
    statusEl.textContent = `live · ${openPrTotal} open PRs · search every ${SEARCH_MS / 1000}s · CI ~${CI_TICK_MS / 1000}s/PR`;
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

loadEcosystemSnapshot().then(() => refreshEcosystemLive(true));
setInterval(() => refreshEcosystemLive(true), ECO_MS);
refreshSearch();
setInterval(refreshSearch, SEARCH_MS);
setInterval(refreshOneCi, CI_TICK_MS);
