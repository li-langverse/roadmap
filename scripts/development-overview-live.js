/**
 * Live PR merge queue via GitHub public API (browser only — no Actions cron).
 * Search API: 10 req/min unauthenticated. Requests are staggered with retry/backoff.
 */
const ORG = "li-langverse";
const GITLAB_HOST = "gitlab.lilangverse.xyz";
const GITLAB_GROUP = "li-langverse";
const GITLAB_ISSUES = (state) =>
  `https://${GITLAB_HOST}/groups/${GITLAB_GROUP}/-/issues?state=${state}&sort=created_date`;
const GITLAB_MRS = (state) =>
  `https://${GITLAB_HOST}/groups/${GITLAB_GROUP}/-/merge_requests?state=${state}`;
const SEARCH_MS = 120_000;
const STATUS_MS = 900_000;
const ECO_MS = 900_000;
const CI_TICK_MS = 90_000;
const SEARCH_GAP_MS = 2_000;
const ECO_CACHE_MS = 900_000;
const ECO_CACHE_KEY = "li-dev-overview-eco-live-v3";
const SEARCH_URL = `https://api.github.com/search/issues?q=org:${ORG}+is:open+is:pr&per_page=100&sort=updated`;
const ECO_STATS_URL = "./ecosystem-stats.json";
const STATUS_JSON_URL = "./status.json";

const GITHUB_SEARCH = (q) =>
  `https://github.com/search?q=${encodeURIComponent(q)}&type=issues`;

function gitlabPrimary(snap) {
  return (
    snap?.vcs_primary === "gitlab" ||
    snap?.issues_source === "gitlab" ||
    snap?.mrs_source === "gitlab"
  );
}

function metricLinks(snap) {
  const gl = gitlabPrimary(snap);
  return {
    "GitLab projects": `https://${GITLAB_HOST}/${GITLAB_GROUP}`,
    "Org repositories": gl
      ? `https://${GITLAB_HOST}/${GITLAB_GROUP}`
      : `https://github.com/orgs/${ORG}/repositories`,
    "Open issues": GITLAB_ISSUES("opened"),
    "Closed issues": GITLAB_ISSUES("closed"),
    "Open MRs": GITLAB_MRS("opened"),
    "Closed MRs": GITLAB_MRS("merged"),
    "Open PRs": gl ? GITLAB_MRS("opened") : GITHUB_SEARCH(`org:${ORG} is:pr is:open`),
    "Closed PRs": gl
      ? GITLAB_MRS("merged")
      : GITHUB_SEARCH(`org:${ORG} is:pr is:closed`),
    "Ready to merge": gl ? GITLAB_MRS("opened") : GITHUB_SEARCH(`org:${ORG} is:pr is:open`),
  };
}

/** @type {{ lines_of_code?: number, org_repositories?: number, packages?: number, issues_open?: number, issues_closed?: number, prs_closed?: number, generated_at?: string }} */
let ecosystemSnapshot = {};

/** Live issue/PR totals fetched in-browser (updated with PR queue refresh). */
let liveEcoCounts = {};

/** @type {Map<string, { ci: string, ready: boolean }>} */
const ciCache = new Map();
let prs = [];
let ciIndex = 0;
let openPrTotal = 0;
let prQueueLive = false;
let vcsPrimary = "gitlab";
let statusSnapshot = {};

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

function setEcoStatus(text) {
  const badge = document.getElementById("eco-live-status");
  const banner = document.getElementById("freshness-eco");
  const value = text || "";
  if (badge) badge.textContent = value;
  if (banner) banner.textContent = value || "Ecosystem counts pending…";
}

function ciProgressText() {
  if (!prs.length) return "";
  const checked = prs.filter((p) => p.ci !== "…").length;
  return `CI ${checked}/${prs.length} checked`;
}

function updateFreshnessPr(extra = "") {
  const el = document.getElementById("freshness-pr");
  if (!el) return;
  if (!prQueueLive) {
    el.textContent = extra || "Loading PR queue…";
    return;
  }
  const parts = [`PR queue live · ${openPrTotal} open`];
  const ci = ciProgressText();
  if (ci) parts.push(ci);
  if (extra) parts.push(extra);
  el.textContent = parts.join(" · ");
}

function markLiveQueueReady() {
  const details = document.getElementById("markdown-snapshot");
  if (details && !details.dataset.liveReady) {
    details.dataset.liveReady = "1";
    details.open = false;
  }
}

function metricCard(label, value, href, hint = "") {
  const hintHtml = hint ? `<p class="hint">${esc(hint)}</p>` : "";
  const inner = `<p class="label">${esc(label)}</p><p class="value">${esc(value)}</p>${hintHtml}`;
  if (href) {
    return `<div class="metric-card"><a class="metric-card-link" href="${href.replace(/"/g, "&quot;")}" target="_blank" rel="noopener noreferrer">${inner}</a></div>`;
  }
  return `<div class="metric-card">${inner}</div>`;
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
  const merged = { ...liveEcoCounts, ...live };
  const snap = { ...ecosystemSnapshot, ...merged };
  const links = metricLinks(snap);
  const gl = gitlabPrimary(snap);
  vcsPrimary = gl ? "gitlab" : "github";
  const loc = snap.lines_of_code;
  const orgRepos =
    merged.gitlab_projects ??
    snap.gitlab_projects ??
    merged.org_repositories ??
    orgReposFromSnapshot(snap);
  const issues = merged.issues_open ?? snap.issues_open;
  const closedIssues = merged.issues_closed ?? snap.issues_closed;
  const openMrs = merged.mrs_open ?? snap.mrs_open ?? snap.prs_open;
  const closedMrs = merged.mrs_closed ?? snap.mrs_closed ?? snap.prs_closed;
  const locAsOf = snap.generated_at;
  const issuesAsOf = merged.issues_at ?? snap.generated_at;
  const asOfEl = document.getElementById("eco-as-of");
  if (asOfEl) {
    const parts = [];
    if (issuesAsOf) parts.push(`${gl ? "GitLab" : "snapshot"} ${issuesAsOf}`);
    if (locAsOf) parts.push(`LoC ${locAsOf}`);
    asOfEl.textContent = parts.length ? parts.join(" · ") : "—";
  }

  setEcoStatus(merged._status || "");

  const locHint =
    loc != null && locAsOf ? `snapshot ${locAsOf}` : "recomputed weekly on main";
  const repoLabel = gl ? "GitLab projects" : "Org repositories";
  const openQueueLabel = gl ? "Open MRs" : "Open PRs";
  const closedQueueLabel = gl ? "Closed MRs" : "Closed PRs";

  return [
    ["Lines of code", fmtNum(loc), null, locHint],
    [repoLabel, fmtNum(orgRepos), links[repoLabel]],
    ["Open issues", fmtNum(issues), links["Open issues"], gl ? "GitLab group" : ""],
    ["Closed issues", fmtNum(closedIssues), links["Closed issues"], gl ? "GitLab group" : ""],
    [openQueueLabel, fmtNum(openMrs), links[openQueueLabel]],
    [closedQueueLabel, fmtNum(closedMrs), links[closedQueueLabel]],
  ]
    .map(([label, value, href, hint]) => metricCard(label, value, href, hint))
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
    liveEcoCounts = { ...liveEcoCounts, ...cached };
    paintEcosystem({ _status: "cached · GitHub refresh soon" });
  } else {
    paintEcosystem({ _status: "loading GitHub counts…" });
  }
}

async function refreshIssueCounts() {
  try {
    const res = await fetch(ECO_STATS_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`snapshot ${res.status}`);
    const eco = await res.json();
    ecosystemSnapshot = { ...ecosystemSnapshot, ...eco };
    const at = eco.generated_at || new Date().toISOString().slice(0, 16);
    const gl = gitlabPrimary(eco);
    liveEcoCounts = {
      ...liveEcoCounts,
      issues_open: eco.issues_open ?? undefined,
      issues_closed: eco.issues_closed ?? undefined,
      mrs_open: eco.mrs_open ?? eco.prs_open ?? undefined,
      mrs_closed: eco.mrs_closed ?? eco.prs_closed ?? undefined,
      gitlab_projects: eco.gitlab_projects ?? undefined,
      issues_at: at,
      generated_at: at,
    };
    const got =
      (typeof eco.issues_open === "number" ? 1 : 0) +
      (typeof eco.issues_closed === "number" ? 1 : 0) +
      (typeof eco.mrs_open === "number" ? 1 : 0);
    const status = got
      ? `GitLab snapshot · ${at}`
      : "GitLab counts unavailable (check GITLAB_TOKEN in refresh workflow)";
    paintEcosystem({ _status: gl ? status : `snapshot · ${at}` });
    if (got > 0) {
      writeEcoCache(liveEcoCounts);
      pushHistoryFromEco(liveEcoCounts, "snapshot");
    }
  } catch (e) {
    paintEcosystem({
      _status: `snapshot unavailable: ${e instanceof Error ? e.message : String(e)}`,
    });
  }
}

async function refreshEcosystemLive(force = false) {
  if (!force) {
    const cached = readEcoCache();
    if (cached) {
      liveEcoCounts = { ...liveEcoCounts, ...cached };
      paintEcosystem({ _status: "cached · next GitHub refresh soon" });
      pushHistoryFromEco(liveEcoCounts, "cached");
      return;
    }
  }

  await refreshIssueCounts();
  if (gitlabPrimary(ecosystemSnapshot)) {
    paintEcosystem({ _status: `GitLab · snapshot refresh every 15m` });
    writeEcoCache(liveEcoCounts);
    return;
  }

  setEcoStatus("refreshing GitHub counts…");
  const { out, errors } = await searchCountsSequential([
    ["prs_closed", `org:${ORG} is:pr is:closed`],
  ]);
  const orgRepos = await fetchOrgRepositoryCount();
  liveEcoCounts = {
    ...liveEcoCounts,
    prs_closed: out.prs_closed ?? undefined,
    org_repositories: orgRepos ?? undefined,
  };
  const got =
    (typeof liveEcoCounts.issues_open === "number" ? 1 : 0) +
    (typeof out.prs_closed === "number" ? 1 : 0);
  let status = got ? `live · GitHub fallback` : "live counts unavailable";
  if (errors.length) status = `${status} · ${errors[0]}`.trim();
  paintEcosystem({ _status: status });
  if (got > 0) writeEcoCache(liveEcoCounts);
}

function pushHistoryFromEco(data, source) {
  const at =
    (data.issues_at && data.issues_at.slice(0, 10)) ||
    data.generated_at ||
    new Date().toISOString().slice(0, 10);
  const historyPoint = { at, source };
  if (typeof data.open_prs === "number") historyPoint.open_prs = data.open_prs;
  if (typeof data.prs_closed === "number") historyPoint.prs_closed = data.prs_closed;
  if (typeof data.issues_open === "number") historyPoint.issues_open = data.issues_open;
  if (typeof data.issues_closed === "number") historyPoint.issues_closed = data.issues_closed;
  if (Object.keys(historyPoint).length > 2) {
    window.DevelopmentOverviewHistory?.updateLive(historyPoint);
  }
}

function renderMetrics(list) {
  const links = metricLinks(ecosystemSnapshot);
  const open = openPrTotal || list.length;
  const drafts = list.filter((p) => p.draft).length;
  const ready = list.filter((p) => p.ready).length;
  const blocked = list.filter((p) => !p.ready && !p.draft && p.ci === "fail").length;
  const pendingCi = list.filter((p) => !p.draft && (p.ci === "…" || p.ci === "pending")).length;
  const readyHint = ready === 0 && pendingCi > 0 ? "pending CI checks" : "";
  const openLabel = vcsPrimary === "gitlab" ? "Open MRs" : "Open PRs";

  return [
    ["Ready to merge", ready, links["Ready to merge"], readyHint],
    [openLabel, open, links[openLabel]],
    ["Drafts", drafts, null],
    ["CI failing", blocked, null],
  ]
    .map(([label, value, href, hint]) => metricCard(label, String(value), href, hint))
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
      const ciLabel = p.ci === "…" ? "loading" : p.ci;
      return `<tr>
        <td>${esc(p.repo)}</td>
        <td><a href="${esc(p.url)}">#${p.number}</a></td>
        <td><a href="${esc(p.url)}">${esc(title)}</a>${draft}</td>
        <td class="mono">${esc(p.base)}</td>
        <td class="${ciClass(p.ci)}" title="${p.ci === "…" ? "CI status not checked yet" : ""}">${esc(ciLabel)}</td>
        <td>${p.ready ? "yes" : "—"}</td>
      </tr>`;
    })
    .join("");
}

function paint() {
  document.getElementById("live-metrics").innerHTML = renderMetrics(prs);
  document.getElementById("live-pr-body").innerHTML = renderPrTable(prs);
  if (prQueueLive) updateFreshnessPr();
}

function mapStatusMr(row) {
  const key = prKey(row.repo, row.number);
  const cached = ciCache.get(key);
  return {
    repo: row.repo,
    number: row.number,
    title: row.title,
    url: row.url,
    base: row.base || "main",
    draft: Boolean(row.draft),
    ci: cached?.ci ?? row.ci ?? "…",
    ready: cached?.ready ?? Boolean(row.ready),
    _key: key,
  };
}

async function refreshFromStatusJson() {
  try {
    const res = await fetch(STATUS_JSON_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`status.json ${res.status}`);
    statusSnapshot = await res.json();
    vcsPrimary = statusSnapshot.vcs_source || vcsPrimary;
    const rows =
      statusSnapshot.merge_requests?.length
        ? statusSnapshot.merge_requests
        : statusSnapshot.pull_requests || [];
    openPrTotal = statusSnapshot.metrics?.open_prs ?? rows.length;
    prs = rows.map(mapStatusMr);
    prQueueLive = true;
    paint();
    markLiveQueueReady();
    const gen = statusSnapshot.generated_at || "";
    updateFreshnessPr(`GitLab MR queue · status.json ${gen} · refresh ${STATUS_MS / 1000}s`);
    const at = (gen || new Date().toISOString()).slice(0, 10);
    window.DevelopmentOverviewHistory?.updateLive({
      at,
      source: "status-json",
      open_prs: openPrTotal,
      open_mrs: openPrTotal,
      ready_to_merge: prs.filter((p) => p.ready).length,
    });
    refreshIssueCounts().catch(() => {});
    return true;
  } catch (e) {
    return false;
  }
}

async function refreshSearch() {
  if (gitlabPrimary(ecosystemSnapshot)) {
    const ok = await refreshFromStatusJson();
    if (ok) return;
  }
  try {
    const data = await ghGet(SEARCH_URL);
    openPrTotal = typeof data.total_count === "number" ? data.total_count : (data.items || []).length;
    prs = (data.items || []).map(mapSearchItem);
    vcsPrimary = "github";
    prQueueLive = true;
    paint();
    markLiveQueueReady();
    updateFreshnessPr(`GitHub PR queue · search every ${SEARCH_MS / 1000}s`);
    const at = new Date().toISOString().slice(0, 10);
    window.DevelopmentOverviewHistory?.updateLive({
      at,
      source: "live-api",
      open_prs: openPrTotal,
      ready_to_merge: prs.filter((p) => p.ready).length,
    });
    setTimeout(() => refreshIssueCounts().catch(() => {}), SEARCH_GAP_MS);
  } catch (e) {
    prQueueLive = false;
    updateFreshnessPr(`unavailable: ${e.message}`);
  }
}

function statusToCi(state) {
  if (state === "success") return "pass";
  if (state === "failure" || state === "error") return "fail";
  if (state === "pending") return "pending";
  return "none";
}

async function refreshOneCi() {
  if (vcsPrimary === "gitlab" || !prs.length) return;
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

loadEcosystemSnapshot().then(async () => {
  await refreshEcosystemLive(true);
  await refreshSearch();
});
setInterval(() => refreshEcosystemLive(true), ECO_MS);
setInterval(refreshSearch, STATUS_MS);
setInterval(refreshOneCi, CI_TICK_MS);
