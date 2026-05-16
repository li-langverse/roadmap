# Release notes: 2026-05-16 — development-overview-live

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** #2 (feat/development-overview)  
**PH / REQ:** N/A — governance / agent visibility  
**Author:** agent

---

## Summary (one sentence)

The published development overview on GitHub Pages now polls `status.json` for a live PR merge queue while keeping the markdown snapshot for branch CI and ecosystem tables.

## Agent continuation (required)

1. Read: `docs/development-overview.md`, `data/development-overview/status.json`, `scripts/refresh-development-overview.sh`.
2. Run: `./scripts/refresh-development-overview.sh && ./scripts/gen-development-overview.sh` after org PR changes; on `main`, the scheduled workflow commits JSON every 15 minutes.
3. Then: merge PR #2; enable GitHub Pages on `roadmap`; point `lic` `canvases/pr-merge-queue.canvas.tsx` at `https://li-langverse.github.io/roadmap/development-overview/`.
4. Blocked on: none (human merge + Pages env setup on first deploy).

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Live data | `scripts/refresh-development-overview.sh` + `.github/li-org-repos.txt` | `gh pr list` per repo → `data/development-overview/status.json` |
| Pages UI | `scripts/development-overview-live.js`, `gen-development-overview.sh` | `site/development-overview/live.js`, polls `status.json` every 60s |
| CI | `refresh-development-overview.yml` (cron */15), `pages.yml`, `ci.yml` | Refresh on main Pages build; CI dry-run refresh + build |

## Not changed (scope fence)

- `lic` `canvases/pr-merge-queue.canvas.tsx` — not in this repo; link manually after Pages URL is live.
- Markdown snapshot tables (branch CI, ecosystem) — still manual/agent edit of `docs/development-overview.md`.
- `benchmarks` dashboard ingest — separate repo; no catalog or `summary.json` changes.
- Agent-kit manifest version — unchanged.

## Breaking changes

None.

## Security

N/A — public org PR metadata via `GITHUB_TOKEN` / `gh`; no new secrets; same data as public GitHub UI.

## Performance

N/A — lightweight JSON (~8–20 PRs); 15-minute cron; client poll 60s. No compiler benchmarks.

## Downstream

| Repo | Action |
|------|--------|
| lic canvas | Add iframe or fetch to Pages URL / `status.json` |
| benchmarks | N/A |

## CHANGELOG entry (paste into Unreleased)

### Added

- Live PR merge queue on development overview Pages site (`status.json`, 15-minute refresh, 60s browser poll).
