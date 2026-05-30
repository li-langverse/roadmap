# PH-DB / native Li sprint — status checklist

<!-- DOC-ecosystem-ph-db-status -->

**Snapshot:** 2026-05-30 (post native-embed integration wave) · **Swarm row:** `ph-db` in [`lic/data/goal-directed-agents/snapshot.json`](https://github.com/li-langverse/lic/blob/main/data/goal-directed-agents/snapshot.json) (4/13 todos done)

**Authority:** WP-N1…N9 in [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md); PH-DB-0…10 in [`proposals/lidb-li-data-platform.md`](../../proposals/lidb-li-data-platform.md); swarm todos in [`lic` ph-db-swarm-plan.md](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/ph-db-swarm-plan.md).

---

## Integration milestones (tracked items)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| Native embed + `liorm.execute` | **Done (branch)** | `lidb` `feat/ph-db-native-embed-wp-a` @ `fa88c18` — WSL smoke + parallel-race PASS |
| `lis db` native + registry rows | **Done (branch)** | `lis` `feat/ph-db-3-lis-db-native` @ `a8649cd` — `run_cli_stub.sh` PASS |
| Registry P95 harness | **Done (branch)** | `benchmarks` `feat/ph-db-5-registry-compare` — `tier_db_registry` lidb_only ~6–9ms P95 |
| Control-plane lidb persist | **Done (branch)** | `li-cursor-agents` `feat/ph-db-10-native-persist` — `test:e2e:lidb-engine` 10/10 WSL |
| [`lis#10`](https://github.com/li-langverse/lis/pull/10) WP-N3 realtime WS | **Pending** | PR open — not merged |
| [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96) `tier_db_security` | **Pending** | PR open — harness wiring not on `main` |
| **`lidb` default branch → `main`** | **Pending** | Still on integration branch family; use `lidb/scripts/set-default-branch-main.sh` |
| **PR merge (four feat/ph-db-* branches)** | **Pending** | Branches pushed; PRs need open + review |
| Postgres P95 compare (honest ratio) | **Pending** | Nightly workflow on benchmarks branch; needs merge + green run with `postgres:16` service |
| Production `LI_CONTROL_PLANE_STORE=lidb` | **Pending** | Default on branch; **human sign-off** before prod |

---

## Swarm progress (goal-directed canvas)

| WP todo | Status |
|---------|--------|
| wp-a-engine-native | **completed** |
| wp-b-lis-db | **completed** |
| wp-c-registry-bench | **completed** |
| wp-e-control-plane | **completed** |
| wp-g-ci-cross-repo | pending |
| wp-h-containers | pending |
| wp-k-postgres-nightly | pending |
| wp-pr-merge-wave | pending |
| wp-h0-default-main | pending |
| wp-n3-realtime | pending |
| wp-n5-security-bench | pending |
| wp-d-registry-v2 | pending |
| wp-prod-lidb-default | pending |

**Verify locally:** `bash scripts/verify-ph-db-wsl.sh` (workspace root with sibling repos)

---

## 1. Feature branches (merge queue)

| Repo | Branch | Tip | Ready for PR |
|------|--------|-----|--------------|
| `lidb` | `feat/ph-db-native-embed-wp-a` | `fa88c18` | Yes — engine + bench + JOIN |
| `lis` | `feat/ph-db-3-lis-db-native` | `a8649cd` | Yes — native db + compose |
| `benchmarks` | `feat/ph-db-5-registry-compare` | `ed2fa64` | Yes — compare manifest + nightly GHA |
| `li-cursor-agents` | `feat/ph-db-10-native-persist` | `6582bd6` | Yes — e2e + default lidb + CI job |

**Re-query:**

```bash
gh search prs --owner li-langverse --state open --limit 50 -- "feat/ph-db"
gh repo view li-langverse/lidb --json defaultBranchRef
```

---

## 2. WP-N1…N9 completion (%)

| WP | Title | % | Evidence / blocker |
|----|-------|---|-------------------|
| **N1** | Native heap + WAL | **75%** | Embed + WAL smoke green on branch; blocked on `main` + default branch rename |
| **N2** | SQL parser + executor | **70%** | JOIN + param SELECT on branch; registry queries work in WSL bench |
| **N3** | Realtime changefeed | **35%** | **Pending** [`lis#10`](https://github.com/li-langverse/lis/pull/10) |
| **N4** | Benchmark matrix CI | **92%** | `tier_db_registry` on branch with real lidb timings; merge + Postgres oracle pending |
| **N5** | Security / audit harness | **65%** | parallel-race PASS on branch; **pending** [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96) merge |
| **N6** | PG wire subset | **0%** | No PR; blocked on N1+N2 on `main` |
| **N7** | RLS + auth production | **50%** | RLS/JWT SQL merged historically; publisher auth not production |
| **N8** | Vector native | **25%** | G0 stubs on benchmarks `main`; no HNSW module PR |
| **N9** | Graph `lidb-graph` | **5%** | Research only |

**Integration gate PH-DB-3.1 (sqlite removal):** **70%** — native embed cutover on branch; blocked on merge to `main` + N3.

---

## 3. Top 3 remaining items

1. **Open + merge PRs** for the four `feat/ph-db-*` branches (engine, lis, benchmarks, agents).
2. **`lidb` default branch → `main`** — unblocks org CI badges and honest required checks (WP-H0).
3. **Merge [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96)** and **first green Postgres nightly** on merged compare workflow (WP-K).

---

## 4. Production registry deploy blockers

| Blocker | Type | Unblocks |
|---------|------|----------|
| Feature branches not on `main` | Merge | Org CI, agent-kit, honest tier status |
| `lis#10` not merged | Merge | N3 realtime exit gate |
| Postgres P95 ratio not measured in CI | CI | WP-K / Phase 3 |
| `LI_CONTROL_PLANE_STORE=lidb` prod flip | Human | Production cutover |

---

## Related

- Swarm plan todos: `lic/docs/superpowers/plans/ph-db-swarm-plan.md`
- Execution tracker (WP-A…K): `lic/docs/superpowers/plans/ph-db-execution-tracker.md`
- Battle plan: `lic/docs/superpowers/plans/ph-db-battle-plan.md`
