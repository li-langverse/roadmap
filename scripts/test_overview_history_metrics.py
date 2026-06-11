#!/usr/bin/env python3
"""Unit tests for cumulative development-overview metrics across VCS migration."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _overview_history_metrics import (  # noqa: E402
    apply_history_migration_offsets,
    cumulative_issues_closed,
    cumulative_prs_closed,
    history_point_metrics,
)


class OverviewHistoryMetricsTests(unittest.TestCase):
    def test_cumulative_prs_prefers_github_lifetime_total(self) -> None:
        self.assertEqual(
            cumulative_prs_closed(
                mrs_source="gitlab",
                github_closed=1653,
                gitlab_closed=6,
            ),
            1653,
        )

    def test_cumulative_prs_prefers_prs_closed_over_gitlab_only(self) -> None:
        self.assertEqual(
            cumulative_prs_closed(
                mrs_source="gitlab",
                github_closed=None,
                prs_closed=1653,
                gitlab_closed=6,
            ),
            1653,
        )

    def test_cumulative_issues_monotonic_across_sources(self) -> None:
        self.assertEqual(
            cumulative_issues_closed(
                issues_source="gitlab",
                github_closed=30,
                gitlab_closed=168,
            ),
            168,
        )
        self.assertEqual(
            cumulative_issues_closed(
                issues_source="gitlab",
                github_closed=200,
                gitlab_closed=168,
            ),
            200,
        )

    def test_history_point_metrics_from_gitlab_snapshot(self) -> None:
        eco = {
            "issues_source": "gitlab",
            "mrs_source": "gitlab",
            "issues_closed": 168,
            "mrs_closed": 6,
            "prs_closed": 6,
            "github_prs_closed": 1653,
            "github_issues_closed": 30,
        }
        metrics = history_point_metrics(eco)
        self.assertEqual(metrics["prs_closed"], 1653)
        self.assertEqual(metrics["issues_closed"], 168)

    def test_apply_history_migration_offsets_repairs_cliff(self) -> None:
        points = [
            {"at": "2026-06-07", "prs_closed": 1558, "issues_closed": 38},
            {"at": "2026-06-08", "prs_closed": 6, "issues_closed": 168},
        ]
        repaired = apply_history_migration_offsets(points)
        self.assertEqual(repaired[1]["prs_closed"], 1558)
        self.assertEqual(repaired[1]["issues_closed"], 168)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
