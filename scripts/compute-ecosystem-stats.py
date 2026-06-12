#!/usr/bin/env python3
"""Compute li-langverse ecosystem stats (lines of Li, org repo count) for the development overview."""
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
    gitlab_project_paths,
    gitlab_token,
)
from _overview_history_metrics import cumulative_issues_closed, cumulative_prs_closed

ORG = "li-langverse"
LI_SOURCE_SUFFIXES = {".li"}
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


def list_github_repo_names() -> list[str] | None:
    data = gh_json(["repo", "list", ORG, "--limit", "10000", "--json", "name"])
    if not isinstance(data, list):
        return None
    names = sorted({str(row.get("name", "")).strip() for row in data if row.get("name")})
    return names or None


def count_org_repositories() -> int | None:
    """All repositories visible to `gh` under the org (public + private for the token)."""
    names = list_github_repo_names()
    if names is not None:
        return len(names)
    return count_org_repositories_via_token()


def count_org_repositories_via_token() -> int | None:
    """Fallback when `gh repo list` fails: paginate org repos with GITHUB_TOKEN (e.g. Actions)."""
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


def list_org_repo_names(root: Path) -> list[str]:
    """Union GitHub org repos and GitLab group projects (GitLab-primary census)."""
    names: set[str] = set()
    gh_names = list_github_repo_names()
    if gh_names:
        names.update(gh_names)
    gl_names = gitlab_project_paths()
    if gl_names:
        names.update(gl_names)
    if not names:
        repos_file = root / ".github" / "li-org-repos.txt"
        if repos_file.is_file():
            names.update(load_repo_list(repos_file))
    return sorted(names)


def count_li_lines(repo_path: Path) -> int:
    """Count physical lines in `.li` source files only."""
    total = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not d.startswith(".")]
        for name in files:
            if Path(name).suffix.lower() not in LI_SOURCE_SUFFIXES:
                continue
            fp = Path(root) / name
            try:
                with fp.open("rb") as fh:
                    total += sum(1 for _ in fh)
            except OSError:
                pass
    return total


def clone_repo_github(name: str, dest: Path) -> bool:
    slug = f"{ORG}/{name}"
    proc = subprocess.run(
        ["gh", "repo", "clone", slug, str(dest / name), "--", "--depth", "1"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and (dest / name).is_dir()


def clone_repo_gitlab(name: str, dest: Path) -> bool:
    """Clone from GitLab — anonymous HTTPS first, then token if the project is private."""
    target = dest / name
    public_url = f"https://{GITLAB_HOST}/{GITLAB_GROUP}/{name}.git"
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", public_url, str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0 and target.is_dir():
        return True
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)

    token = gitlab_token()
    if not token:
        return False
    auth_url = f"https://oauth2:{token}@{GITLAB_HOST}/{GITLAB_GROUP}/{name}.git"
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", auth_url, str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and target.is_dir()


def clone_repo(name: str, dest: Path) -> bool:
    if clone_repo_github(name, dest):
        return True
    return clone_repo_gitlab(name, dest)


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


def compute_lines_of_li(
    repos: list[str], workdir: Path, clone_missing: bool
) -> tuple[int, dict[str, int], int]:
    per_repo: dict[str, int] = {}
    missing = 0
    tmp_clone: Path | None = None
    if clone_missing:
        tmp_clone = Path(tempfile.mkdtemp(prefix="li-ecosystem-loc-"))
    try:
        for name in repos:
            local = resolve_local_clone(name, repo_root())
            if local is not None:
                per_repo[name] = count_li_lines(local)
                continue
            if tmp_clone is None:
                per_repo[name] = 0
                missing += 1
                continue
            if clone_repo(name, tmp_clone):
                per_repo[name] = count_li_lines(tmp_clone / name)
            else:
                per_repo[name] = 0
                missing += 1
    finally:
        if tmp_clone is not None:
            shutil.rmtree(tmp_clone, ignore_errors=True)
    return sum(per_repo.values()), per_repo, missing


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
    new_loc = payload.get("lines_of_li")
    if new_loc is not None and new_loc > 0:
        # Fresh `.li` census from this run — never substitute legacy mixed-language totals.
        pass
    else:
        existing_loc = existing.get("lines_of_li")
        if existing_loc is None and existing.get("loc_metric") != "lines_of_li":
            existing_loc = existing.get("lines_of_code")
        existing_loc = existing_loc or 0
        if existing_loc and (new_loc == 0 or new_loc is None):
            payload["lines_of_li"] = existing_loc
            payload["lines_per_repo"] = existing.get("lines_per_repo", {})
            payload["repos_loc_missing"] = existing.get("repos_loc_missing")
        elif existing_loc and new_loc is not None and new_loc < existing_loc * 0.75:
            payload["lines_of_li"] = existing_loc
            payload["lines_per_repo"] = existing.get("lines_per_repo", {})
            payload["repos_loc_missing"] = existing.get("repos_loc_missing")
    if payload.get("org_swarm") is None and existing.get("org_swarm"):
        payload["org_swarm"] = existing["org_swarm"]
    return payload


def main() -> int:
    overview = os.environ.get("GH_TOKEN_OVERVIEW_PAGE", "").strip()
    if overview:
        os.environ.setdefault("GH_TOKEN", overview)
        os.environ.setdefault("GITHUB_TOKEN", overview)

    root = repo_root()
    out_dir = root / "data" / "development-overview"
    out_json = out_dir / "ecosystem-stats.json"

    if shutil.which("gh") is None:
        sys.stderr.write("error: gh CLI required\n")
        return 1

    repos = list_org_repo_names(root)
    skip_clone = os.environ.get("ECOSYSTEM_STATS_SKIP_CLONE", "") == "1"
    clone_missing = not skip_clone

    lines_total: int | None = None
    lines_per_repo: dict[str, int] | None = None
    repos_loc_missing: int | None = None
    if skip_clone:
        # Pages/CI only checks out roadmap — LoC needs shallow clones of all org repos.
        pass
    else:
        lines_total, lines_per_repo, repos_loc_missing = compute_lines_of_li(
            repos, root, clone_missing
        )

    org_repositories = count_org_repositories()
    open_issues, closed_issues, issues_source = issue_counts()
    open_mrs, closed_mrs, mrs_source = mr_counts()
    gitlab_projects = gitlab_project_count() if gitlab_token() else None

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
        "repos_loc_tracked": len(repos),
        "repos_loc_missing": repos_loc_missing,
        "loc_metric": "lines_of_li",
        "loc_file_types": sorted(LI_SOURCE_SUFFIXES),
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
        payload["lines_of_li"] = lines_total
        payload["lines_per_repo"] = lines_per_repo

    out_dir.mkdir(parents=True, exist_ok=True)
    payload = merge_existing(payload, out_json)
    payload.pop("lines_of_code", None)
    payload.pop("repos_tracked", None)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {out_json} — lines of Li {payload.get('lines_of_li', lines_total)} "
        f"({payload.get('repos_loc_tracked', len(repos))} repos, "
        f"missing {payload.get('repos_loc_missing', repos_loc_missing)}), "
        f"gitlab projects {gitlab_projects}, issues ({issues_source}) open {open_issues}, "
        f"MRs ({mrs_source}) open {open_mrs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
