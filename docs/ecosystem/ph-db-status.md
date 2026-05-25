# PH-DB / native Li sprint — status checklist

<!-- DOC-ecosystem-ph-db-status -->

**Snapshot:** 2026-05-25 (UTC, post–native merge wave) · **Query:** read-only `gh pr list` / `gh repo view` / `gh api …/git/trees/main` across `li-langverse/*`. Re-run before merge decisions.

**Authority:** WP-N1…N9 scheduling in [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md); PH-DB-0…10 in [`proposals/lidb-li-data-platform.md`](../../proposals/lidb-li-data-platform.md).

---

## Integration milestones (tracked items)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| [`lis#10`](https://github.com/li-langverse/lis/pull/10) WP-N3 realtime WS | **Pending** | PR **OPEN** — `feat(ph-db): Realtime WebSocket changefeed` |
| [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96) `tier_db_security` → lidb | **Pending** | PR **OPEN** — harness wiring not merged |
| **`lidb` default branch → `main`** | **Pending** | `defaultBranchRef.name` = `feat/ph-db-2-liorm-liq` (not `main`) |
| **`tier_db_registry` on `benchmarks` `main`** | **Done** | `benchmarks/tier_db_registry/**` present on `main` tree |

---

## 1. PRs — merged vs open (branch family)

| State | Count (approx.) | Notes |
|-------|-----------------|-------|
| **Merged** | **32+** | Native N1/N2 + PH-DB-3.1 cutover + lip PH-DB-4 E2E landed on integration branches |
| **Open** | **8** | N3 (`lis#10`), bench security (#96), org hygiene (agent-kit), PH-DB-10 stubs |
| **Closed unmerged** | 5+ | Superseded stacks (`lis#7`–`8`, `li-cursor-agents#16`, `lidb#9`, `lidb#11`) |

### Merged (representative — do not re-implement)

| Repo | PR | Title |
|------|-----|-------|
| `roadmap` | [#14](https://github.com/li-langverse/roadmap/pull/14)–[#15](https://github.com/li-langverse/roadmap/pull/15), [#17](https://github.com/li-langverse/roadmap/pull/17), [#22](https://github.com/li-langverse/roadmap/pull/22) | PH-DB ADRs, native engine plan, status checklist |
| `lidb` | [#1](https://github.com/li-langverse/lidb/pull/1)–[#5](https://github.com/li-langverse/lidb/pull/5), [#7](https://github.com/li-langverse/lidb/pull/7)–[#8](https://github.com/li-langverse/lidb/pull/8), [#10](https://github.com/li-langverse/lidb/pull/10), [#12](https://github.com/li-langverse/lidb/pull/12)–[#13](https://github.com/li-langverse/lidb/pull/13), [#15](https://github.com/li-langverse/lidb/pull/15)–[#16](https://github.com/li-langverse/lidb/pull/16) | Scaffold, **WP-N1** heap/WAL, **WP-N2** native SQL, **PH-DB-3.1** sqlite cutover, liq audit, bench env |
| `lis` | [#5](https://github.com/li-langverse/lis/pull/5)–[#9](https://github.com/li-langverse/lis/pull/9) | PH-DB-3 `lis db` stub; PH-DB-4 registry routes → lidb |
| `lip` | [#13](https://github.com/li-langverse/lip/pull/13)–[#19](https://github.com/li-langverse/lip/pull/19) | OpenAPI, publish client, **PH-DB-4** automated E2E, stack-full probe |
| `lic` | [#275](https://github.com/li-langverse/lic/pull/275) | Master plan PH-DB cross-link |
| `li-cursor-agents` | [#17](https://github.com/li-langverse/li-cursor-agents/pull/17) | PH-DB-2/10 liq MCP stub |
| `benchmarks` | [#72](https://github.com/li-langverse/benchmarks/pull/72), [#74](https://github.com/li-langverse/benchmarks/pull/74), [#88](https://github.com/li-langverse/benchmarks/pull/88), [#89](https://github.com/li-langverse/benchmarks/pull/89) | `tier_db_registry` + G0 stubs + WP-N4 spectrum (on **`main`**) |

### Open (merge order hint: `lis#10` N3 → `benchmarks#96` N5 evidence → org `main`)

| Repo | PR | Branch / WP |
|------|-----|-------------|
| `lis` | [#10](https://github.com/li-langverse/lis/pull/10) | **WP-N3** realtime WS — **pending** |
| `benchmarks` | [#96](https://github.com/li-langverse/benchmarks/pull/96) | **WP-N5** `tier_db_security` → lidb harness — **pending** |
| `lidb` | [#6](https://github.com/li-langverse/lidb/pull/6), [#14](https://github.com/li-langverse/lidb/pull/14), [#17](https://github.com/li-langverse/lidb/pull/17) | agent-kit / docs SEO (non-engine) |
| `li-cursor-agents` | [#19](https://github.com/li-langverse/li-cursor-agents/pull/19), [#20](https://github.com/li-langverse/li-cursor-agents/pull/20) | PH-DB-10 checkbox audit + ControlPlaneStore stub |

**Re-query:**

```bash
gh search prs --owner li-langverse --state open --limit 50 -- "head:feat/ph-db"
gh search prs --owner li-langverse --state open --limit 50 -- "head:feat/lidb"
gh repo view li-langverse/lidb --json defaultBranchRef
gh api repos/li-langverse/benchmarks/git/trees/main?recursive=1 --jq '.tree[] | select(.path|test("tier_db_registry")) | .path' | head
```

---

## 2. WP-N1…N9 completion (%)

Exit gates from [`lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md). Percent = **engineering judgment** from PR state + branch artifacts (not automated).

| WP | Title | % | Evidence / blocker |
|----|-------|---|-------------------|
| **N1** | Native heap + WAL | **55%** | Merged [`lidb#13`](https://github.com/li-langverse/lidb/pull/13); default branch still integration ref until → `main` |
| **N2** | SQL parser + executor | **55%** | Merged [`lidb#12`](https://github.com/li-langverse/lidb/pull/12); exit gate smoke on integration branch |
| **N3** | Realtime changefeed | **35%** | **Pending** [`lis#10`](https://github.com/li-langverse/lis/pull/10); [`lidb#11`](https://github.com/li-langverse/lidb/pull/11) closed unmerged — re-open or stack on `lis#10` |
| **N4** | Benchmark matrix CI | **88%** | **Done** on `benchmarks` `main` (`tier_db_registry`, audit, G0 stubs); nightly ingest optional |
| **N5** | Security / audit harness | **55%** | Base harness merged; **pending** [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96); [`lidb#9`](https://github.com/li-langverse/lidb/pull/9) closed unmerged |
| **N6** | PG wire subset | **0%** | No open PR; blocked on N1+N2 production cutover on `main` |
| **N7** | RLS + auth production | **50%** | RLS/JWT SQL merged [`lidb#2`](https://github.com/li-langverse/lidb/pull/2); publisher auth path not production |
| **N8** | Vector native | **25%** | G0 bench stubs on `benchmarks` `main` [`#74`](https://github.com/li-langverse/benchmarks/pull/74); no `lidb` HNSW module PR |
| **N9** | Graph `lidb-graph` | **5%** | Research only (PH-DB-G0); no module PR |

**Integration gate PH-DB-3.1 (sqlite removal):** **45%** — merged [`lidb#15`](https://github.com/li-langverse/lidb/pull/15) native embed cutover; blocked on **`lidb` → `main`** + N3 realtime.

**Batch A parallel (N1–N5):** ~**58%** mean · **Sequential tail (N6–N9):** ~**20%** mean.

---

## 3. Top 3 remaining items

1. **`lidb` default branch → `main`** (currently `feat/ph-db-2-liorm-liq`) — unblocks org CI/agent-kit audits and honest required-check badges ([org hygiene plan](https://github.com/li-langverse/li-cursor-agents/blob/main/docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md) WP-H0). **Pending** per `gh repo view`.
2. **Merge WP-N3 realtime:** review + merge [`lis#10`](https://github.com/li-langverse/lis/pull/10); reconcile closed [`lidb#11`](https://github.com/li-langverse/lidb/pull/11) changefeed API (re-open or fold into `lis#10` stack). **Pending.**
3. **Merge [`benchmarks#96`](https://github.com/li-langverse/benchmarks/pull/96)** — wire `tier_db_security` to `lidb` harness for WP-N5 CI evidence. **Pending.**

---

## 4. Production registry deploy blockers

| Blocker | Type | Unblocks |
|---------|------|----------|
| **`lidb` default branch ≠ `main`** | Org / human | Required checks, agent-kit sync, honest CI badges |
| **WP-N3 realtime unmerged** (`lis#10`; `lidb#11` closed) | Engineering | `lis` changefeed contract; PH-DB-3.1 full sign-off |
| **`tier_db_security` harness open** (`benchmarks#96`) | CI / evidence | WP-N5 security gate in ecosystem CI |
| **Production registry:** domain + TLS + secrets | Human | Public PH-DB-4 / **PH-8d-v2** remote registry |
| **Auth/RLS production path** (publisher JWT, not stubs) | Engineering | PH-DB-5 before untrusted publish |
| **Control plane still Supabase** | Engineering (PH-DB-10) | Optional for registry v1; blocks agent store migration |

**Resolved since prior snapshot:** `tier_db_registry` on `benchmarks` `main`; native N1/N2 + PH-DB-3.1 cutover merged on `lidb` integration branch; `lip#17` PH-DB-4 E2E merged.

**PH-8d-v2** (`lip` remote registry + trust store) remains **blocked on PH-DB-4** until rows above are cleared ([`vision-and-roadmap.md`](vision-and-roadmap.md#li-data-platform-ph-db-0--ph-db-10)).

---

## Agent continuation

1. **Read:** this file; [`benchmark-tier-index.md`](benchmark-tier-index.md); [`proposals/lidb-native-li-matrices.md`](../../proposals/lidb-native-li-matrices.md)
2. **Run:** re-query commands in §1; `gh repo view li-langverse/lidb --json defaultBranchRef`; `gh pr view 10 --repo li-langverse/lis`; `gh pr view 96 --repo li-langverse/benchmarks`
3. **Then:** after human H0 (`lidb` → `main`), refresh §2 from merged exit gates only
4. **Blocked on:** human branch rename — agents must not force-push `lidb`/`main`

## Links

- Bench index: [`benchmark-tier-index.md`](benchmark-tier-index.md)
- Live org queue: [development overview](https://li-langverse.github.io/roadmap/development-overview/)
- Control-plane migration: [li-cursor-agents `lidb-migration-control-plane.md`](https://github.com/li-langverse/li-cursor-agents/blob/main/docs/plans/lidb-migration-control-plane.md)
