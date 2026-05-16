# Release notes: 2026-05-16 — development-overview-live

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** #2 (feat/development-overview)  
**PH / REQ:** N/A — governance / agent visibility  
**Author:** agent

---

## Summary (one sentence)

The published development overview uses **embedded JavaScript** to call the GitHub API from the browser for a live PR queue (no Actions cron). Markdown snapshot tables unchanged.

## Agent continuation (required)

1. Read: `docs/development-overview.md`, `scripts/development-overview-live.js`.
2. Run: `./scripts/gen-development-overview.sh` after editing the markdown snapshot; optional offline `refresh-development-overview.sh` for agents without a browser.
3. Then: merge PR #2; point `lic` canvas at `https://li-langverse.github.io/roadmap/development-overview/`.
4. Blocked on: none (human merge + Pages env on first deploy).

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Live UI | `scripts/development-overview-live.js` | GitHub Search API + staggered commit status (browser) |
| Pages | `gen-development-overview.sh` | Embeds `live.js`; no `status.json` required |
| CI | Removed `refresh-development-overview.yml` cron | `pages.yml` build-only on push |

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
