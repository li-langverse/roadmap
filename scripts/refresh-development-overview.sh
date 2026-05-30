#!/usr/bin/env bash
# Refresh live merge-queue JSON from GitHub (gh). Committed to data/ for Pages polling.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPOS_FILE="${ROOT}/.github/li-org-repos.txt"
OUT_DIR="${ROOT}/data/development-overview"
OUT_JSON="${OUT_DIR}/status.json"

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI required" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

if [[ -x "${ROOT}/scripts/compute-ecosystem-stats.py" ]]; then
  ECOSYSTEM_STATS_SKIP_CLONE="${ECOSYSTEM_STATS_SKIP_CLONE:-1}" \
    python3 "${ROOT}/scripts/compute-ecosystem-stats.py" || true
fi

export ROOT REPOS_FILE OUT_JSON
python3 <<'PY'
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.environ["ROOT"])
repos_file = Path(os.environ["REPOS_FILE"])
out_json = Path(os.environ["OUT_JSON"])

repos: list[str] = []
for line in repos_file.read_text(encoding="utf-8").splitlines():
    line = line.split("#", 1)[0].strip()
    if line:
        repos.append(line)

LIVE_DOCS = {
    "benchmarks": "https://li-langverse.github.io/benchmarks/",
    "li-language": "https://li-langverse.github.io/li-language/",
}


def run_json(args: list[str]) -> list[dict]:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        return []
    if not proc.stdout.strip():
        return []
    return json.loads(proc.stdout)


def classify_ci(rollup: list[dict] | None) -> str:
    if not rollup:
        return "none"
    statuses: list[str] = []
    for item in rollup:
        st = (item.get("status") or "").upper()
        con = (item.get("conclusion") or "").upper()
        if st in ("QUEUED", "IN_PROGRESS", "PENDING", "WAITING", "REQUESTED"):
            statuses.append("pending")
        elif con in ("FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STALE"):
            statuses.append("fail")
        elif con in ("SUCCESS", "SKIPPED", "NEUTRAL"):
            statuses.append("pass")
        else:
            statuses.append("pending")
    if any(s == "fail" for s in statuses):
        return "fail"
    if any(s == "pending" for s in statuses):
        return "pending"
    if statuses:
        return "pass"
    return "none"


def live_docs_count() -> int:
    n = 0
    for url in LIVE_DOCS.values():
        try:
            import urllib.request

            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=12) as resp:
                if 200 <= resp.status < 400:
                    n += 1
        except Exception:
            pass
    return n


pull_requests: list[dict] = []
for repo in repos:
    slug = f"li-langverse/{repo}"
    rows = run_json(
        [
            "pr",
            "list",
            "--repo",
            slug,
            "--state",
            "open",
            "--json",
            "number,title,url,baseRefName,isDraft,statusCheckRollup",
            "--limit",
            "50",
        ]
    )
    for pr in rows:
        ci = classify_ci(pr.get("statusCheckRollup"))
        pull_requests.append(
            {
                "repo": repo,
                "number": pr["number"],
                "title": pr["title"],
                "url": pr["url"],
                "base": pr.get("baseRefName", "main"),
                "ci": ci,
                "draft": bool(pr.get("isDraft")),
                "ready": ci == "pass" and not pr.get("isDraft"),
            }
        )

pull_requests.sort(key=lambda p: (p["repo"], p["number"]))

ready = sum(1 for p in pull_requests if p["ready"])
open_count = len(pull_requests)
blocked = sum(
    1
    for p in pull_requests
    if not p["ready"] and (p["ci"] in ("fail", "pending") or p["draft"])
)

eco_path = root / "data" / "development-overview" / "ecosystem-stats.json"
ecosystem = {}
if eco_path.is_file():
    try:
        ecosystem = json.loads(eco_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        pass

payload = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
    "pages_url": "https://li-langverse.github.io/roadmap/development-overview/",
    "metrics": {
        "ready_to_merge": ready,
        "open_prs": open_count,
        "blocked": blocked,
        "repos_with_live_docs": live_docs_count(),
        "repos_total": len(repos),
    },
    "ecosystem": ecosystem,
    "pull_requests": pull_requests,
}

out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {out_json} ({open_count} open PRs, {ready} ready)")
PY
