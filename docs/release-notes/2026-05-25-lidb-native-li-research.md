# Release notes: 2026-05-25 — lidb-native-li-research

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PH / REQ:** PH-DB-0, PH-DB-3.1

---

## Summary

Adds competitor feature matrices, WP-N1…N9 scheduling, benchmark spectrum gates, and cross-links to the lidb native Li architecture ADR.

## Agent continuation

1. **Read:** `proposals/lidb-native-li-matrices.md`, `proposals/lidb-li-data-platform.md` (PH-DB-3.1 row), `../lidb/docs/architecture-native-li.md`
2. **Run:** none (docs-only)
3. **Then:** open/merge lidb PR for `architecture-native-li.md`; assign squads to WP-N1…N5 parallel
4. **Blocked on:** none for merge

## Changed

| Area | What | Evidence |
|------|------|----------|
| Matrices | 8 vertical tables + benchmark spectrum + WP-N diagram | `proposals/lidb-native-li-matrices.md` |
| Platform ADR | PH-DB-3.1, WP-N links | `proposals/lidb-li-data-platform.md` |
| Native engine | Cross-ref WP-N authority | `proposals/lidb-native-engine.md` |

## Not changed

- `lidb` engine C++ implementation — **lidb** repo PR
- `lic` master plan rows — sibling PR if needed
- Benchmarks harness CSV — WP-N4

## Breaking changes

None.

## Security

N/A — research docs; gates reference `lidb/tests/security/`.

## Performance

N/A — cites `tier_db_registry` thresholds only.

## Downstream

- **lidb:** `docs/architecture-native-li.md`
- **benchmarks:** WP-N4 tier spectrum ingest
