# Release notes: 2026-05-25 — ph-db-status

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** `feat/ph-db-status-doc`  
**PH / REQ:** PH-DB-0 (governance), REQ-registry-v2 (tracking)  
**Author:** agent

---

## Summary (one sentence)

Adds a single checklist doc for post–native-Li-sprint PH-DB work: PR merge state, WP-N1…N9 completion estimates, five human actions, and production registry deploy blockers.

## Agent continuation (required)

1. **Read:** `docs/ecosystem/ph-db-status.md`, `docs/ecosystem/benchmark-tier-index.md`
2. **Run:** `gh search prs --owner li-langverse --state open --limit 50 -- "head:feat/ph-db"` (refresh §1 tables)
3. **Then:** after `lidb` → `main` and `benchmarks` tier branch merge, update §2 percentages from exit gates only
4. **Blocked on:** human `lidb` default-branch rename — **do not** duplicate merge work in this PR

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Status doc | PR tables, WP-N %, blockers | `docs/ecosystem/ph-db-status.md` |
| Bench index | Link to status doc | `docs/ecosystem/benchmark-tier-index.md` |
| Snapshot | 2026-05-25 `gh` read-only queries | PR URLs in doc body |

## Not changed (scope fence)

- No merges in `lidb`, `lis`, `lip`, `benchmarks`, or `li-cursor-agents`
- WP-N implementation code — **not** in roadmap repo
- `benchmark-tier-index` branch URLs for `feat/tier-db-registry` — unchanged until benchmarks integration PR

## Breaking changes

None.

## Security

N/A — governance doc only; cites `lidb/tests/security/` as future gate, no harness changes.

## Performance

N/A — references `tier_db_registry` threshold; no bench runs in this PR.

## Downstream

| Repo | Action |
|------|--------|
| All PH-DB repos | Use `ph-db-status.md` as merge-queue hint; refresh after human actions §3 |

## CHANGELOG entry (paste into Unreleased)

- PH-DB status checklist: `docs/ecosystem/ph-db-status.md` ([2026-05-25-ph-db-status.md](2026-05-25-ph-db-status.md))
