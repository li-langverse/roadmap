#!/usr/bin/env bash
# Generate static HTML for GitHub Pages from docs/development-overview.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/docs/development-overview.md"
ECO_JSON="${ROOT}/data/development-overview/ecosystem-stats.json"
OUT_DIR="${ROOT}/site/development-overview"
OUT_HTML="${OUT_DIR}/index.html"
AS_OF="$(grep -m1 'scanned \*\*' "$SRC" | sed -n 's/.*scanned \*\*\([^*]*\)\*\*.*/\1/p' || date -u +%Y-%m-%dT%H:%MZ)"

mkdir -p "$OUT_DIR"

PY="${PYTHON:-python3}"
if ! "$PY" -c "import markdown" 2>/dev/null; then
  VENV="${ROOT}/.venv-overview"
  if [[ ! -x "${VENV}/bin/python" ]]; then
    "$PY" -m venv "$VENV"
    "${VENV}/bin/pip" install -q markdown
  fi
  PY="${VENV}/bin/python"
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
def org_repos_val(e):
    v = e.get("org_repositories")
    if v is not None:
        return v
    return e.get("packages")

eco_cards = [
    ("Lines of code", fmt_int(eco.get("lines_of_code"))),
    ("Org repositories", fmt_int(org_repos_val(eco))),
    ("Open issues", fmt_int(eco.get("issues_open"))),
    ("Closed PRs", fmt_int(eco.get("prs_closed"))),
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
      padding: 0.65rem 0.75rem;
      background: #0d1117;
    }}
    .metric-card .label {{ color: var(--muted); font-size: 0.78rem; margin: 0; }}
    .metric-card .value {{ font-size: 1.35rem; font-weight: 600; margin: 0.15rem 0 0; }}
    .ci-pass {{ color: #3fb950; }}
    .ci-fail {{ color: #f85149; }}
    .ci-pending {{ color: #d29922; }}
    .ci-none {{ color: var(--muted); }}
    #live-status {{ color: var(--muted); font-size: 0.82rem; }}
    .live-table-wrap {{ overflow-x: auto; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Li development overview</h1>
      <p>li-langverse org · snapshot <span id="snapshot-as-of">{as_of}</span> · <span id="live-status">loading live queue…</span> · <a href="https://github.com/li-langverse/roadmap/blob/main/docs/development-overview.md">edit snapshot</a></p>
      <nav class="nav" aria-label="Related">
        <a href="https://li-langverse.github.io/benchmarks/">Benchmarks</a>
        <a href="https://li-langverse.github.io/li-language/">Language docs</a>
        <a href="https://github.com/li-langverse/roadmap">roadmap repo</a>
      </nav>
    </header>
    <section class="live-banner" aria-labelledby="eco-heading">
      <h2 id="eco-heading">Ecosystem statistics</h2>
      <p>Snapshot <span id="eco-as-of">{eco_as_of}</span> · <strong>Org repositories</strong> = every repo under li-langverse on GitHub (LoC still sums <code>.github/li-org-repos.txt</code> only). Live open issues &amp; closed PRs refresh in the browser · <a href="https://github.com/li-langverse/roadmap/blob/main/scripts/compute-ecosystem-stats.py">recompute stats</a></p>
      <div class="live-metrics" id="ecosystem-metrics">{eco_cards_html}</div>
    </section>
    <section class="live-banner" aria-labelledby="live-heading">
      <h2 id="live-heading">Live PR merge queue</h2>
      <p>Live queue: embedded JavaScript calls the <a href="https://docs.github.com/en/rest/search">GitHub API</a> from your browser (no Actions cron). CI status fills in gradually (~90s per PR). Tables below are the markdown snapshot.</p>
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
{body}
    </main>
  </div>
  <script src="./live.js" defer></script>
</body>
</html>
"""

Path(out_path).write_text(html, encoding="utf-8")
print(f"Wrote {out_path}")
PY

cp "$SRC" "$OUT_DIR/overview.md"
cp "${ROOT}/scripts/development-overview-live.js" "$OUT_DIR/live.js"
if [[ -f "$ECO_JSON" ]]; then
  cp "$ECO_JSON" "$OUT_DIR/ecosystem-stats.json"
fi
echo "Generated ${OUT_HTML}"
