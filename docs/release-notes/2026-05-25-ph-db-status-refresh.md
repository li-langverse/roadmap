# Release notes: 2026-05-25 — ph-db-status refresh

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** `chore/ph-db-status-refresh`  
**PH / REQ:** PH-DB-0 (governance), REQ-registry-v2 (tracking)  
**Author:** agent

---

## Summary (one sentence)

Refreshes `ph-db-status.md` after the native-Li merge wave: marks `lis#10`, `benchmarks#96`, and `lidb`→`main` pending/done from `gh` state, bumps WP-N1…N9 %, and trims actions to top 3.

## Agent continuation (required)

1. **Read:** `docs/ecosystem/ph-db-status.md` § Integration milestones
2. **Run:** `gh repo view li-langverse/lidb --json defaultBranchRef`; `gh pr view 10 --repo li-langverse/lis`; `gh pr view 96 --repo li-langverse/benchmarks`
3. **Then:** after H0 branch rename + `lis#10` / `benchmarks#96` merge, refresh §2 exit-gate % only
4. **Blocked on:** human `lidb` default-branch rename — **do not** force-push `main`

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Status doc | Milestone table, WP-N %, top 3, blockers | `docs/ecosystem/ph-db-status.md` |
| Snapshot | Post-merge-wave `gh` queries 2026-05-25 | `lidb#12`–`#16`, `lip#17`, `benchmarks` `main` tree |

## Not changed (scope fence)

- No code merges in `lidb`, `lis`, `lip`, `benchmarks`, or `li-cursor-agents`
- WP-N implementation — **not** in roadmap repo
- `proposals/lidb-native-li-matrices.md` exit-gate definitions

## Breaking changes

None.

## Security

N/A — governance doc only; cites pending `benchmarks#96` harness wiring.

## Performance

N/A — references `tier_db_registry` on `benchmarks` `main`; no bench runs in this PR.

## Downstream

| Repo | Action |
|------|--------|
| Agents | Use §3 top 3 before opening duplicate N1/N2 PRs |
| Human | H0: rename `lidb` default branch to `main` |
