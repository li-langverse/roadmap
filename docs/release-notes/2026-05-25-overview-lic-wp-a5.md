# Release notes: 2026-05-25 — overview-lic-wp-a5

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (branch `docs/overview-lic-wp-a5`)  
**PH / REQ:** Org hygiene WP-A5  
**Author:** agent

---

## Summary (one sentence)

Ecosystem docs now point agents and contributors to **`lic`** as the canonical compiler repo; **`li-language`** is called out as deprecated with a pointer to WP-B3 for archive redirect.

## Agent continuation (required)

1. Read: `docs/ecosystem/overview.md`, `governance.md`, `agent-coordination.md`; org plan WP-B3 in `li-cursor-agents/docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md`.
2. Run: `rg -n 'li-language' roadmap benchmarks --glob '*.md'` — expect only deprecation notes and historical tables (e.g. `development-overview.md`).
3. Then: WP-B3 — add archive redirect to `li-language` README (human may archive repo).
4. Blocked on: none for this PR.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ecosystem overview | Primary language link → `lic`; deprecation callout; `LI_REPO=../lic` in lip bootstrap | `docs/ecosystem/overview.md` |
| Governance | Language + compiler row → `lic`; traceability example `PKG-lic` | `docs/ecosystem/governance.md` |
| Agent coordination | GitHub CLI example `cd lic` | `docs/ecosystem/agent-coordination.md` |

## Not changed (scope fence)

- **`li-language` repo README** — WP-B3 (Phase 2), not this PR
- **`docs/development-overview.md`** — still lists historical `li-language` PR/CI matrix for audit; separate maintainer pass
- **Benchmarks** ingest scripts, tier registry, agent-kit manifest — no edits
- **`lic` compiler code**, `lip`/`lit` implementation — docs-only

## Breaking changes

None — documentation link targets only; no API or toolchain contract change.

## Security

N/A — no security surface touched.

## Performance

N/A — no benchmarks or CI runtime changes.

## Downstream

| Repo | Action |
|------|--------|
| lip / lit / packages | N/A — agents should clone `lic` per updated overview; existing `LI_REPO` env var name unchanged |
| li-language | WP-B3: README archive notice after this merges |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Changed
- Ecosystem docs: compiler canonical repo is `lic` (deprecated `li-language` noted) — [2026-05-25-overview-lic-wp-a5.md](docs/release-notes/2026-05-25-overview-lic-wp-a5.md) (WP-A5)
```
