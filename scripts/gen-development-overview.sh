#!/usr/bin/env bash
# Generate static HTML for GitHub Pages from docs/development-overview.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/docs/development-overview.md"
ECO_JSON="${ROOT}/data/development-overview/ecosystem-stats.json"
OUT_DIR="${ROOT}/site/development-overview"
OUT_HTML="${OUT_DIR}/index.html"
AS_OF="$(grep -m1 'scanned \*\*' "$SRC" | sed -n 's/.*scanned \*\*\([^*]*\)\*\*.*/\1/p' || date -u +%Y-%m-%dT%H:%MZ)"

mkdir -p "$OUT_DIR" "${ROOT}/site"

# Pages root (site/ is gitignored; generated on each Pages build)
cat >"${ROOT}/site/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Li roadmap</title>
  <meta http-equiv="refresh" content="0; url=./development-overview/">
  <link rel="canonical" href="https://li-langverse.github.io/roadmap/development-overview/">
</head>
<body>
  <p>Redirecting to <a href="./development-overview/">development overview</a>…</p>
</body>
</html>
HTML

PY="${PYTHON:-python3}"
if ! "$PY" -c "import markdown" 2>/dev/null; then
  VENV="${ROOT}/.venv-overview"
  if [[ ! -x "${VENV}/bin/python" ]]; then
    if "$PY" -m venv "$VENV" 2>/dev/null; then
      "${VENV}/bin/pip" install -q markdown
    fi
  fi
  if [[ -x "${VENV}/bin/python" ]] && "${VENV}/bin/python" -c "import markdown" 2>/dev/null; then
    PY="${VENV}/bin/python"
  elif command -v node >/dev/null 2>&1 || [[ -x "${HOME}/.local/node/bin/node" ]]; then
    export PATH="${HOME}/.local/node/bin:${PATH}"
    chmod +x "${ROOT}/scripts/gen-development-overview-node.mjs"
    exec node "${ROOT}/scripts/gen-development-overview-node.mjs"
  else
    echo "error: need python markdown or node+npx marked" >&2
    exit 1
  fi
fi

"$PY" - "$SRC" "$OUT_HTML" "$AS_OF" "$ECO_JSON" <<'PY'
import json
import re
import sys
from pathlib import Path

src_path, out_path, as_of, eco_path = sys.argv[1:5]
text = Path(src_path).read_text(encoding="utf-8")

try:
    import markdown
except ImportError:
    sys.stderr.write(
        "error: Python package 'markdown' required\n"
        "  pip install markdown   # or: python3 -m pip install markdown\n"
    )
    sys.exit(1)

body = markdown.markdown(
    text,
    extensions=["tables", "fenced_code", "sane_lists", "toc"],
    output_format="html5",
)

body = re.sub(r"^<h1[^>]*>.*?</h1>\s*", "", body, count=1, flags=re.DOTALL)

eco = {}
eco_file = Path(eco_path)
if eco_file.is_file():
    try:
        eco = json.loads(eco_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        pass

def fmt_int(n) -> str:
    if n is None:
        return "—"
    return f"{int(n):,}"


eco_as_of = eco.get("generated_at", "—")
repos_loc_tracked = eco.get("repos_loc_tracked") or eco.get("repos_tracked") or eco.get("gitlab_projects") or "—"
loc_file_types = ", ".join(eco.get("loc_file_types") or [".li"])
gitlab_projects = eco.get("gitlab_projects", "—")
def org_repos_val(e):
    v = e.get("org_repositories")
    if v is not None:
        return v
    return e.get("packages")


def cumulative_closed_prs(e):
  gh = e.get("github_prs_closed")
  if isinstance(gh, int):
    return gh
  prs = e.get("prs_closed")
  if isinstance(prs, int):
    return prs
  return e.get("mrs_closed")


def cumulative_closed_issues(e):
  gh = e.get("github_issues_closed")
  gl = e.get("issues_closed_gitlab")
  if gl is None:
    gl = e.get("issues_closed")
  if isinstance(gh, int) and isinstance(gl, int):
    return max(gh, gl)
  if isinstance(gl, int):
    return gl
  return gh


eco_cards = [
    ("Lines of Li", fmt_int(eco.get("lines_of_li") or eco.get("lines_of_code"))),
    ("Org repositories", fmt_int(org_repos_val(eco))),
    ("Open issues", fmt_int(eco.get("issues_open"))),
    ("Closed issues", fmt_int(cumulative_closed_issues(eco))),
    ("Closed PRs", fmt_int(cumulative_closed_prs(eco))),
]
eco_cards_html = "".join(
    f'<div class="metric-card"><p class="label">{label}</p><p class="value">{value}</p></div>'
    for label, value in eco_cards
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Li development overview — li-langverse</title>
  <meta name="description" content="PR merge queue, branch CI coverage, live docs, and benchmarks across the Li org." />
  <style>
    :root {{
      --bg: #0d1117;
      --fg: #e6edf3;
      --muted: #8b949e;
      --border: #30363d;
      --accent: #58a6ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.55;
    }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    header {{ margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }}
    header h1 {{ margin: 0 0 0.35rem; font-size: 1.75rem; }}
    header p {{ margin: 0; color: var(--muted); font-size: 0.9rem; }}
    a {{ color: var(--accent); }}
    h2 {{ margin-top: 2.25rem; font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; }}
    h3 {{ margin-top: 1.5rem; font-size: 1.05rem; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      margin: 1rem 0;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.45rem 0.6rem;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: #161b22; }}
    tr:nth-child(even) td {{ background: #161b22; }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
    em {{ color: var(--muted); font-size: 0.85rem; }}
    ul {{ padding-left: 1.25rem; }}
    li {{ margin: 0.35rem 0; }}
    .nav {{ margin-top: 0.75rem; font-size: 0.85rem; }}
    .nav a {{ margin-right: 1rem; }}
    .live-banner {{
      margin: 1rem 0 1.5rem;
      padding: 0.75rem 1rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #161b22;
      font-size: 0.88rem;
    }}
    .live-metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 0.75rem;
      margin: 1rem 0;
    }}
    .metric-card {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0;
      background: #0d1117;
      min-width: 0;
    }}
    .metric-card-link {{
      display: block;
      padding: 0.65rem 0.75rem;
      color: inherit;
      text-decoration: none;
      border-radius: 6px;
    }}
    .metric-card-link:hover {{
      border: 1px solid var(--accent);
      margin: -1px;
      background: #161b22;
    }}
    .metric-card .label {{ color: var(--muted); font-size: 0.78rem; margin: 0; }}
    .metric-card .value {{ font-size: 1.35rem; font-weight: 600; margin: 0.15rem 0 0; }}
    .metric-card .hint {{ color: var(--muted); font-size: 0.72rem; margin: 0.2rem 0 0; }}
    .ci-pass {{ color: #3fb950; }}
    .ci-fail {{ color: #f85149; }}
    .ci-pending {{ color: #d29922; }}
    .ci-none {{ color: var(--muted); }}
    .freshness-banner {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.35rem 0.5rem;
      margin: 0.5rem 0 0;
      padding: 0.55rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #161b22;
      font-size: 0.82rem;
      color: var(--muted);
    }}
    .freshness-banner strong {{ color: var(--fg); font-weight: 500; }}
    .live-status-badge {{
      color: var(--accent);
      font-size: 0.82rem;
    }}
    .live-status-badge:empty {{ display: none; }}
    .page-toc {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem 1rem;
      margin-top: 0.75rem;
      font-size: 0.85rem;
    }}
    .section-note {{ color: var(--muted); font-size: 0.85rem; margin: 0 0 0.75rem; }}
    .live-table-wrap {{ overflow-x: auto; }}
    .snapshot-details {{
      margin-top: 2rem;
      border: 1px dashed var(--border);
      border-radius: 6px;
      padding: 0.5rem 0.75rem 1rem;
      background: #161b22;
    }}
    .snapshot-details summary {{
      cursor: pointer;
      color: var(--fg);
      font-weight: 500;
      padding: 0.35rem 0;
    }}
    .snapshot-details .snapshot-body {{ margin-top: 0.75rem; }}
    .history-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }}
    @media (max-width: 720px) {{
      .history-grid {{ grid-template-columns: 1fr; }}
    }}
    .history-chart {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.65rem 0.75rem 0.5rem;
      background: #0d1117;
      min-width: 0;
    }}
    .history-chart-head {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 0.5rem;
      margin-bottom: 0.35rem;
    }}
    .history-chart h3 {{ margin: 0; font-size: 0.82rem; color: var(--muted); font-weight: 500; }}
    .history-latest {{ font-size: 0.95rem; font-weight: 600; font-variant-numeric: tabular-nums; }}
    .history-canvas-wrap {{ position: relative; height: 140px; }}
    .history-empty {{ margin: 0.5rem 0 0; color: var(--muted); font-size: 0.82rem; }}
    .history-meta {{ font-size: 0.78rem; color: var(--muted); margin: 0.5rem 0 0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Li development overview</h1>
      <p class="section-note">li-langverse org — live sections poll the public GitHub API from your browser.</p>
      <div class="freshness-banner" id="freshness-banner" aria-live="polite">
        <span><strong>Markdown snapshot</strong> <time id="snapshot-as-of">{as_of}</time></span>
        <span aria-hidden="true">·</span>
        <span id="freshness-pr">Loading PR queue…</span>
        <span aria-hidden="true">·</span>
        <span id="freshness-eco">Loading ecosystem counts…</span>
        <span aria-hidden="true">·</span>
        <a href="https://github.com/li-langverse/roadmap/blob/main/docs/development-overview.md">edit snapshot</a>
      </div>
      <nav class="page-toc" aria-label="On this page">
        <a href="#eco-heading">Ecosystem</a>
        <a href="#history-heading">History</a>
        <a href="#live-heading">PR queue</a>
        <a href="#markdown-snapshot">Snapshot tables</a>
      </nav>
      <nav class="nav" aria-label="Related">
        <a href="https://li-langverse.github.io/benchmarks/">Benchmarks</a>
        <a href="https://li-langverse.github.io/li-language/">Language docs</a>
        <a href="https://github.com/li-langverse/roadmap">roadmap repo</a>
      </nav>
    </header>
    <section class="live-banner" aria-labelledby="eco-heading">
      <h2 id="eco-heading">Ecosystem statistics</h2>
      <p class="section-note">
        Committed baseline <span id="eco-as-of">{eco_as_of}</span>.
        Issue and MR counts from <a href="https://gitlab.lilangverse.xyz/li-langverse">GitLab</a> snapshot (15m refresh); MR queue from <code>status.json</code> (~15m); <strong>Lines of Li</strong> weekly ({loc_file_types} across {repos_loc_tracked} org repos) — <span id="eco-live-status" class="live-status-badge"></span>
        <a href="https://github.com/li-langverse/roadmap/blob/main/scripts/compute-ecosystem-stats.py" title="Counts physical lines in .li source files across all GitHub/GitLab org repositories; excludes C++, Python harness, docs, and other languages.">Li source scope</a>
        · <a href="https://github.com/li-langverse/roadmap/blob/main/scripts/compute-ecosystem-stats.py">Maintainer: recompute snapshot</a>
      </p>
      <div class="live-metrics" id="ecosystem-metrics">{eco_cards_html}</div>
    </section>

    <section class="live-banner" aria-labelledby="history-heading">
      <h2 id="history-heading">Org activity history</h2>
      <p>Issue and MR trends from GitLab snapshots (<code>refresh-development-overview.sh</code>) plus live status points in your browser. One point per calendar day (UTC). Hover charts for values.</p>
      <div class="history-grid" id="history-charts"></div>
      <p id="history-status" class="history-meta"></p>
    </section>
    <section class="live-banner" aria-labelledby="live-heading">
      <h2 id="live-heading">Live merge queue</h2>
      <p class="section-note">GitLab-primary: polls committed <code>status.json</code> (~15m, refreshed every 15m on main). GitHub mirror fallback uses Search API when GitLab snapshot is unavailable. Older tables are in <a href="#markdown-snapshot">snapshot tables</a>.</p>
      <div class="live-metrics" id="live-metrics"></div>
      <div class="live-table-wrap">
        <table id="live-pr-table">
          <thead>
            <tr><th>Repo</th><th>#</th><th>Title</th><th>Base</th><th>CI</th><th>Ready</th></tr>
          </thead>
          <tbody id="live-pr-body"></tbody>
        </table>
      </div>
    </section>
    <main>
      <details id="markdown-snapshot" class="snapshot-details" open>
        <summary>Markdown snapshot tables (<time id="snapshot-as-of-summary">{as_of}</time>)</summary>
        <div class="snapshot-body">
{body}
        </div>
      </details>
    </main>
  </div>
  <script src="./history.js" defer></script>
  <script src="./live.js" defer></script>
</body>
</html>
"""

Path(out_path).write_text(html, encoding="utf-8")
print(f"Wrote {out_path}")
PY

cp "$SRC" "$OUT_DIR/overview.md"
cp "${ROOT}/scripts/development-overview-live.js" "$OUT_DIR/live.js"
cp "${ROOT}/scripts/development-overview-history.js" "$OUT_DIR/history.js"
HIST_JSON="${ROOT}/data/development-overview/history.json"
if [[ -f "$HIST_JSON" ]]; then
  cp "$HIST_JSON" "$OUT_DIR/history.json"
fi
if [[ -f "$ECO_JSON" ]]; then
  cp "$ECO_JSON" "$OUT_DIR/ecosystem-stats.json"
fi
STATUS_JSON="${ROOT}/data/development-overview/status.json"
if [[ -f "$STATUS_JSON" ]]; then
  cp "$STATUS_JSON" "$OUT_DIR/status.json"
fi
echo "Generated ${OUT_HTML}"
