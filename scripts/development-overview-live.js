/**
 * Development overview — loads status.json (refreshed by GitHub Actions) and
 * optionally supplements the PR queue from the public Search API.
 */
const ORG = "li-langverse";
const STATUS_URL = "./status.json";
const STATUS_POLL_MS = 60_000;
const SEARCH_POLL_MS = 120_000;
const SEARCH_URL = `https://api.github.com/search/issues?q=org:${ORG}+is:open+is:pr&per_page=100&sort=updated`;

let status = null;

const GH_HEADERS = { Accept: "application/vnd.github+json" };

function esc(s) {
  const el = document.createElement("span");
  el.textContent = String(s ?? "");
  return el.innerHTML;
}

function ciClass(ci) {
  const key = String(ci || "none").toLowerCase();
  return `ci-${key === "pass" ? "pass" : key === "fail" ? "fail" : key === "pending" ? "pending" : "none"}`;
}

function fmtTime(iso) {
  if (!iso) return "\u2014";
  try {
    return new Date(iso).toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
}

function ageLabel(iso) {
  if (!iso) return "";
  const ms = Date.now() - new Date(iso).getTime();
  if (ms < 0) return "just now";
  const min = Math.floor(ms / 60_000);
  if (min < 2) return "just now";
  if (min < 60) return `${min}m ago`;
  const hr = Math.floor(min / 60);
  if (hr < 48) return `${hr}h ago`;
  return `${Math.floor(hr / 24)}d ago`;
}

function renderMetrics(m) {
  const cards = [
    ["Public repos", m.public_repos],
    ["Open PRs", m.open_prs],
    ["Ready to merge", m.ready_to_merge],
    ["Open issues", m.open_issues],
    ["CI failing PRs", m.blocked_prs],
    ["Repos with CI", m.repos_with_ci],
    ["Live doc sites", m.repos_with_live_docs],
  ];
  return cards
    .map(
      ([label, value]) =>
        `<div class="metric-card"><p class="label">${esc(label)}</p><p class="value">${esc(String(value))}</p></div>`
    )
    .join("");
}

function renderRepoTable(repos) {
  const sorted = [...repos].sort((a, b) => a.name.localeCompare(b.name));
  return sorted
    .map((r) => {
      const docs = r.live_docs
        ? `<a href="${esc(r.live_docs)}">live</a>`
        : `<span class="ci-none">\u2014</span>`;
      const ci = r.has_ci ? r.main_ci_last : "none";
      const wf = r.has_ci
        ? `${r.workflow_count} wf`
        : `<span class="ci-fail">missing</span>`;
      return `<tr>
        <td><a href="${esc(r.url)}">${esc(r.name)}</a></td>
        <td>${r.open_issues}</td>
        <td>${r.open_prs}</td>
        <td class="${ciClass(ci)}">${esc(ci)}</td>
        <td>${wf}</td>
        <td>${docs}</td>
        <td class="ci-none">${esc(fmtTime(r.updated_at))}</td>
      </tr>`;
    })
    .join("");
}

function renderPrTable(prs) {
  const sorted = [...prs].sort(
    (a, b) => Number(b.ready) - Number(a.ready) || a.repo.localeCompare(b.repo)
  );
  return sorted
    .map((p) => {
      const title = p.title.length > 72 ? `${p.title.slice(0, 69)}\u2026` : p.title;
      const draft = p.draft ? ` <span class="ci-none">(draft)</span>` : "";
      return `<tr>
        <td>${esc(p.repo)}</td>
        <td><a href="${esc(p.url)}">#${p.number}</a></td>
        <td><a href="${esc(p.url)}">${esc(title)}</a>${draft}</td>
        <td class="mono">${esc(p.base || "main")}</td>
        <td class="${ciClass(p.ci)}">${esc(p.ci)}</td>
        <td>${p.ready ? "yes" : "\u2014"}</td>
      </tr>`;
    })
    .join("");
}

function paint() {
  if (!status) return;
  const m = status.metrics;
  document.getElementById("live-metrics").innerHTML = renderMetrics(m);
  document.getElementById("live-repo-body").innerHTML = renderRepoTable(status.repos || []);
  document.getElementById("live-pr-body").innerHTML = renderPrTable(status.pull_requests || []);

  const asOf = document.getElementById("snapshot-as-of");
  if (asOf) asOf.textContent = status.generated_at || "\u2014";

  const statusEl = document.getElementById("live-status");
  if (statusEl) {
    const age = ageLabel(status.generated_at);
    const missing =
      m.missing_hint_repos?.length > 0
        ? ` \u00b7 ${m.missing_hint_repos.length} hint repo(s) not in org`
        : "";
    statusEl.textContent = `refreshed ${age}${missing} \u00b7 poll ${STATUS_POLL_MS / 1000}s`;
  }

  const hintEl = document.getElementById("repo-hint-note");
  if (hintEl && m.missing_hint_repos?.length) {
    hintEl.innerHTML = `<p class="hint-warn">Listed in <code>li-org-repos.txt</code> but not found in org: ${esc(m.missing_hint_repos.join(", "))}</p>`;
  }
}

async function loadStatus() {
  const statusEl = document.getElementById("live-status");
  try {
    const res = await fetch(`${STATUS_URL}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`status.json ${res.status}`);
    status = await res.json();
    paint();
  } catch (e) {
    if (statusEl) statusEl.textContent = `status.json unavailable: ${e.message}`;
  }
}

async function ghGet(url) {
  const res = await fetch(url, { headers: GH_HEADERS });
  if (!res.ok) throw new Error(`GitHub API ${res.status}`);
  return res.json();
}

async function refreshSearchOverlay() {
  if (!status) return;
  try {
    const data = await ghGet(SEARCH_URL);
    const total = data.total_count ?? 0;
    if (total > (status.pull_requests?.length || 0)) {
      const statusEl = document.getElementById("live-status");
      if (statusEl) {
        statusEl.textContent += ` \u00b7 Search API: ${total} open PRs total`;
      }
    }
  } catch {
    /* rate limit */
  }
}

loadStatus();
setInterval(loadStatus, STATUS_POLL_MS);
setInterval(refreshSearchOverlay, SEARCH_POLL_MS);
