#!/usr/bin/env python3
"""Append today's ecosystem metrics to development-overview history (one point per UTC day)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
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


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def day_key(at: str) -> str:
    return str(at)[:10]


def merge_daily(prev: dict | None, nxt: dict) -> dict:
    day = day_key(str(nxt.get("at", "")))
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


def point_from_ecosystem(eco: dict, today: str, status: dict) -> dict:
    metrics = status.get("metrics") if isinstance(status.get("metrics"), dict) else {}
    open_prs = eco.get("prs_open")
    if open_prs is None and isinstance(metrics.get("open_prs"), int):
        open_prs = metrics["open_prs"]
    if open_prs is None:
        open_prs = search_total(f"org:{ORG}+is:pr+is:open")

    point = {
        "at": today,
        "open_prs": open_prs,
        "ready_to_merge": metrics.get("ready_to_merge"),
        "prs_closed": eco.get("prs_closed")
        if eco.get("prs_closed") is not None
        else search_total(f"org:{ORG}+is:pr+is:closed"),
        "issues_open": eco.get("issues_open")
        if eco.get("issues_open") is not None
        else search_total(f"org:{ORG}+is:issue+is:open"),
        "issues_closed": eco.get("issues_closed")
        if eco.get("issues_closed") is not None
        else search_total(f"org:{ORG}+is:issue+is:closed"),
        "source": "scheduled-4h",
    }
    return {k: v for k, v in point.items() if v is not None}


def main() -> int:
    overview = os.environ.get("GH_TOKEN_OVERVIEW_PAGE", "").strip()
    if overview:
        os.environ.setdefault("GH_TOKEN", overview)
        os.environ.setdefault("GITHUB_TOKEN", overview)

    root = repo_root()
    eco_path = root / "data" / "development-overview" / "ecosystem-stats.json"
    status_path = root / "data" / "development-overview" / "status.json"
    history_path = root / "data" / "development-overview" / "history.json"

    eco = load_json(eco_path)
    status = load_json(status_path)
    if not eco:
        sys.stderr.write(f"error: missing {eco_path} — run compute-ecosystem-stats.py first\n")
        return 1

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_point = point_from_ecosystem(eco, today, status)

    history = load_json(history_path) or {"version": 1, "org": ORG, "points": []}
    if not isinstance(history.get("points"), list):
        history["points"] = []

    points = compact_daily(list(history["points"]) + [new_point])
    if len(points) > 400:
        points = points[-400:]

    history["version"] = 1
    history["org"] = ORG
    history["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    history["points"] = points

    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {history_path} — {len(points)} days, today open_prs={new_point.get('open_prs')} "
        f"issues_open={new_point.get('issues_open')} prs_closed={new_point.get('prs_closed')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
