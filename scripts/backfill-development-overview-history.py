#!/usr/bin/env python3
"""One-time backfill of daily org history from GitHub PR/issue timestamps."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ORG = "li-langverse"
METRIC_KEYS = (
    "open_prs",
    "ready_to_merge",
    "prs_closed",
    "issues_open",
    "issues_closed",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def gh_json(args: list[str]) -> list | dict | None:
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


def list_org_repos() -> list[str]:
    rows = gh_json(["repo", "list", ORG, "--limit", "10000", "--json", "name,isArchived"])
    if not isinstance(rows, list):
        return []
    return [r["name"] for r in rows if not r.get("isArchived")]


def gh_api_jsonl(endpoint: str, jq_filter: str) -> list[dict]:
    proc = subprocess.run(
        ["gh", "api", "--paginate", endpoint, "--jq", jq_filter],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "")
        return []
    rows: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def list_pulls(repo: str) -> list[dict]:
    endpoint = f"repos/{ORG}/{repo}/pulls?state=all&per_page=100"
    return gh_api_jsonl(
        endpoint,
        ".[] | {createdAt: .created_at, closedAt: .closed_at}",
    )


def list_issues_only(repo: str) -> list[dict]:
    endpoint = f"repos/{ORG}/{repo}/issues?state=all&per_page=100"
    rows = gh_api_jsonl(
        endpoint,
        ".[] | select(.pull_request == null) | {createdAt: .created_at, closedAt: .closed_at}",
    )
    return rows


def parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def day_range(start: date, end: date) -> list[date]:
    days: list[date] = []
    cur = start
    while cur <= end:
        days.append(cur)
        cur += timedelta(days=1)
    return days


def build_daily_series(
    pr_events: list[tuple[date, date | None]],
    issue_events: list[tuple[date, date | None]],
) -> list[dict]:
    pr_opens: dict[date, int] = defaultdict(int)
    pr_closes: dict[date, int] = defaultdict(int)
    issue_opens: dict[date, int] = defaultdict(int)
    issue_closes: dict[date, int] = defaultdict(int)

    all_days: list[date] = []
    today = datetime.now(timezone.utc).date()

    for created, closed in pr_events:
        if created:
            pr_opens[created] += 1
            all_days.append(created)
        if closed:
            pr_closes[closed] += 1
            all_days.append(closed)

    for created, closed in issue_events:
        if created:
            issue_opens[created] += 1
            all_days.append(created)
        if closed:
            issue_closes[closed] += 1
            all_days.append(closed)

    if not all_days:
        return []

    start = min(all_days)
    days = day_range(start, today)

    open_prs = 0
    open_issues = 0
    cum_prs_closed = 0
    cum_issues_closed = 0
    points: list[dict] = []

    for day in days:
        open_prs += pr_opens.get(day, 0) - pr_closes.get(day, 0)
        open_issues += issue_opens.get(day, 0) - issue_closes.get(day, 0)
        cum_prs_closed += pr_closes.get(day, 0)
        cum_issues_closed += issue_closes.get(day, 0)
        points.append(
            {
                "at": day.isoformat(),
                "open_prs": max(0, open_prs),
                "prs_closed": cum_prs_closed,
                "issues_open": max(0, open_issues),
                "issues_closed": cum_issues_closed,
                "source": "github-backfill",
            }
        )

    return points


def merge_daily(prev: dict | None, nxt: dict) -> dict:
    day = str(nxt.get("at", ""))[:10]
    out = {**(prev or {}), **nxt, "at": day}
    for key in METRIC_KEYS:
        if not isinstance(out.get(key), (int, float)) and isinstance(
            (prev or {}).get(key), (int, float)
        ):
            out[key] = prev[key]
    return out


def compact_daily(raw_points: list[dict]) -> list[dict]:
    by_day: dict[str, dict] = {}
    for p in sorted(raw_points, key=lambda x: str(x.get("at", ""))):
        day = str(p.get("at", ""))[:10]
        if not day:
            continue
        by_day[day] = merge_daily(by_day.get(day), p)
    return [by_day[d] for d in sorted(by_day.keys())]


def load_history_file(path: Path) -> dict:
    if not path.is_file():
        return {"version": 1, "org": ORG, "points": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"version": 1, "org": ORG, "points": []}
    except json.JSONDecodeError:
        return {"version": 1, "org": ORG, "points": []}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root() / "data" / "development-overview" / "history.json",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge into existing history.json instead of replacing",
    )
    parser.add_argument(
        "--since",
        metavar="YYYY-MM-DD",
        help="When merging, only add/update days on or after this date",
    )
    args = parser.parse_args()

    if subprocess.run(["gh", "--version"], capture_output=True).returncode != 0:
        sys.stderr.write("error: gh CLI required\n")
        return 1

    repos = list_org_repos()
    if not repos:
        sys.stderr.write("error: no org repos from gh\n")
        return 1

    pr_events: list[tuple[date, date | None]] = []
    issue_events: list[tuple[date, date | None]] = []

    for i, repo in enumerate(repos, 1):
        prs = list_pulls(repo)
        issues = list_issues_only(repo)
        for row in prs:
            pr_events.append((parse_day(row.get("createdAt")), parse_day(row.get("closedAt"))))
        for row in issues:
            issue_events.append(
                (parse_day(row.get("createdAt")), parse_day(row.get("closedAt")))
            )
        print(
            f"  [{i}/{len(repos)}] {repo}: {len(prs)} prs, {len(issues)} issues",
            file=sys.stderr,
        )

    points = build_daily_series(pr_events, issue_events)
    new_by_day = {str(p["at"])[:10]: p for p in points}

    if args.merge:
        payload = load_history_file(args.output)
        old_points = payload.get("points") if isinstance(payload.get("points"), list) else []
        by_day = {str(p.get("at", ""))[:10]: p for p in old_points if p.get("at")}
        since = args.since
        for day, p in new_by_day.items():
            if since and day < since:
                continue
            by_day[day] = merge_daily(by_day.get(day), p)
        merged = [by_day[d] for d in sorted(by_day.keys())]
        payload["points"] = compact_daily(merged)
        payload["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        payload["backfill"] = {
            "repos": len(repos),
            "prs_total": len(pr_events),
            "issues_total": len(issue_events),
            "days": len(merged),
            "merged": True,
            "since": since,
        }
    else:
        payload = {
            "version": 1,
            "org": ORG,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
            "backfill": {
                "repos": len(repos),
                "prs_total": len(pr_events),
                "issues_total": len(issue_events),
                "days": len(points),
            },
            "points": compact_daily(points),
        }

    print(
        f"Built {len(points)} daily points "
        f"({len(pr_events)} PRs, {len(issue_events)} issues across {len(repos)} repos)",
        file=sys.stderr,
    )

    if args.dry_run:
        if points:
            print(json.dumps(points[0], indent=2))
            print("...")
            print(json.dumps(points[-1], indent=2))
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
