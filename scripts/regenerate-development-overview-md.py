#!/usr/bin/env python3
"""Regenerate docs/development-overview.md snapshot from gh (no Actions)."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPOS_FILE = ROOT / ".github/li-org-repos.txt"
OUT_MD = ROOT / "docs/development-overview.md"

LIVE_DOCS = {
    "benchmarks": "https://li-langverse.github.io/benchmarks/",
    "li-language": "https://li-langverse.github.io/li-language/",
    "roadmap": "https://li-langverse.github.io/roadmap/development-overview/",
}


def run_json(args: list[str]) -> list[dict] | dict | None:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        return None
    if not proc.stdout.strip():
        return None
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
            req = Request(url, method="HEAD")
            with urlopen(req, timeout=12) as resp:
                if 200 <= resp.status < 400:
                    n += 1
        except OSError:
            pass
    return n


def load_repos() -> list[str]:
    repos: list[str] = []
    for line in REPOS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            repos.append(line)
    return repos


def main() -> int:
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        print("error: gh auth required — GH_TOKEN or gh auth login", file=sys.stderr)
        return 1

    repos = load_repos()
    scanned = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    pull_requests: list[dict] = []

    for repo in repos:
        rows = run_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,baseRefName,isDraft,statusCheckRollup",
                "--limit",
                "50",
            ]
        )
        if not isinstance(rows, list):
            continue
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
    live_n = live_docs_count()

    merge_ready = [p for p in pull_requests if p["ready"]]
    merge_blocked = [p for p in pull_requests if not p["ready"] and p["ci"] == "fail"]

    lines: list[str] = [
        "# Li development overview",
        "",
        f"**li-langverse org** · scanned **{scanned}** · `gh pr list` / checks · live docs HEAD",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Ready to merge (CI green) | {ready} |",
        f"| Open PRs | {open_count} |",
        f"| Blocked / needs work | {blocked} |",
        f"| Repos with live docs | {live_n} / {len(repos)} |",
        "",
        "## Recommended merge order",
        "",
    ]

    if merge_ready:
        for i, p in enumerate(merge_ready[:12], 1):
            lines.append(
                f"{i}. [{p['repo']} #{p['number']}]({p['url']}) — {p['title'][:72]}"
            )
    else:
        lines.append("_No PRs with green CI and non-draft status._")

    lines.extend(
        [
            "",
            "## Merge when reviewed",
            "",
            "| Priority | PR | CI | Action | Notes |",
            "|----------|-----|-----|--------|-------|",
        ]
    )
    for p in merge_ready:
        lines.append(
            f"| P0 | [{p['repo']}#{p['number']}]({p['url']}) | {p['ci']} | Merge when approved | Auto snapshot {scanned} |"
        )
    if not merge_ready:
        lines.append("| — | — | — | — | No green PRs |")

    lines.extend(
        [
            "",
            "## Do not merge yet",
            "",
            "| PR | CI | Action | Notes |",
            "|-----|-----|--------|-------|",
        ]
    )
    for p in merge_blocked:
        lines.append(
            f"| [{p['repo']}#{p['number']}]({p['url']}) | {p['ci']} | Fix CI first | {p['title'][:60]} |"
        )
    if not merge_blocked:
        lines.append("| — | — | — | No failing open PRs |")

    lines.extend(
        [
            "",
            "## All open PRs",
            "",
            "| Repo | # | Title | Base | CI | Ready |",
            "|------|---|-------|------|-----|-------|",
        ]
    )
    for p in pull_requests:
        title = p["title"][:70] + ("…" if len(p["title"]) > 70 else "")
        lines.append(
            f"| {p['repo']} | {p['number']} | [{title}]({p['url']}) | {p['base']} | {p['ci']} | {'yes' if p['ready'] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main`.*",
            "",
            "*Snapshot: `./scripts/regenerate-development-overview-md.py` then `./scripts/deploy-pages-local.sh --build`. "
            "Live queue: browser on [development overview](https://li-langverse.github.io/roadmap/development-overview/) — no redeploy for queue-only changes.*",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD} ({open_count} open PRs, {ready} ready, live docs {live_n}/{len(repos)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
