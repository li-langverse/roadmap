/**
 * Live PR merge queue via GitHub public API (browser only — no Actions cron).
 * Search API: 10 req/min. Core API (commit status): 60 req/hr — one PR per 90s.
 */
const ORG = "li-langverse";
const SEARCH_MS = 120_000;
const CI_TICK_MS = 90_000;
const SEARCH_URL = `https://api.github.com/search/issues?q=org:${ORG}+is:open+is:pr&per_page=100&sort=updated`;

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

refreshSearch();
setInterval(refreshSearch, SEARCH_MS);
setInterval(refreshOneCi, CI_TICK_MS);
