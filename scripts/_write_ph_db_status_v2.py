from pathlib import Path

Path(__file__).resolve().parent.parent.joinpath(
    "docs/ecosystem/ph-db-status.md"
).write_text(
    """# PH-DB / native Li sprint — status checklist

<!-- DOC-ecosystem-ph-db-status -->

**Snapshot:** 2026-05-30 (integration wave on `main`) · **Swarm row:** `ph-db` in [`lic` goal-directed snapshot](https://github.com/li-langverse/lic/blob/cursor/world-studio-master-plan-loop/data/goal-directed-agents/snapshot.json)

**Authority:** WP-N1…N9 in [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md); PH-DB-0…10 in [`proposals/lidb-li-data-platform.md`](../../proposals/lidb-li-data-platform.md).

---

## Integration milestones (on `main`)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| Native embed + `liorm.execute` | **Done** | `lidb` `main` @ `6d2632d` (PR #18/#21 family) |
| `lis db` native + registry rows | **Done** | `lis#24` merged → `main` @ `6f39026` |
| Registry P95 compare harness | **Done** | `benchmarks#202` merged → `main` @ `827254a` |
| Control-plane lidb persist | **Done** | `li-cursor-agents#42` merged → `main` @ `3016c4e` |
| WP-N3 realtime changefeed | **Done** | `lis#10` merged (prior wave) |
| `tier_db_security` harness | **Done** | `benchmarks#96` merged (prior wave) |
| **`lidb` default branch → `main`** | **Done** | 2026-05-30 — org default now `main` |
| Postgres P95 compare (honest ratio) | **Pending** | Nightly workflow on `benchmarks` `main`; needs first green run with `postgres:16` |
| Production `LI_CONTROL_PLANE_STORE=lidb` | **Pending** | Default in agents; **human sign-off** before prod |

---

## Swarm progress (6/13 todos)

| WP todo | Status |
|---------|--------|
| wp-a-engine-native | **completed** |
| wp-b-lis-db | **completed** |
| wp-c-registry-bench | **completed** |
| wp-e-control-plane | **completed** |
| wp-h0-default-main | **completed** |
| wp-n3-realtime | **completed** |
| wp-n5-security-bench | **completed** |
| wp-g-ci-cross-repo | pending (e2e on `main`; cross-repo matrix optional) |
| wp-h-containers | pending |
| wp-k-postgres-nightly | pending |
| wp-pr-merge-wave | **mostly done** (four feat PRs merged; roadmap docs PRs conflicted) |
| wp-d-registry-v2 | pending |
| wp-prod-lidb-default | pending |

**Verify:** `bash scripts/verify-ph-db-wsl.sh` (sibling repos)

---

## Top 3 remaining

1. **First green Postgres nightly** on merged `benchmarks` compare workflow (WP-K).
2. **Merge / refresh roadmap PH-DB docs PRs** (#32–#34 — currently conflicted with `main`).
3. **Production sign-off** for `LI_CONTROL_PLANE_STORE=lidb`.

---

## Related

- Swarm plan: `lic/docs/superpowers/plans/ph-db-swarm-plan.md` (branch `cursor/world-studio-master-plan-loop`)
- Execution tracker: `lic/docs/superpowers/plans/ph-db-execution-tracker.md`
""",
    encoding="utf-8",
)
print("wrote ph-db-status.md")
