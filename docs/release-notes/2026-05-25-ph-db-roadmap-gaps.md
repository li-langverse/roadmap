# Release notes: 2026-05-25 — ph-db-roadmap-gaps

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** feat/ph-db-roadmap-gaps  
**PH / REQ:** PH-DB-0, PKG-lidb, PH-8d-v2 → PH-DB-4  
**Author:** agent

---

## Summary

Closes roadmap traceability gaps for the Li data platform: **PKG-lidb** in official packages, PH-DB-0..10 table + **PH-8d-v2 → PH-DB-4** in ecosystem vision, bidirectional lidb proposal cross-links, and a benchmark tier doc index pointing at `tier_db_registry` (pending benchmarks merge).

## Agent continuation

1. Read: `docs/ecosystem/vision-and-roadmap.md` § PH-DB; `official-packages.md` PKG-lidb row; `benchmark-tier-index.md`
2. Run: none (governance docs only)
3. Then: merge benchmarks `feat/tier-db-registry` when ready; open lic master-plan PH-DB row PR; human creates `li-langverse/lidb` for PH-DB-1
4. Blocked on: human merge of governance PR; benchmarks tier PR separate

## Changed

| Area | What | Evidence |
|------|------|----------|
| Packages | `PKG-lidb` proposed row | `docs/ecosystem/official-packages.md` |
| PH tracker | PH-DB-0..10 + dependency edge | `docs/ecosystem/vision-and-roadmap.md`, `docs/roadmap/milestones.md` |
| Cross-links | ADR ↔ research ↔ bench index | `proposals/lidb-*.md`, `benchmark-tier-index.md` |
| CHANGELOG | Unreleased Added | `CHANGELOG.md` |

## Not changed

- **lic master plan** — PH-DB row deferred to sibling lic PR (roadmap table is canonical copy until then)
- **benchmarks repo** — `plan-cross-links.md` update lands with `feat/tier-db-registry` PR
- **`lidb` runtime** — no engine code

## Breaking changes

None.

## Security

N/A — documentation only.

## Performance

N/A — links to `tier_db_registry` bench doc (PH-DB-5 evidence path).

## Downstream

| Repo | Action |
|------|--------|
| **benchmarks** | Merge tier-db-registry PR; flip `benchmark-tier-index.md` URLs to `main` |
| **lic** | Add master plan PH-DB row + Future org repos `lidb` reminder |
| **lidb** (new) | Human creates repo; WP1 scaffold |

## CHANGELOG entry

Under `[Unreleased]` → Added: PH-DB roadmap gaps (PKG-lidb, vision PH table, bench tier index, proposal cross-links).
