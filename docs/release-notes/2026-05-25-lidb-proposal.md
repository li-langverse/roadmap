# Release notes: 2026-05-25 — lidb-proposal

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (feat/ph-db-0-lidb-proposal)  
**PH / REQ:** PH-DB-0, REQ-registry-v2  
**Author:** agent

---

## Summary

Adds PH-DB-0 ADR `proposals/lidb-li-data-platform.md` — north star, lean `lidb`+`lis` Supabase-parity bundle, `liorm`+`liq`, phased PH-DB-0..10, packaging map, footprint targets, and registry-min path for central registry DB.

## Agent continuation

1. Read: `proposals/lidb-li-data-platform.md`; lic master plan PH-DB row; lip plan § 8d v2 note
2. Run: human creates `li-langverse/lidb` repo per governance checklist; then start **WP1** (`feat/ph-db-1-lidb-scaffold`)
3. Then: parallel **WP4-prep** (lip OpenAPI), **WP-bench** (`tier_db_registry`); sequenced **WP2** → **WP5** → **WP4**
4. Blocked on: human — org repo `lidb` creation, registry domain DNS/TLS (PH-DB-4)

## Changed

| Area | What | Evidence |
|------|------|----------|
| ADR | `proposals/lidb-li-data-platform.md` — full PH-DB program | PH-DB-0..10 table, mermaid, packaging map |
| Policy cross-link | lic master plan + lip 8d minimal edits (sibling PR or same wave) | `registry v2 DB → PH-DB-4` |
| CHANGELOG | Unreleased Added entry | `CHANGELOG.md` |

## Not changed

- **`lidb` runtime** — no engine code in this PR (WP1)
- **`lip` / `lit` / `lic` compiler** — no toolchain or proof surface changes
- **li-cursor-agents Supabase control plane** — PH-DB-10 only
- **Benchmarks tier execution** — WP-bench skeleton only

## Breaking changes

None — documentation and governance only.

## Security

N/A — proposal defines future `liorm`/`liq` exploit harness (PH-DB-2); no runtime yet.

## Performance

N/A — footprint targets documented (registry-min ≤256 MiB); evidence in WP1 `docs/footprint.md`.

## Downstream

| Repo | Action |
|------|--------|
| **lic** | Merge PH-DB cross-link PR; agents read master plan row before WP1 |
| **lidb** (new) | Scaffold after human creates repo (WP1) |
| **lip** | PH-DB-4 prep OpenAPI (WP4-prep, parallel) |
| **lis** | PH-DB-3 bundle stub (WP5, after WP1) |
| **benchmarks** | `tier_db_registry` skeleton (WP-bench, parallel) |

## CHANGELOG entry

```markdown
### Added
- PH-DB-0 ADR: Li data platform (`lidb` + `lis` bundle), phased PH-DB-0..10, registry-min path (PH-DB-0)
```
