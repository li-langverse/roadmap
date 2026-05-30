# Release notes: 2026-05-30 — development-overview-history

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**Author:** agent

---

## Summary (one sentence)

The development overview page now shows four SVG trend charts (open PRs, closed PRs, open issues, closed issues) from committed `history.json` snapshots plus live GitHub Search API points.

## Changed (specific)

| Area | What |
|------|------|
| Data | `data/development-overview/history.json` — seeded time series |
| Refresh | `refresh-development-overview.sh` appends a snapshot on each run |
| UI | `development-overview-history.js` — four inline SVG charts |
| Live | `development-overview-live.js` feeds live counts into charts |
| Pages | `gen-development-overview.sh` embeds history section; copies `history.json` |

## CHANGELOG entry (paste into Unreleased)

### Added

- Org activity history charts on the development overview (open/closed PRs and issues).
