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
sys.path.insert(0, str(root / "scripts"))
from _overview_history_metrics import history_point_metrics
repos_file = Path(os.environ["REPOS_FILE"])
out_json = Path(os.environ["OUT_JSON"])

repos: list[str] = []
for line in repos_file.read_text(encoding="utf-8").splitlines():
    line = line.split("#", 1)[0].strip()
    if line:
        repos.append(line)

LIVE_DOCS = {
    "benchmarks": "https://benchmarks.lilangverse.xyz/",
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


vcs_source = "github"
pull_requests: list[dict] = []
if os.environ.get("GITLAB_TOKEN", "").strip():
    try:
        from _gitlab_overview_api import fetch_gitlab_open_merge_requests

        pull_requests = fetch_gitlab_open_merge_requests(limit=250)
        if pull_requests:
            vcs_source = "gitlab"
    except Exception as exc:
        sys.stderr.write(f"gitlab MR fetch failed: {exc}\n")

if not pull_requests:
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
                    "source": "github",
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
    "pages_url": "https://progress.lilangverse.xyz/",
    "vcs_source": vcs_source,
    "metrics": {
        "ready_to_merge": ready,
        "open_prs": open_count,
        "open_mrs": open_count if vcs_source == "gitlab" else None,
        "blocked": blocked,
        "repos_with_live_docs": live_docs_count(),
        "repos_total": len(repos),
    },
    "ecosystem": ecosystem,
    "merge_requests": pull_requests if vcs_source == "gitlab" else [],
    "pull_requests": pull_requests,
}

out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {out_json} ({open_count} open PRs, {ready} ready)")

history_path = root / "data" / "development-overview" / "history.json"
history = {"version": 1, "org": "li-langverse", "points": []}
if history_path.is_file():
    try:
        history = json.loads(history_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        pass
points: list[dict] = list(history.get("points") or [])

def search_total(query: str) -> int | None:
    proc = subprocess.run(
        ["gh", "api", f"search/issues?q={query}", "--jq", ".total_count"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    try:
        return int(proc.stdout.strip())
    except ValueError:
        return None

METRIC_KEYS = ("open_prs", "ready_to_merge", "prs_closed", "issues_open", "issues_closed")

def day_key(at: str) -> str:
    return str(at)[:10]


def merge_daily(prev: dict | None, nxt: dict) -> dict:
    day = day_key(nxt.get("at", ""))
    out = {**(prev or {}), **nxt, "at": day}
    for key in METRIC_KEYS:
        if not isinstance(out.get(key), (int, float)) and isinstance(
            (prev or {}).get(key), (int, float)
        ):
            out[key] = prev[key]
    return out


def compact_daily(raw_points: list[dict]) -> list[dict]:
    by_day: dict[str, dict] = {}
    for p in sorted(raw_points, key=lambda x: day_key(str(x.get("at", "")))):
        day = day_key(str(p.get("at", "")))
        if not day:
            continue
        by_day[day] = merge_daily(by_day.get(day), p)
    return [by_day[d] for d in sorted(by_day.keys())]


today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
issues_open = ecosystem.get("issues_open")
if issues_open is None and ecosystem.get("issues_source") != "gitlab":
    issues_open = search_total(f"org:li-langverse+is:issue+is:open")
cumulative = history_point_metrics(ecosystem)
issues_closed = cumulative["issues_closed"]
if issues_closed is None and ecosystem.get("issues_source") != "gitlab":
    issues_closed = search_total(f"org:li-langverse+is:issue+is:closed")
mrs_closed = cumulative["prs_closed"]
if mrs_closed is None and vcs_source != "gitlab":
    mrs_closed = search_total(f"org:li-langverse+is:pr+is:closed")
new_point = {
    "at": today,
    "open_prs": open_count,
    "open_mrs": open_count if vcs_source == "gitlab" else None,
    "ready_to_merge": ready,
    "prs_closed": mrs_closed,
    "mrs_closed": ecosystem.get("mrs_closed") if vcs_source == "gitlab" else mrs_closed,
    "issues_open": issues_open,
    "issues_closed": issues_closed,
    "source": ecosystem.get("issues_source", vcs_source),
    "vcs_source": vcs_source,
}
points = compact_daily(points + [new_point])
if len(points) > 400:
    points = points[-400:]
history["points"] = points
history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {history_path} ({len(points)} points)")

PY
