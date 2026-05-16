# Release notes: 2026-05-16 — cursor-automation-overview-maintainer

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (this branch)  
**PH / REQ:** N/A — agent ops  
**Author:** agent

---

## Summary (one sentence)

Adds Cursor Automation prompt and `ecosystem-health-check.sh` so cloud agents maintain the development overview (failed PRs, missing CI, docs) without Actions cron.

## Agent continuation (required)

1. Read: `.cursor/automations/README.md`, paste `development-overview-maintainer.md` at cursor.com/automations (12h schedule).
2. Run: `./scripts/ecosystem-health-check.sh` locally to verify `gh` + refresh script.
3. Then: enable automation; human merges PRs the agent opens.
4. Blocked on: none.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Automations | `.cursor/automations/development-overview-maintainer.md` | Prompt for cursor.com/automations |
| Script | `scripts/ecosystem-health-check.sh` | Agent health report |
| Docs | `AGENTS.md` | Links overview URL + automation |

## Not changed (scope fence)

- `development-overview-live.js` — still public API only
- `benchmarks` repo automations — unchanged
- lic compiler / bench performance — not in this PR

## Breaking changes

None.

## Security

N/A — prompts forbid embedding tokens in client JS; `gh` uses runner/agent credentials only.

## Performance

N/A.

## Downstream

| Repo | Action |
|------|--------|
| User | Create automation in Cursor UI from README |

## CHANGELOG entry

### Added

- Cursor Automation templates for development overview maintainer (`.cursor/automations/`).
