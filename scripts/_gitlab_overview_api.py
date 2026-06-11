"""GitLab API helpers for development overview (issues, MRs, projects)."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

GITLAB_HOST = os.environ.get("LI_GITLAB_HOST", "gitlab.lilangverse.xyz").strip()
GITLAB_GROUP = os.environ.get("LI_GITLAB_GROUP", "li-langverse").strip()


def gitlab_token() -> str | None:
    token = os.environ.get("GITLAB_TOKEN", "").strip()
    return token or None


def gitlab_api_bases() -> list[str]:
    explicit = os.environ.get("GITLAB_API_URL", "").strip().rstrip("/")
    if explicit:
        return [explicit]
    scheme = os.environ.get("LI_GITLAB_SCHEME", "https").strip().lower()
    internal = os.environ.get("LI_GIT_INTERNAL_SVC", "").strip()
    bases: list[str] = []
    if internal and "lilangverse.xyz" in GITLAB_HOST:
        bases.append(f"http://{internal}")
    if scheme != "http":
        bases.append(f"https://{GITLAB_HOST}")
    if scheme == "http":
        bases.append(f"http://{GITLAB_HOST}")
    out: list[str] = []
    for base in bases:
        if base not in out:
            out.append(base)
    return out


def _gitlab_get(path: str, *, token: str) -> tuple[int, object, dict[str, str]]:
    headers = {
        "PRIVATE-TOKEN": token,
        "Accept": "application/json",
    }
    last: tuple[int, object, dict[str, str]] = (0, {"message": "no bases"}, {})
    for base in gitlab_api_bases():
        url = path if path.startswith("http") else f"{base}{path}"
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw = resp.read().decode()
                hdrs = {k: v for k, v in resp.headers.items()}
                ctype = (hdrs.get("Content-Type") or "").lower()
                if "text/html" in ctype:
                    raise ValueError("GitLab returned HTML")
                payload = json.loads(raw) if raw else None
                return resp.status, payload, hdrs
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
            last = (getattr(exc, "code", 0) or 0, {"message": str(exc)}, {})
    return last


def gitlab_header_total(path: str) -> int | None:
    token = gitlab_token()
    if not token:
        return None
    status, _payload, hdrs = _gitlab_get(path, token=token)
    if status != 200:
        return None
    total = hdrs.get("X-Total") or hdrs.get("x-total")
    if total is not None:
        try:
            return int(total)
        except ValueError:
            pass
    return _gitlab_paginate_count(path, token=token)


def _gitlab_paginate_count(path: str, *, token: str) -> int | None:
    sep = "&" if "?" in path else "?"
    page = 1
    total = 0
    while page <= 50:
        status, data, _ = _gitlab_get(f"{path}{sep}per_page=100&page={page}", token=token)
        if status != 200 or not isinstance(data, list):
            return total if total else None
        total += len(data)
        if len(data) < 100:
            return total
        page += 1
    return total


def gitlab_group_issue_counts() -> tuple[int | None, int | None]:
    group = urllib.parse.quote(GITLAB_GROUP, safe="")
    open_n = gitlab_header_total(
        f"/api/v4/groups/{group}/issues?state=opened&include_subgroups=true&scope=all"
    )
    closed_n = gitlab_header_total(
        f"/api/v4/groups/{group}/issues?state=closed&include_subgroups=true&scope=all"
    )
    return open_n, closed_n


def gitlab_group_mr_counts() -> tuple[int | None, int | None]:
    group = urllib.parse.quote(GITLAB_GROUP, safe="")
    open_n = gitlab_header_total(
        f"/api/v4/groups/{group}/merge_requests?state=opened&include_subgroups=true"
    )
    closed_n = gitlab_header_total(
        f"/api/v4/groups/{group}/merge_requests?state=closed&include_subgroups=true"
    )
    merged_n = gitlab_header_total(
        f"/api/v4/groups/{group}/merge_requests?state=merged&include_subgroups=true"
    )
    if closed_n is None and merged_n is not None:
        closed_n = merged_n
    elif closed_n is not None and merged_n is not None:
        closed_n = max(closed_n, merged_n)
    return open_n, closed_n


def gitlab_project_count() -> int | None:
    group = urllib.parse.quote(GITLAB_GROUP, safe="")
    return gitlab_header_total(
        f"/api/v4/groups/{group}/projects?include_subgroups=true&archived=false"
    )


def _repo_from_mr(mr: dict) -> str:
    ref = str(mr.get("references", {}).get("full", ""))
    if "!" in ref:
        return ref.split("!", 1)[0].rsplit("/", 1)[-1]
    web = str(mr.get("web_url", ""))
    m = re.search(r"/([^/]+)/-/merge_requests/", web)
    return m.group(1) if m else "unknown"


def classify_gl_mr(mr: dict) -> tuple[str, bool]:
    if mr.get("draft"):
        return "draft", False
    pipe = mr.get("head_pipeline") if isinstance(mr.get("head_pipeline"), dict) else {}
    status = str(pipe.get("status", "")).lower()
    if status == "success":
        return "pass", True
    if status in ("failed", "canceled", "cancelled"):
        return "fail", False
    if status in ("running", "pending", "created", "waiting_for_resource", "preparing"):
        return "pending", False
    merge_status = str(mr.get("detailed_merge_status", "")).lower()
    if merge_status in ("approvals_syncing", "checking", "ci_still_running", "not_approved"):
        return "pending", False
    if merge_status in ("mergeable", "not_open"):
        return "pass", not bool(mr.get("draft"))
    return "none", False


def fetch_gitlab_open_merge_requests(*, limit: int = 200) -> list[dict]:
    token = gitlab_token()
    if not token:
        return []
    group = urllib.parse.quote(GITLAB_GROUP, safe="")
    path = f"/api/v4/groups/{group}/merge_requests?state=opened&include_subgroups=true"
    out: list[dict] = []
    page = 1
    while len(out) < limit and page <= 20:
        status, data, _ = _gitlab_get(f"{path}&per_page=100&page={page}", token=token)
        if status != 200 or not isinstance(data, list):
            break
        for mr in data:
            if not isinstance(mr, dict):
                continue
            repo = _repo_from_mr(mr)
            ci, ready = classify_gl_mr(mr)
            out.append(
                {
                    "repo": repo,
                    "number": int(mr.get("iid", 0)),
                    "title": str(mr.get("title", "")),
                    "url": str(mr.get("web_url", "")),
                    "base": str(mr.get("target_branch", "main")),
                    "draft": bool(mr.get("draft")),
                    "ci": ci,
                    "ready": ready,
                    "source": "gitlab",
                }
            )
            if len(out) >= limit:
                break
        if len(data) < 100:
            break
        page += 1
    out.sort(key=lambda r: (r["repo"], r["number"]))
    return out
