"""Cumulative org metrics across GitHub→GitLab migration for development overview."""

from __future__ import annotations

CUMULATIVE_KEYS = ("prs_closed", "issues_closed")


def cumulative_prs_closed(
    *,
    mrs_source: str,
    github_closed: int | None,
    prs_closed: int | None = None,
    gitlab_closed: int | None = None,
) -> int | None:
    """Lifetime closed PR/MR count. GitHub search retains full mirror history."""
    if github_closed is not None:
        return github_closed
    if prs_closed is not None:
        return prs_closed
    return gitlab_closed


def cumulative_issues_closed(
    *,
    issues_source: str,
    github_closed: int | None,
    gitlab_closed: int | None,
) -> int | None:
    """Lifetime closed issues — monotonic across GitHub freeze + GitLab-primary era."""
    if issues_source == "gitlab":
        candidates = [v for v in (github_closed, gitlab_closed) if isinstance(v, int)]
        return max(candidates) if candidates else None
    if github_closed is not None:
        return github_closed
    return gitlab_closed


def history_point_metrics(eco: dict) -> dict[str, int | None]:
    """Map ecosystem snapshot fields to cumulative history chart metrics."""
    issues_source = str(eco.get("issues_source") or eco.get("vcs_primary") or "")
    mrs_source = str(eco.get("mrs_source") or eco.get("prs_source") or issues_source)
    gitlab_issues_closed = eco.get("issues_closed")
    return {
        "prs_closed": cumulative_prs_closed(
            mrs_source=mrs_source,
            github_closed=eco.get("github_prs_closed"),
            prs_closed=eco.get("prs_closed"),
            gitlab_closed=eco.get("mrs_closed"),
        ),
        "issues_closed": cumulative_issues_closed(
            issues_source=issues_source,
            github_closed=eco.get("github_issues_closed"),
            gitlab_closed=gitlab_issues_closed,
        ),
    }


def apply_history_migration_offsets(points: list[dict]) -> list[dict]:
    """Repair discontinuities where GitLab-era snapshots reset cumulative counters."""
    if not points:
        return points

    repaired: list[dict] = []
    offsets = {key: 0 for key in CUMULATIVE_KEYS}

    for point in points:
        row = dict(point)
        for key in CUMULATIVE_KEYS:
            value = row.get(key)
            if not isinstance(value, (int, float)):
                continue
            prev = repaired[-1].get(key) if repaired else None
            if isinstance(prev, (int, float)) and value + offsets[key] < prev:
                offsets[key] = int(prev) - int(value)
            if offsets[key]:
                row[key] = int(value) + offsets[key]
        repaired.append(row)
    return repaired
