# Release notes: 2026-05-25 — lidb-native-plan

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** feat/lidb-native-plan  
**PH / REQ:** PH-DB-1, PH-DB-7, REQ-registry-v2  
**Author:** agent

---

## Summary

Adds PH-DB native engine ADR (`proposals/lidb-native-engine.md`): deprecate sqlite smoke, native C++/Li WAL/pages + SQL executor, realtime in `lis` bundle, and N1–N6 parallel/sequential work packages.

## Agent continuation

1. Read: `proposals/lidb-native-engine.md`, `proposals/lidb-li-data-platform.md`, `lidb/docs/pg-subset-v1.md` (sibling PR on lidb)
2. Run: pick parallel WP — **N2** (WAL/pages), **N3** (SQL executor), or **N5** (realtime protocol) in `lidb`/`lis`
3. Then: integrator **N4** after N2+N3 green; **N6** after N5 + PH-DB-5 RLS
4. Blocked on: none for N1–N3/N5 starts; N4 on N2+N3; N6 on N5

## Changed

| Area | What | Evidence |
|------|------|----------|
| ADR | `proposals/lidb-native-engine.md` — N1–N6 WPs, sqlite REMOVED, migration | WP table + mermaid |
| ADR | `proposals/lidb-li-data-platform.md` — cross-links, PH-DB-1/7 rows, Learned from | Parent doc |
| Release note | This file | PH-DB-1 revision |

## Not changed

- **`lidb` engine code** — documentation/plan only (implementation in N2–N4 PRs)
- **`lis` runtime** — N5/N6 protocol stubs land in lis repo
- **lic master plan** — cross-link optional follow-up PR
- **Benchmarks tier execution** — still skeleton until N4

## Breaking changes

None in roadmap repo. **Future breaking (lidb N4):** sqlite smoke removal; devs must reset `LI_DATA_DIR` per migration path in `pg-subset-v1.md`.

## Security

N/A — plan only. N6 documents RLS-filtered realtime channels (PH-DB-5 + PH-DB-7).

## Performance

N/A — native engine enables `tier_db_registry` after N4; not run in this PR.

## Downstream

| Repo | Action |
|------|--------|
| **lidb** | Merge `pg-subset-v1.md` update; start N2/N3 branches |
| **lis** | N5 realtime broker scaffold |
| **lic** | Optional master-plan PH-DB-1 row tweak |

## CHANGELOG entry

```markdown
### Added
- PH-DB native engine ADR (`proposals/lidb-native-engine.md`): sqlite deprecation, N1–N6 work packages, realtime in `lis` bundle
```
