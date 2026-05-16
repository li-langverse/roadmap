/** Live PR merge queue — fetches directly from GitHub REST API (no server-side cron). */
const ORG = "li-langverse";
const REPOS = [
  "lic", "li-language", "lip", "lit", "lis", "benchmarks",
  "roadmap", "li-net", "li-httpd", "li-std-core", "li-std-math", "li-demo",
];
const POLL_MS = 5 * 60_000;
const LIVE_DOCS = {
  benchmarks: "https://li-langverse.github.io/benchmarks/",
  "li-language": "https://li-langverse.github.io/li-language/",
};

function ciClass(ci) {
  return `ci-${ci === "pass" ? "pass" : ci === "fail" ? "fail" : ci === "pending" ? "pending" : "none"}`;
}

function esc(s) {
  const el = document.createElement("span");
  el.textContent = s;
  return el.innerHTML;
}

function classifyCi(statuses) {
  if (!statuses || statuses.length === 0) return "none";
  let hasFail = false, hasPending = false;
  for (const s of statuses) {
    const state = (s.state || s.status || "").toLowerCase();
    const conclusion = (s.conclusion || "").toLowerCase();
    if (state === "success" || conclusion === "success" || conclusion === "skipped" || conclusion === "neutral") continue;
    if (state === "failure" || state === "error" || conclusion === "failure" || conclusion === "cancelled" || conclusion === "timed_out") { hasFail = true; continue; }
    hasPending = true;
  }
  if (hasFail) return "fail";
  if (hasPending) return "pending";
  return "pass";
}

async function ghFetch(url) {
  const res = await fetch(url, {
    headers: { Accept: "application/vnd.github+json" },
  });
  if (res.status === 403 && res.headers.get("x-ratelimit-remaining") === "0") {
    const reset = Number(res.headers.get("x-ratelimit-reset") || 0);
    const wait = reset ? new Date(reset * 1000).toLocaleTimeString() : "soon";
    throw new Error(`GitHub API rate limit exceeded — resets at ${wait}`);
  }
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${url}`);
  return res.json();
}

async function fetchRepoPRs(repo) {
  const prs = await ghFetch(
    `https://api.github.com/repos/${ORG}/${repo}/pulls?state=open&per_page=50`
  );
  const results = [];
  for (const pr of prs) {
    let ci = "none";
    try {
      const combined = await ghFetch(
        `https://api.github.com/repos/${ORG}/${repo}/commits/${pr.head.sha}/status`
      );
      const checks = await ghFetch(
        `https://api.github.com/repos/${ORG}/${repo}/commits/${pr.head.sha}/check-runs?per_page=50`
      );
      const allStatuses = [
        ...(combined.statuses || []),
        ...(checks.check_runs || []).map((cr) => ({
          state: cr.status === "completed" ? cr.conclusion : "pending",
          conclusion: cr.conclusion || "",
        })),
      ];
      ci = classifyCi(allStatuses);
    } catch { /* rate limit or error — leave as none */ }

    results.push({
      repo,
      number: pr.number,
      title: pr.title,
      url: pr.html_url,
      base: pr.base.ref,
      ci,
      draft: pr.draft,
      ready: ci === "pass" && !pr.draft,
    });
  }
  return results;
}

function renderMetrics(metrics) {
  const cards = [
    ["Ready to merge (CI green)", metrics.ready_to_merge],
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
  const sorted = [...prs].sort(
    (a, b) => Number(b.ready) - Number(a.ready) || a.repo.localeCompare(b.repo) || a.number - b.number
  );
  return sorted
    .map((p) => {
      const title = p.title.length > 72 ? `${p.title.slice(0, 69)}…` : p.title;
      return `<tr>
        <td>${esc(p.repo)}</td>
        <td><a href="${esc(p.url)}">#${p.number}</a></td>
        <td><a href="${esc(p.url)}">${esc(title)}</a>${p.draft ? ' <em>(draft)</em>' : ''}</td>
        <td class="mono">${esc(p.base)}</td>
        <td class="${ciClass(p.ci)}">${esc(p.ci)}</td>
        <td>${p.ready ? "✓ yes" : "—"}</td>
      </tr>`;
    })
    .join("");
}

let lastData = null;

async function refresh() {
  const statusEl = document.getElementById("live-status");
  statusEl.textContent = "fetching from GitHub API…";

  try {
    const allPRs = [];
    const batchSize = 3;
    for (let i = 0; i < REPOS.length; i += batchSize) {
      const batch = REPOS.slice(i, i + batchSize);
      const results = await Promise.all(batch.map(fetchRepoPRs));
      for (const prs of results) allPRs.push(...prs);
    }

    const docsCount = Object.keys(LIVE_DOCS).length;

    const data = {
      generated_at: new Date().toISOString(),
      metrics: {
        ready_to_merge: allPRs.filter((p) => p.ready).length,
        open_prs: allPRs.length,
        blocked: allPRs.filter((p) => !p.ready).length,
        repos_with_live_docs: docsCount,
        repos_total: REPOS.length,
      },
      pull_requests: allPRs,
    };

    lastData = data;
    document.getElementById("live-metrics").innerHTML = renderMetrics(data.metrics);
    document.getElementById("live-pr-body").innerHTML = renderPrTable(data.pull_requests);
    statusEl.textContent = `live · ${new Date().toLocaleTimeString()} · refreshes every ${POLL_MS / 60_000} min · ${data.metrics.open_prs} PRs across ${REPOS.length} repos`;
  } catch (e) {
    if (lastData) {
      statusEl.textContent = `showing cached data · ${e.message}`;
    } else {
      statusEl.textContent = `unavailable: ${e.message}`;
    }
  }
}

refresh();
setInterval(refresh, POLL_MS);
