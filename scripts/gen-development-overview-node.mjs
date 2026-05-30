#!/usr/bin/env node
/** Fallback site generator when Python markdown/venv is unavailable. */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { execFileSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "docs/development-overview.md");
const OUT_DIR = path.join(ROOT, "site/development-overview");
const OUT_HTML = path.join(OUT_DIR, "index.html");
const LIVE_JS = path.join(ROOT, "scripts/development-overview-live.js");

const md = fs.readFileSync(SRC, "utf8");
const asOf =
  md.match(/scanned \*\*([^*]+)\*\*/)?.[1] ?? new Date().toISOString().slice(0, 16) + "Z";

const body = execFileSync(
  "npx",
  ["--yes", "marked", "--gfm"],
  { input: md, encoding: "utf8", cwd: ROOT, maxBuffer: 10 * 1024 * 1024 }
).replace(/^<h1[^>]*>.*?<\/h1>\s*/s, "");

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Li development overview — li-langverse</title>
  <style>
    :root { --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e; --border:#30363d; --accent:#58a6ff; }
    body { margin:0; font-family:system-ui,sans-serif; background:var(--bg); color:var(--fg); line-height:1.55; }
    .wrap { max-width:1100px; margin:0 auto; padding:2rem 1.25rem 4rem; }
    header { margin-bottom:2rem; border-bottom:1px solid var(--border); padding-bottom:1rem; }
    a { color:var(--accent); }
    h2 { margin-top:2.25rem; font-size:1.25rem; border-bottom:1px solid var(--border); padding-bottom:.35rem; }
    table { width:100%; border-collapse:collapse; font-size:.88rem; margin:1rem 0; }
    th,td { border:1px solid var(--border); padding:.45rem .6rem; text-align:left; }
    th { background:#161b22; }
    .live-banner { margin:1rem 0 1.5rem; padding:.75rem 1rem; border:1px solid var(--border); border-radius:6px; background:#161b22; }
    .live-metrics { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:.75rem; margin:1rem 0; }
    .metric-card { border:1px solid var(--border); border-radius:6px; padding:.65rem .75rem; }
    .metric-card .label { color:var(--muted); font-size:.78rem; }
    .metric-card .value { font-size:1.35rem; font-weight:600; }
    #live-status { color:var(--muted); font-size:.82rem; }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Li development overview</h1>
      <p>li-langverse org · snapshot <span id="snapshot-as-of">${asOf}</span> · <span id="live-status">loading live queue…</span></p>
      <nav><a href="https://li-langverse.github.io/benchmarks/">Benchmarks</a> · <a href="https://github.com/li-langverse/roadmap">roadmap</a></nav>
    </header>
    <section class="live-banner">
      <h2>Live PR merge queue</h2>
      <p>Browser polls GitHub API — no Actions cron.</p>
      <div class="live-metrics" id="live-metrics"></div>
      <table id="live-pr-table"><thead><tr><th>Repo</th><th>#</th><th>Title</th><th>Base</th><th>CI</th><th>Ready</th></tr></thead><tbody id="live-pr-body"></tbody></table>
    </section>
    <main>${body}</main>
  </div>
  <script src="./live.js" defer></script>
</body>
</html>`;

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(OUT_HTML, html);
fs.copyFileSync(SRC, path.join(OUT_DIR, "overview.md"));
fs.copyFileSync(LIVE_JS, path.join(OUT_DIR, "live.js"));
console.log(`Wrote ${OUT_HTML}`);
