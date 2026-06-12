#!/usr/bin/env python3
"""Regenerate docs/development-overview.md from committed GitLab status.json."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/development-overview/status.json"
ECO = ROOT / "data/development-overview/ecosystem-stats.json"
OUT_MD = ROOT / "docs/development-overview.md"


def main() -> int:
    if not STATUS.is_file():
        print(f"skip: missing {STATUS}", file=sys.stderr)
        return 0

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    ecosystem = status.get("ecosystem") or {}
    if ECO.is_file():
        try:
            ecosystem = {**ecosystem, **json.loads(ECO.read_text(encoding="utf-8"))}
        except json.JSONDecodeError:
            pass

    scanned = status.get("generated_at") or datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%MZ"
    )
    vcs = status.get("vcs_source", "gitlab")
    pull_requests = status.get("pull_requests") or status.get("merge_requests") or []
    metrics = status.get("metrics") or {}

    ready = int(metrics.get("ready_to_merge") or sum(1 for p in pull_requests if p.get("ready")))
    open_count = int(metrics.get("open_prs") or len(pull_requests))
    blocked = int(
        metrics.get("blocked")
        or sum(
            1
            for p in pull_requests
            if not p.get("ready") and (p.get("ci") in ("fail", "pending") or p.get("draft"))
        )
    )
    issues_open = ecosystem.get("issues_open")
    live_docs = metrics.get("repos_with_live_docs")

    merge_ready = [p for p in pull_requests if p.get("ready")]
    merge_blocked = [p for p in pull_requests if not p.get("ready") and p.get("ci") == "fail"]

    lines: list[str] = [
        "# Li development overview",
        "",
        f"**li-langverse org** · scanned **{scanned}** · {vcs} snapshot · live queue via status.json",
        "",
        "| Metric | Value |",
        "|--------|------:|",
    ]
    if issues_open is not None:
        lines.append(f"| Open issues (GitLab) | {issues_open} |")
    lines.extend(
        [
            f"| Ready to merge (CI green) | {ready} |",
            f"| Open MRs / PRs | {open_count} |",
            f"| Blocked / needs work | {blocked} |",
        ]
    )
    if live_docs is not None:
        repos_total = metrics.get("repos_total") or ecosystem.get("org_repositories") or "—"
        lines.append(f"| Repos with live docs | {live_docs} / {repos_total} |")

    lines.extend(["", "## Recommended merge order", ""])
    if merge_ready:
        for i, p in enumerate(merge_ready[:12], 1):
            title = str(p.get("title", ""))[:72]
            lines.append(
                f"{i}. [{p.get('repo')} #{p.get('number')}]({p.get('url')}) — {title}"
            )
    else:
        lines.append("_No MRs with green CI and non-draft status._")

    lines.extend(
        [
            "",
            "## Merge when reviewed",
            "",
            "| Priority | MR/PR | CI | Action | Notes |",
            "|----------|-------|-----|--------|-------|",
        ]
    )
    for p in merge_ready[:20]:
        lines.append(
            f"| P0 | [{p.get('repo')}#{p.get('number')}]({p.get('url')}) | {p.get('ci')} | Merge when approved | snapshot {scanned} |"
        )
    if not merge_ready:
        lines.append("| — | — | — | — | No green MRs |")

    lines.extend(
        [
            "",
            "## Do not merge yet",
            "",
            "| MR/PR | CI | Action | Notes |",
            "|-------|-----|--------|-------|",
        ]
    )
    for p in merge_blocked[:20]:
        title = str(p.get("title", ""))[:60]
        lines.append(
            f"| [{p.get('repo')}#{p.get('number')}]({p.get('url')}) | {p.get('ci')} | Fix CI first | {title} |"
        )
    if not merge_blocked:
        lines.append("| — | — | — | No failing open MRs |")

    lines.extend(
        [
            "",
            "## All open MRs / PRs",
            "",
            "| Repo | # | Title | Base | CI | Ready |",
            "|------|---|-------|------|-----|-------|",
        ]
    )
    for p in pull_requests[:120]:
        title = str(p.get("title", ""))
        if len(title) > 70:
            title = title[:70] + "…"
        lines.append(
            f"| {p.get('repo')} | {p.get('number')} | [{title}]({p.get('url')}) | {p.get('base', 'main')} | {p.get('ci')} | {'yes' if p.get('ready') else 'no'} |"
        )
    if len(pull_requests) > 120:
        lines.append(f"| … | … | _{len(pull_requests) - 120} more in status.json_ | … | … | … |")

    lines.extend(
        [
            "",
            "---",
            "",
            "*Agents do not merge governance MRs without owner sign-off. Never push directly to protected `main`.*",
            "",
            "*Snapshot regenerated from `data/development-overview/status.json`. Live queue polls the same file in the browser.*",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD} from status.json ({open_count} open, {ready} ready)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
