#!/usr/bin/env python3
"""Configure li-langverse GitHub org for GHCR-only (archive git mirror repos).

Default is dry-run. Use --apply to mutate GitHub.

Keeps active: `.github` (org profile).
Archives: all other repos in the org (restores stale git mirrors to read-only).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time

ORG = "li-langverse"
GITLAB_GROUP = "https://gitlab.lilangverse.xyz/li-langverse"
ORG_DESCRIPTION = (
    "Li ecosystem - develop on GitLab. This GitHub org is GHCR-only "
    "(ghcr.io/li-langverse). Source: gitlab.lilangverse.xyz/li-langverse"
)
KEEP_REPOS = frozenset({".github"})
REPO_DESCRIPTION_TEMPLATE = (
    "ARCHIVED mirror — do not use for git. Develop on GitLab: "
    f"{GITLAB_GROUP}/{{name}}"
)


def gh_json(args: list[str]) -> dict | list | None:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        return None
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_org_repos() -> list[dict]:
    data = gh_json(
        ["repo", "list", ORG, "--limit", "1000", "--json", "name,isArchived,description"]
    )
    return data if isinstance(data, list) else []


def gh_rate_limit_ok(min_remaining: int = 10) -> bool:
    data = gh_json(["api", "rate_limit"])
    if not isinstance(data, dict):
        return True
    core = data.get("resources", {}).get("core", {})
    remaining = core.get("remaining", 1)
    reset = core.get("reset", 0)
    if remaining >= min_remaining:
        return True
    wait = max(0, int(reset) - int(time.time()) + 5)
    sys.stderr.write(
        f"GitHub API rate limit low ({remaining} left). "
        f"Reset in ~{wait // 60}m. Re-run later or use --stamp-only after reset.\n"
    )
    return False


def patch_org_description(apply: bool) -> None:
    print(f"org description -> {ORG_DESCRIPTION!r}")
    if not apply:
        return
    if not gh_rate_limit_ok():
        sys.exit(2)
    proc = subprocess.run(
        [
            "gh",
            "api",
            f"orgs/{ORG}",
            "-X",
            "PATCH",
            "-f",
            f"description={ORG_DESCRIPTION}",
            "-f",
            f"blog={GITLAB_GROUP}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        sys.exit(1)
    print("OK org description")


def stamp_repo(name: str, apply: bool) -> None:
    desc = REPO_DESCRIPTION_TEMPLATE.format(name=name)
    print(f"  stamp {name}: {desc[:72]}...")
    if not apply:
        return
    if not gh_rate_limit_ok(min_remaining=5):
        sys.exit(2)
    proc = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{ORG}/{name}",
            "-X",
            "PATCH",
            "-f",
            f"description={desc}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(f"FAIL stamp {name}: {proc.stderr}\n")


def archive_repo(name: str, apply: bool) -> None:
    print(f"  archive {name}")
    if not apply:
        return
    if not gh_rate_limit_ok(min_remaining=5):
        sys.exit(2)
    proc = subprocess.run(
        ["gh", "repo", "archive", f"{ORG}/{name}", "--yes"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(f"FAIL archive {name}: {proc.stderr}\n")
    time.sleep(0.5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Mutate GitHub (default is dry-run preview)",
    )
    parser.add_argument(
        "--stamp-only",
        action="store_true",
        help="Update org + repo descriptions only; do not archive",
    )
    args = parser.parse_args()

    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        sys.stderr.write("error: gh not authenticated\n")
        return 1

    repos = list_org_repos()
    if not repos:
        sys.stderr.write("error: no repos from gh repo list\n")
        return 1

    to_archive = [
        r["name"]
        for r in repos
        if r["name"] not in KEEP_REPOS and not r.get("isArchived")
    ]
    already = [r["name"] for r in repos if r.get("isArchived")]

    print(f"org={ORG} repos={len(repos)} keep={sorted(KEEP_REPOS)}")
    print(f"would archive {len(to_archive)} repos; already archived {len(already)}")
    if already:
        print(f"  archived: {', '.join(sorted(already)[:8])}{'…' if len(already) > 8 else ''}")

    patch_org_description(args.apply)

    for name in sorted(to_archive):
        stamp_repo(name, args.apply)
        if not args.stamp_only:
            archive_repo(name, args.apply)

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to execute.")
        print("  --stamp-only   descriptions only, no archive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
