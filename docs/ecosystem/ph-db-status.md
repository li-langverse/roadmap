# PH-DB / native Li sprint — status checklist

<!-- DOC-ecosystem-ph-db-status -->

**Snapshot:** 2026-05-25 (UTC) · **Query:** read-only `gh search prs` / `gh pr list` for `head:feat/ph-db*`, `head:feat/lidb*`, `head:feat/tier-db*` across `li-langverse/*`. Re-run before merge decisions.

**Authority:** WP-N1…N9 scheduling in [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md); PH-DB-0…10 in [`proposals/lidb-li-data-platform.md`](../../proposals/lidb-li-data-platform.md).

---

## 1. PRs — merged vs open (branch family)

| State | Count (approx.) | Notes |
|-------|-----------------|-------|
| **Merged** | **22+** | Scaffold + stubs landed; not production registry |
| **Open** | **14** | Native engine + E2E + docs; review queue |
| **Closed unmerged** | 3 | Superseded stacks (`lis` #7–8, `li-cursor-agents` #16) |

### Merged (representative — do not re-implement)

| Repo | PR | Title |
|------|-----|-------|
| `roadmap` | [#14](https://github.com/li-langverse/roadmap/pull/14) | PH-DB-0 lidb data platform ADR |
| `roadmap` | [#15](https://github.com/li-langverse/roadmap/pull/15) | PH-DB ecosystem gaps (PKG-lidb, bench index) |
| `lidb` | [#1](https://github.com/li-langverse/lidb/pull/1)–[#5](https://github.com/li-langverse/lidb/pull/5) | PH-DB-1..2 scaffold, liorm/liq, PH-DB-3 wire, PH-DB-5 RLS SQL |
| `lis` | [#5](https://github.com/li-langverse/lis/pull/5)–[#9](https://github.com/li-langverse/lis/pull/9) | PH-DB-3 `lis db` stub; PH-DB-4 registry routes → lidb |
| `lip` | [#13](https://github.com/li-langverse/lip/pull/13)–[#16](https://github.com/li-langverse/lip/pull/16), [#18](https://github.com/li-langverse/lip/pull/18) | OpenAPI prep, publish client, cross-repo E2E script |
| `lic` | [#275](https://github.com/li-langverse/lic/pull/275) | Master plan PH-DB cross-link |
| `li-cursor-agents` | [#17](https://github.com/li-langverse/li-cursor-agents/pull/17) | PH-DB-2/10 liq MCP stub |
| `benchmarks` | [#72](https://github.com/li-langverse/benchmarks/pull/72), [#74](https://github.com/li-langverse/benchmarks/pull/74), [#88](https://github.com/li-langverse/benchmarks/pull/88), [#89](https://github.com/li-langverse/benchmarks/pull/89) | `tier_db_registry` skeleton, G0 graph/vector stubs, WP-N4 spectrum + token efficiency |

### Open (merge order hint: docs → N1/N2 → N5 → N3/lis → E2E)

| Repo | PR | Branch / WP |
|------|-----|-------------|
| `lidb` | [#6](https://github.com/li-langverse/lidb/pull/6) | agent-kit 1.3.3 |
| `lidb` | [#7](https://github.com/li-langverse/lidb/pull/7) | learned-from (N1 docs) |
| `lidb` | [#8](https://github.com/li-langverse/lidb/pull/8) | PH-DB-3.1 architecture ADR |
| `lidb` | [#9](https://github.com/li-langverse/lidb/pull/9) | **WP-N5** security/audit harness |
| `lidb` | [#10](https://github.com/li-langverse/lidb/pull/10) | liq token audit |
| `lidb` | [#11](https://github.com/li-langverse/lidb/pull/11) | **WP-N3** changefeed API |
| `lidb` | [#12](https://github.com/li-langverse/lidb/pull/12) | **WP-N2** native SQL |
| `lidb` | [#13](https://github.com/li-langverse/lidb/pull/13) | **WP-N1** heap + WAL |
| `lis` | [#10](https://github.com/li-langverse/lis/pull/10) | **WP-N3** realtime WS |
| `lip` | [#17](https://github.com/li-langverse/lip/pull/17) | PH-DB-4 publish → registry E2E |
| `lip` | [#19](https://github.com/li-langverse/lip/pull/19) | stack-full + realtime probe |
| `roadmap` | [#17](https://github.com/li-langverse/roadmap/pull/17) | native engine plan (N1–N6) |
| `li-cursor-agents` | [#19](https://github.com/li-langverse/li-cursor-agents/pull/19) | PH-DB-10 checkbox audit |
| `li-cursor-agents` | [#20](https://github.com/li-langverse/li-cursor-agents/pull/20) | PH-DB-10 ControlPlaneStore stub |

**Re-query:**

```bash
gh search prs --owner li-langverse --state open --limit 50 -- "head:feat/ph-db"
gh search prs --owner li-langverse --state open --limit 50 -- "head:feat/lidb"
gh search prs --owner li-langverse --merged --limit 50 -- "head:feat/tier-db"
```

---

## 2. WP-N1…N9 completion (%)

Exit gates from [`lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md). Percent = **engineering judgment** from PR state + branch artifacts (not automated).

| WP | Title | % | Evidence / blocker |
|----|-------|---|-------------------|
| **N1** | Native heap + WAL | **15%** | Open [`lidb#13`](https://github.com/li-langverse/lidb/pull/13); sqlite smoke still default on integration branch |
| **N2** | SQL parser + executor | **20%** | Open [`lidb#12`](https://github.com/li-langverse/lidb/pull/12); merged liorm stubs use embed/sqlite path |
| **N3** | Realtime changefeed | **25%** | Open [`lidb#11`](https://github.com/li-langverse/lidb/pull/11), [`lis#10`](https://github.com/li-langverse/lis/pull/10) |
| **N4** | Benchmark matrix CI | **70%** | Merged benchmarks #72/#88/#89 on **`feat/tier-db-registry`**; **not** on `benchmarks` `main` yet |
| **N5** | Security / audit harness | **45%** | Stubs merged (`lidb#1`); expansion in open [`lidb#9`](https://github.com/li-langverse/lidb/pull/9) |
| **N6** | PG wire subset | **0%** | No open PR; blocked on N1+N2 + PH-DB-3.1 cutover |
| **N7** | RLS + auth production | **50%** | RLS/JWT SQL merged [`lidb#2`](https://github.com/li-langverse/lidb/pull/2); publisher auth path not production |
| **N8** | Vector native | **10%** | G0 bench stubs [`benchmarks#74`](https://github.com/li-langverse/benchmarks/pull/74); no `lidb` HNSW module PR |
| **N9** | Graph `lidb-graph` | **5%** | Research only (PH-DB-G0); no module PR |

**Integration gate PH-DB-3.1 (sqlite removal):** **0%** shipped — target cutover per [`lidb-native-engine.md`](../../proposals/lidb-native-engine.md) after **N1+N2** green.

**Batch A parallel (N1–N5):** ~**31%** mean · **Sequential tail (N6–N9):** ~**16%** mean.

---

## 3. Next 5 human actions

1. **Rename `lidb` default branch → `main`** (currently `feat/ph-db-2-liorm-liq`) — unblocks org CI/agent-kit audits ([org hygiene plan](https://github.com/li-langverse/li-cursor-agents/blob/main/docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md) WP-H0).
2. **Merge `benchmarks` `feat/tier-db-registry` → `main`** (or open/merge a single integration PR) so `tier_db_registry` docs/harness match [`benchmark-tier-index.md`](benchmark-tier-index.md).
3. **Review + merge native stack PRs in order:** `lidb#13` (N1) + `lidb#12` (N2) → then `lidb#9` (N5) → `lidb#11` + `lis#10` (N3) — avoid duplicate sqlite/native work.
4. **Production registry:** provision **domain + TLS** and decide hosted `lis db` endpoint before calling PH-DB-4 “done” ([`lidb-li-data-platform.md`](../../proposals/lidb-li-data-platform.md) PH-DB-4 row).
5. **Triage closed duplicate PRs** (`lis#7`–`8`, `li-cursor-agents#16`) so agents do not reopen superseded PH-DB-4 stacks.

---

## 4. Production registry deploy blockers

| Blocker | Type | Unblocks |
|---------|------|----------|
| **Native engine not default** (sqlite smoke / embed path) | Engineering | PH-DB-3.1 + N1+N2 merge |
| **`tier_db_registry` not on `benchmarks` `main`** | CI / evidence | PH-DB-4 perf sign-off (≤1.2× Postgres P95) |
| **`lidb` default branch ≠ `main`** | Org / human | Required checks, agent-kit sync, honest CI badges |
| **Open native PR stack unmerged** (N1–N3, N5) | Engineering | `lis` registry routes serving real lidb OLTP |
| **`lip#17` E2E not green on production profile** | Engineering | `lip publish` → central DB contract |
| **Domain + TLS + secrets** (registry host) | Human | Public PH-DB-4 / **PH-8d-v2** remote registry |
| **Auth/RLS production path** (publisher JWT, not stubs) | Engineering | PH-DB-5 before untrusted publish |
| **Control plane still Supabase** | Engineering (PH-DB-10) | Optional for registry v1; blocks agent store migration |

**PH-8d-v2** (`lip` remote registry + trust store) remains **blocked on PH-DB-4** until rows above are cleared ([`vision-and-roadmap.md`](vision-and-roadmap.md#li-data-platform-ph-db-0--ph-db-10)).

---

## Agent continuation

1. **Read:** this file; [`benchmark-tier-index.md`](benchmark-tier-index.md); [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md)
2. **Run:** re-query commands in §1; `gh repo view li-langverse/lidb --json defaultBranchRef`
3. **Then:** after human H0/H1, refresh §2 percentages from merged PR exit gates only
4. **Blocked on:** human branch rename + benchmarks `main` integration — agents must not force-push `lidb`/`main`

## Links

- Bench index: [`benchmark-tier-index.md`](benchmark-tier-index.md)
- Live org queue: [development overview](https://li-langverse.github.io/roadmap/development-overview/)
- Control-plane migration: [li-cursor-agents `lidb-migration-control-plane.md`](https://github.com/li-langverse/li-cursor-agents/blob/main/docs/plans/lidb-migration-control-plane.md)
