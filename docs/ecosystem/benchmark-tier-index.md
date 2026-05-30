# Benchmark tier doc index

<!-- DOC-ecosystem-benchmark-tier-index -->

Pointers from **roadmap** to normative tier docs in [`li-langverse/benchmarks`](https://github.com/li-langverse/benchmarks). Perf claims must cite a row here + dashboard ingest.

**PH-DB sprint status (PRs, WP-N1…N9, deploy blockers):** [`ph-db-status.md`](ph-db-status.md) — refresh after native-li merge waves.

| Tier / suite | Doc | PH / trigger | Status on `main` |
|--------------|-----|--------------|------------------|
| Full suite runner | [`full-benchmark-suite.md`](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/full-benchmark-suite.md) | PH-5b | on `main` |
| HTTP RPS matrix | [`http-server-rps-matrix.md`](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/http-server-rps-matrix.md) | PH-H | on `main` |
| Plan cross-links | [`plan-cross-links.md`](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/plan-cross-links.md) | meta | on `main` |
| **`tier_db_registry`** | [`tier-db-registry-benchmark.md`](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/tier-db-registry-benchmark.md) | **PH-DB-4**, PH-DB-5 | **pending** — merge [benchmarks `feat/tier-db-registry`](https://github.com/li-langverse/benchmarks/tree/feat/tier-db-registry) (sibling PR) |
| tier_db_registry harness | [`benchmarks/tier_db_registry/README.md`](https://github.com/li-langverse/benchmarks/blob/feat/tier-db-registry/benchmarks/tier_db_registry/README.md) | PH-DB-1 bench prep | branch-only until merge |
| tier_db_registry schema | [`registry-v1.sql`](https://github.com/li-langverse/benchmarks/blob/feat/tier-db-registry/benchmarks/tier_db_registry/schema/registry-v1.sql) | PH-DB-1 | branch-only until merge |

**Agents:** After `feat/tier-db-registry` merges, replace branch URLs above with `main` paths only; update [`plan-cross-links.md`](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/plan-cross-links.md) in the same benchmarks PR or follow-up.
