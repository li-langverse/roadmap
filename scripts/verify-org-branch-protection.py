#!/usr/bin/env python3
"""Verify Li: protected branches ruleset exists and is active on org repos."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Reuse apply module helpers
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_org_branch_protection import (  # type: ignore
    find_ruleset,
    gh_get,
    load_config,
    list_org_repos,
)


def main() -> None:
    cfg = load_config()
    org = cfg["org"]
    name = cfg["ruleset_name"]
    repos = sys.argv[1:] if len(sys.argv) > 1 else list_org_repos(org)
    missing = []
    for repo in repos:
        rs = find_ruleset(org, repo, name)
        if not rs or rs.get("enforcement") != "active":
            missing.append(repo)
            print(f"FAIL {repo}: ruleset missing or not active")
        else:
            print(f"OK   {repo}: ruleset {rs['id']}")
    if missing:
        raise SystemExit(f"{len(missing)} repo(s) missing protection — run apply-org-branch-protection.py")
    print("All protected.")


if __name__ == "__main__":
    main()
