#!/usr/bin/env python3
"""Compute li-langverse ecosystem stats (LoC, org repo count) for the development overview."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from _gitlab_overview_api import (
    GITLAB_GROUP,
    GITLAB_HOST,
    gitlab_group_issue_counts,
    gitlab_group_mr_counts,
    gitlab_project_count,
    gitlab_token,
)
from _overview_history_metrics import cumulative_issues_closed, cumulative_prs_closed

ORG = "li-langverse"
CODE_SUFFIXES = {
    ".li",
    ".cpp",
    ".h",
    ".hpp",
    ".c",
    ".py",
    ".rs",
    ".toml",
    ".lean",
    ".sh",
    ".md",
    ".yml",
    ".yaml",
    ".jl",
    ".lock",
}
SKIP_DIR_NAMES = {
    ".git",
    "build",
    "target",
    "node_modules",
    ".venv",
    ".venv-docs",
    ".venv-overview",
    "vendor",
    "__pycache__",
    "site",
    "dist",
    "out",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_repo_list(path: Path) -> list[str]:
    repos: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            repos.append(line)
    return repos


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


def search_total_count(query: str) -> int | None:
    data = gh_json(["api", f"search/issues?q={query}", "--jq", ".total_count"])
    time.sleep(float(os.environ.get("ECOSYSTEM_STATS_SEARCH_GAP_SEC", "2")))
    if isinstance(data, int):
        return data
    return None


def issue_counts() -> tuple[int | None, int | None, str]:
    """(open, closed, source) — GitLab primary when GITLAB_TOKEN is set."""
    provider = os.environ.get("LI_VCS_PROVIDER", "gitlab").strip().lower()
    use_gitlab = provider != "github" and gitlab_token() is not None
    if use_gitlab:
        open_n, closed_n = gitlab_group_issue_counts()
        if open_n is not None or closed_n is not None:
            return open_n, closed_n, "gitlab"
    open_n = search_total_count(f"org:{ORG}+is:issue+is:open")
    closed_n = search_total_count(f"org:{ORG}+is:issue+is:closed")
    return open_n, closed_n, "github"


def mr_counts() -> tuple[int | None, int | None, str]:
    """(open, closed/merged, source) — GitLab primary when GITLAB_TOKEN is set."""
    provider = os.environ.get("LI_VCS_PROVIDER", "gitlab").strip().lower()
    use_gitlab = provider != "github" and gitlab_token() is not None
    if use_gitlab:
        open_n, closed_n = gitlab_group_mr_counts()
        if open_n is not None or closed_n is not None:
            return open_n, closed_n, "gitlab"
    open_n = search_total_count(f"org:{ORG}+is:pr+is:open")
    closed_n = search_total_count(f"org:{ORG}+is:pr+is:closed")
    return open_n, closed_n, "github"


def count_org_repositories() -> int | None:
    """All repositories visible to `gh` under the org (public + private for the token)."""
    proc = subprocess.run(
        ["gh", "repo", "list", ORG, "--limit", "10000", "--json", "name"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        data = json.loads(proc.stdout)
        if isinstance(data, list):
            return len(data)
    return count_org_repositories_via_token()


def count_org_repositories_via_token() -> int | None:
    """Fallback when `gh repo list` fails: paginate org repos with GITHUB_TOKEN (e.g. Actions)."""
    import urllib.error
    import urllib.request

    token = (
        os.environ.get("GH_TOKEN_OVERVIEW_PAGE")
        or os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
    )
    if not token:
        return None
    total = 0
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{ORG}/repos?per_page=100&page={page}&type=all"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                chunk = json.loads(resp.read().decode())
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return total if total else None
        if not isinstance(chunk, list) or not chunk:
            break
        total += len(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return total


def count_lines(repo_path: Path) -> int:
    total = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not d.startswith(".")]
        for name in files:
            if Path(name).suffix.lower() not in CODE_SUFFIXES:
                continue
            fp = Path(root) / name
            try:
                with fp.open("rb") as fh:
                    total += sum(1 for _ in fh)
            except OSError:
                pass
    return total


def clone_repo(name: str, dest: Path) -> bool:
    slug = f"{ORG}/{name}"
    proc = subprocess.run(
        ["gh", "repo", "clone", slug, str(dest / name), "--", "--depth", "1"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and (dest / name).is_dir()


def resolve_local_clone(name: str, parent: Path) -> Path | None:
    """Prefer sibling checkout under coding-projects when present."""
    candidates = [
        parent.parent / name,
        parent.parent / "li" if name == "li-language" else None,
    ]
    for p in candidates:
        if p is not None and p.is_dir() and (p / ".git").exists():
            return p
    return None


def compute_loc(repos: list[str], workdir: Path, clone_missing: bool) -> tuple[int, dict[str, int]]:
    per_repo: dict[str, int] = {}
    tmp_clone: Path | None = None
    if clone_missing:
        tmp_clone = Path(tempfile.mkdtemp(prefix="li-ecosystem-loc-"))
    try:
        for name in repos:
            local = resolve_local_clone(name, repo_root())
            if local is not None:
                per_repo[name] = count_lines(local)
                continue
            if tmp_clone is None:
                per_repo[name] = 0
                continue
            if clone_repo(name, tmp_clone):
                per_repo[name] = count_lines(tmp_clone / name)
            else:
                per_repo[name] = 0
    finally:
        if tmp_clone is not None:
            shutil.rmtree(tmp_clone, ignore_errors=True)
    return sum(per_repo.values()), per_repo




def merge_existing(payload: dict, path: Path) -> dict:
    """Keep committed snapshot values when a CI/gh refresh cannot resolve them."""
    if not path.is_file():
        return payload
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return payload
    if not isinstance(existing, dict):
        return payload
    for key, value in existing.items():
        if key not in payload or payload.get(key) is None:
            if value is not None:
                payload[key] = value
    existing_loc = existing.get("lines_of_code") or 0
    new_loc = payload.get("lines_of_code") or 0
    if existing_loc and (new_loc == 0 or new_loc < existing_loc * 0.75):
        payload["lines_of_code"] = existing_loc
        payload["lines_per_repo"] = existing.get("lines_per_repo", {})
    elif not payload.get("lines_of_code") and existing.get("lines_of_code"):
        payload["lines_of_code"] = existing["lines_of_code"]
        payload["lines_per_repo"] = existing.get("lines_per_repo", {})
    return payload

def main() -> int:
    overview = os.environ.get("GH_TOKEN_OVERVIEW_PAGE", "").strip()
    if overview:
        os.environ.setdefault("GH_TOKEN", overview)
        os.environ.setdefault("GITHUB_TOKEN", overview)

    root = repo_root()
    repos_file = root / ".github" / "li-org-repos.txt"
    out_dir = root / "data" / "development-overview"
    out_json = out_dir / "ecosystem-stats.json"

    if not repos_file.is_file():
        sys.stderr.write(f"missing {repos_file}\n")
        return 1
    if shutil.which("gh") is None:
        sys.stderr.write("error: gh CLI required\n")
        return 1

    repos = load_repo_list(repos_file)
    skip_clone = os.environ.get("ECOSYSTEM_STATS_SKIP_CLONE", "") == "1"
    clone_missing = not skip_clone

    if skip_clone:
        # Pages/CI only checks out roadmap — counting LoC here yields ~6k not ~67k.
        lines_total, lines_per_repo = None, None
    else:
        lines_total, lines_per_repo = compute_loc(repos, root, clone_missing)
    org_repositories = count_org_repositories()

    open_issues, closed_issues, issues_source = issue_counts()
    open_mrs, closed_mrs, mrs_source = mr_counts()
    gitlab_projects = gitlab_project_count() if gitlab_token() else None

    # GitHub org repo count remains useful during mirror transition.
    gh_open_prs = search_total_count(f"org:{ORG}+is:pr+is:open")
    gh_closed_prs = search_total_count(f"org:{ORG}+is:pr+is:closed")
    gh_open_issues = search_total_count(f"org:{ORG}+is:issue+is:open")
    gh_closed_issues = search_total_count(f"org:{ORG}+is:issue+is:closed")

    cumulative_closed_prs = cumulative_prs_closed(
        mrs_source=mrs_source,
        github_closed=gh_closed_prs,
        gitlab_closed=closed_mrs,
    )
    cumulative_closed_issues = cumulative_issues_closed(
        issues_source=issues_source,
        github_closed=gh_closed_issues,
        gitlab_closed=closed_issues,
    )

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "org": ORG,
        "vcs_primary": issues_source,
        "gitlab_host": GITLAB_HOST,
        "gitlab_group": GITLAB_GROUP,
        "repos_tracked": len(repos),
        "org_repositories": org_repositories,
        "gitlab_projects": gitlab_projects,
        "issues_source": issues_source,
        "issues_open": open_issues,
        "issues_closed": cumulative_closed_issues,
        "issues_closed_gitlab": closed_issues,
        "issues_total": (open_issues or 0) + (closed_issues or 0)
        if open_issues is not None and closed_issues is not None
        else None,
        "mrs_source": mrs_source,
        "mrs_open": open_mrs,
        "mrs_closed": closed_mrs,
        "prs_source": mrs_source,
        "prs_open": open_mrs if mrs_source == "gitlab" else gh_open_prs,
        "prs_closed": cumulative_closed_prs,
        "github_prs_open": gh_open_prs,
        "github_prs_closed": gh_closed_prs,
        "github_issues_open": gh_open_issues,
        "github_issues_closed": gh_closed_issues,
    }
    if lines_total is not None:
        payload["lines_of_code"] = lines_total
        payload["lines_per_repo"] = lines_per_repo


    out_dir.mkdir(parents=True, exist_ok=True)
    payload = merge_existing(payload, out_json)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {out_json} — LoC {payload.get('lines_of_code', lines_total)}, "
        f"gitlab projects {gitlab_projects}, issues ({issues_source}) open {open_issues}, "
        f"MRs ({mrs_source}) open {open_mrs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
