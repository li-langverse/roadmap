#!/usr/bin/env python3
"""Apply or update GitHub repository rulesets for li-langverse org repos.

Blocks direct push to main/dev/master; requires PR + 1 approval; optional CI contexts.
Idempotent: upserts ruleset by name. Run from roadmap checkout with GH_TOKEN (via with-github-env.sh).

Usage:
  ./scripts/apply-org-branch-protection.py              # all org repos
  ./scripts/apply-org-branch-protection.py lic lip    # subset
  ./scripts/apply-org-branch-protection.py --dry-run lic
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "scripts" / "org-branch-protection.json"
API = "https://api.github.com"


def gh_request(method: str, path: str, body: dict | None = None) -> Any:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN not set — run via scripts/with-github-env.sh")
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise SystemExit(f"GitHub API {method} {path} -> {e.code}: {err}") from e


def gh_get(path: str) -> Any:
    return gh_request("GET", path)


def gh_post(path: str, body: dict) -> Any:
    return gh_request("POST", path, body)


def gh_put(path: str, body: dict) -> Any:
    return gh_request("PUT", path, body)


def load_config() -> dict:
    with CONFIG.open(encoding="utf-8") as f:
        return json.load(f)


def list_org_repos(org: str) -> list[str]:
    names: list[str] = []
    page = 1
    while True:
        chunk = gh_get(f"/orgs/{org}/repos?per_page=100&page={page}")
        if not chunk:
            break
        names.extend(r["name"] for r in chunk)
        if len(chunk) < 100:
            break
        page += 1
    return sorted(names)


def repo_branches(org: str, repo: str, prefixes: list[str]) -> list[str]:
    """Return ref includes that exist on the remote (main/dev/master)."""
    want = {p.removeprefix("refs/heads/") for p in prefixes}
    found: set[str] = set()
    page = 1
    while True:
        try:
            chunk = gh_get(f"/repos/{org}/{repo}/branches?per_page=100&page={page}")
        except SystemExit:
            return [p for p in prefixes if p.endswith("/main")]
        if not chunk:
            break
        for b in chunk:
            if b["name"] in want:
                found.add(b["name"])
        if len(chunk) < 100:
            break
        page += 1
    if not found:
        default = gh_get(f"/repos/{org}/{repo}")["default_branch"]
        found.add(default)
    return [f"refs/heads/{b}" for b in sorted(found)]


def build_ruleset(
    name: str,
    refs: list[str],
    checks: list[str],
    codeowners: bool,
) -> dict:
    rules: list[dict] = [
        {"type": "update"},
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {
            "type": "pull_request",
            "parameters": {
                "dismiss_stale_reviews_on_push": True,
                "require_code_owner_review": codeowners,
                "require_last_push_approval": False,
                "required_approving_review_count": 1,
                "required_review_thread_resolution": False,
            },
        },
    ]
    if checks:
        rules.append(
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": [{"context": c} for c in checks],
                },
            }
        )
    return {
        "name": name,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": refs, "exclude": []}},
        "rules": rules,
    }


def find_ruleset(org: str, repo: str, name: str) -> dict | None:
    rulesets = gh_get(f"/repos/{org}/{repo}/rulesets") or []
    for rs in rulesets:
        if rs.get("name") == name:
            return rs
    return None


def upsert_ruleset(org: str, repo: str, payload: dict, dry_run: bool) -> str:
    existing = find_ruleset(org, repo, payload["name"])
    path = f"/repos/{org}/{repo}/rulesets"
    if dry_run:
        action = "PUT" if existing else "POST"
        print(f"  [dry-run] {action} {org}/{repo} ruleset '{payload['name']}' refs={payload['conditions']['ref_name']['include']}")
        return "dry-run"
    if existing:
        gh_put(f"{path}/{existing['id']}", payload)
        return "updated"
    gh_post(path, payload)
    return "created"


def repo_settings(cfg: dict, repo: str) -> dict:
    repos = cfg.get("repos", {})
    base = dict(cfg.get("default_repo", {}))
    if repo in repos:
        base.update(repos[repo])
    return base


def main() -> None:
    argv = sys.argv[1:]
    dry_run = False
    if "--dry-run" in argv:
        dry_run = True
        argv = [a for a in argv if a != "--dry-run"]

    cfg = load_config()
    org = cfg["org"]
    ruleset_name = cfg["ruleset_name"]
    ref_prefixes = cfg["protected_ref_prefixes"]

    if argv:
        targets = argv
    else:
        targets = list_org_repos(org)

    print(f"Org: {org} | ruleset: {ruleset_name} | repos: {len(targets)}")
    results: list[tuple[str, str]] = []

    for repo in targets:
        settings = repo_settings(cfg, repo)
        refs = repo_branches(org, repo, ref_prefixes)
        payload = build_ruleset(
            ruleset_name,
            refs,
            settings.get("required_checks", []),
            bool(settings.get("require_code_owner_review", False)),
        )
        print(f"==> {repo}")
        try:
            action = upsert_ruleset(org, repo, payload, dry_run)
            results.append((repo, action))
            print(f"    {action}: {', '.join(refs)} checks={settings.get('required_checks', [])}")
        except SystemExit as e:
            print(f"    ERROR: {e}", file=sys.stderr)
            results.append((repo, "failed"))

    failed = [r for r, a in results if a == "failed"]
    if failed:
        raise SystemExit(f"failed repos: {', '.join(failed)}")
    print("Done.")


if __name__ == "__main__":
    main()
