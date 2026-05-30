#!/usr/bin/env python3
"""Refresh development-overview status.json from live GitHub org data."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ORG = "li-langverse"
ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "development-overview" / "status.json"
REPOS_HINT = ROOT / ".github" / "li-org-repos.txt"

# Custom / known doc sites (extend when new Pages domains ship).
KNOWN_DOC_URLS: dict[str, str] = {
    "benchmarks": "https://benchmarks.lilangverse.xyz/",
    "lic-docs": "https://docs.lilangverse.xyz/",
    "roadmap": "https://progress.lilangverse.xyz/",
    "proof-library": "https://proofs.lilangverse.xyz/",
    "li-language": "https://li-langverse.github.io/li-language/",
}


def gh_json(args: list[str]) -> Any:
    proc = subprocess.run(
        ["gh", "api", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        return None
    if not proc.stdout or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def gh_paginate(endpoint: str) -> list[Any]:
    proc = subprocess.run(
        ["gh", "api", endpoint, "--paginate"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        return []
    items: list[Any] = []
    for chunk in proc.stdout.split("\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            page = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(page, list):
            items.extend(page)
    return items


def gh_cli_json(args: list[str]) -> Any:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        return None
    if not proc.stdout or not proc.stdout.strip():
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


def http_ok(url: str, timeout: float = 10.0) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def load_repo_hints() -> set[str]:
    hints: set[str] = set()
    if REPOS_HINT.is_file():
        for line in REPOS_HINT.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                hints.add(line)
    return hints


def fetch_org_repos() -> list[dict]:
    repos = gh_paginate(f"orgs/{ORG}/repos?type=public&per_page=100")
    repos.sort(key=lambda r: r.get("name", "").lower())
    return [r for r in repos if isinstance(r, dict) and not r.get("archived")]


def workflows_on_main(repo: str) -> tuple[bool, list[str]]:
    data = gh_json([f"repos/{ORG}/{repo}/contents/.github/workflows?ref=main"])
    if not data:
        data = gh_json([f"repos/{ORG}/{repo}/contents/.github/workflows"])
    if not isinstance(data, list):
        return False, []
    names = sorted(
        item.get("name", "")
        for item in data
        if isinstance(item, dict) and str(item.get("name", "")).endswith((".yml", ".yaml"))
    )
    return bool(names), names


def main_branch_ci_state(repo: str) -> str:
    runs = gh_json([f"repos/{ORG}/{repo}/actions/runs?branch=main&per_page=1"])
    if not runs or not runs.get("workflow_runs"):
        return "none"
    run = runs["workflow_runs"][0]
    con = (run.get("conclusion") or "").lower()
    st = (run.get("status") or "").lower()
    if st != "completed":
        return "pending"
    if con in ("success", "skipped", "neutral"):
        return "pass"
    if con in ("failure", "cancelled", "timed_out", "action_required", "stale"):
        return "fail"
    return "unknown"


def resolve_live_docs(name: str, repo: dict) -> str | None:
    if name in KNOWN_DOC_URLS:
        url = KNOWN_DOC_URLS[name]
        return url if http_ok(url) else None
    homepage = repo.get("homepage") or ""
    if homepage.startswith("http") and http_ok(homepage):
        return homepage
    if repo.get("has_pages"):
        pages_url = f"https://{ORG}.github.io/{name}/"
        return pages_url if http_ok(pages_url) else None
    return None


def fetch_open_prs() -> list[dict]:
    pull_requests: list[dict] = []
    page = 1
    while page <= 10:
        data = gh_json(
            [
                f"search/issues?q=org:{ORG}+is:open+is:pr&per_page=100&page={page}",
            ]
        )
        if not data:
            break
        for item in data.get("items") or []:
            repo_url = item.get("repository_url") or ""
            repo = repo_url.rsplit("/", 1)[-1] if repo_url else "unknown"
            pull_requests.append(
                {
                    "repo": repo,
                    "number": item["number"],
                    "title": item.get("title", ""),
                    "url": item.get("html_url", ""),
                    "base": "main",
                    "draft": False,
                    "ci": "pending",
                    "ready": False,
                }
            )
        if len(data.get("items") or []) < 100:
            break
        page += 1

    # Enrich with CI rollup via gh pr list per repo (accurate checks).
    by_repo: dict[str, list[dict]] = {}
    for pr in pull_requests:
        by_repo.setdefault(pr["repo"], []).append(pr)

    enriched: list[dict] = []
    for repo, prs in sorted(by_repo.items()):
        rows = gh_cli_json(
            [
                "pr",
                "list",
                "--repo",
                f"{ORG}/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,baseRefName,isDraft,statusCheckRollup",
                "--limit",
                "100",
            ]
        )
        rollup_by_num = {
            r["number"]: r for r in (rows or []) if isinstance(r, dict)
        }
        for pr in prs:
            row = rollup_by_num.get(pr["number"])
            if row:
                ci = classify_ci(row.get("statusCheckRollup"))
                pr["title"] = row.get("title", pr["title"])
                pr["url"] = row.get("url", pr["url"])
                pr["base"] = row.get("baseRefName", pr["base"])
                pr["draft"] = bool(row.get("isDraft"))
                pr["ci"] = ci
                pr["ready"] = ci == "pass" and not pr["draft"]
            enriched.append(pr)
    enriched.sort(key=lambda p: (p["repo"], p["number"]))
    return enriched


def fetch_org_open_issues() -> int:
    data = gh_json([f"search/issues?q=org:{ORG}+is:open+is:issue"])
    if isinstance(data, dict):
        return int(data.get("total_count") or 0)
    return 0


def build_repo_row(name: str, repo: dict, open_prs: int) -> dict:
    combined = int(repo.get("open_issues_count") or 0)
    open_issues = max(0, combined - open_prs)
    has_ci, workflow_names = workflows_on_main(name)
    return {
        "name": name,
        "description": (repo.get("description") or "").strip(),
        "default_branch": repo.get("default_branch") or "main",
        "updated_at": repo.get("pushed_at") or repo.get("updated_at"),
        "open_issues": open_issues,
        "open_prs": open_prs,
        "has_ci": has_ci,
        "workflow_count": len(workflow_names),
        "workflows": workflow_names[:8],
        "main_ci_last": main_branch_ci_state(name) if has_ci else "none",
        "live_docs": resolve_live_docs(name, repo),
        "url": repo.get("html_url") or f"https://github.com/{ORG}/{name}",
    }


def main() -> int:
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        sys.stderr.write("error: gh CLI must be authenticated\n")
        return 1

    hints = load_repo_hints()
    org_repos = fetch_org_repos()
    repo_by_name = {r["name"]: r for r in org_repos if r.get("name")}

    pull_requests = fetch_open_prs()
    pr_count_by_repo: dict[str, int] = {}
    for pr in pull_requests:
        pr_count_by_repo[pr["repo"]] = pr_count_by_repo.get(pr["repo"], 0) + 1

    repos_out: list[dict] = []
    for name, repo in sorted(repo_by_name.items()):
        repos_out.append(build_repo_row(name, repo, pr_count_by_repo.get(name, 0)))

    # Surface repos listed in hints but missing from org (renamed/deleted).
    missing_hints = sorted(hints - set(repo_by_name))

    ready = sum(1 for p in pull_requests if p["ready"])
    open_prs = len(pull_requests)
    blocked = sum(
        1
        for p in pull_requests
        if not p["ready"] and (p["ci"] in ("fail", "pending") or p["draft"])
    )
    open_issues = fetch_org_open_issues()
    live_docs = sum(1 for r in repos_out if r.get("live_docs"))
    with_ci = sum(1 for r in repos_out if r["has_ci"])

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "pages_url": "https://progress.lilangverse.xyz/",
        "org": ORG,
        "metrics": {
            "ready_to_merge": ready,
            "open_prs": open_prs,
            "blocked_prs": blocked,
            "open_issues": open_issues,
            "public_repos": len(repos_out),
            "repos_with_ci": with_ci,
            "repos_with_live_docs": live_docs,
            "repo_hints": len(hints),
            "missing_hint_repos": missing_hints,
        },
        "repos": repos_out,
        "pull_requests": pull_requests,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    m = payload["metrics"]
    print(
        f"Wrote {OUT_JSON}: {m['public_repos']} repos, "
        f"{m['open_prs']} PRs ({m['ready_to_merge']} ready), "
        f"{m['open_issues']} issues, {m['repos_with_live_docs']} live docs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
