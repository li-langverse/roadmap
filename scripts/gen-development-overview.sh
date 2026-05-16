#!/usr/bin/env bash
# Generate static HTML for GitHub Pages from docs/development-overview.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/docs/development-overview.md"
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

"$PY" - "$SRC" "$OUT_HTML" "$AS_OF" <<'PY'
import re
import sys
from pathlib import Path

src_path, out_path, as_of = sys.argv[1:4]
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
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Li development overview</h1>
      <p>li-langverse org · as of {as_of} · <a href="https://github.com/li-langverse/roadmap/blob/main/docs/development-overview.md">edit source</a></p>
      <nav class="nav" aria-label="Related">
        <a href="https://li-langverse.github.io/benchmarks/">Benchmarks</a>
        <a href="https://li-langverse.github.io/li-language/">Language docs</a>
        <a href="https://github.com/li-langverse/roadmap">roadmap repo</a>
      </nav>
    </header>
    <main>
{body}
    </main>
  </div>
</body>
</html>
"""

html = html.replace("<motion.div", "<div")

Path(out_path).write_text(html, encoding="utf-8")
print(f"Wrote {out_path}")
PY

cp "$SRC" "$OUT_DIR/overview.md"
echo "Generated ${OUT_HTML}"
