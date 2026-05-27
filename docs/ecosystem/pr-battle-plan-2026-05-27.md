# Org PR battle plan (2026-05-27)

**Purpose:** Merge superseding work first, close duplicate PRs without losing unique commits, then drain the queue by pillar priority (proof → compiler Wave A → benches → Studio verticals → ecosystem hygiene).

**Live queue:** [development overview](https://li-langverse.github.io/roadmap/development-overview/) · **Perf:** [benchmarks dashboard](https://li-langverse.github.io/benchmarks/)

---

## Summary (session 2026-05-27)

| Action | PRs / repos | Status |
|--------|-------------|--------|
| Merged vertical stack + LLVM bootstrap | `lic` #341, #335–#340, #334, #339 | **On `main`** |
| Drug-design deepen (LITL + inspector) | `lic` #336 | **Fix pushed** (`b7b82b35` — LLVM dominance split for `array[4,float]` returns); **merge when CI green** |
| Closed superseded (partial — token) | #289, #285 | **Closed** |
| Close remaining superseded | #284, #297, optional #269/#292 | **Pending** `gh` (see § Superseded hygiene) |
| Green merge candidates | `lic` #280; org agent-kit sync | **Pending** rebase + human/`merge-approved` |

---

## Merge policy (agents)

1. **Never** force-push. Rebase on `main`, resolve conflicts keeping **deeper vertical** `lib.li` over foundation stubs.
2. **Required for merge:** `build-and-test` + `build-and-test-macos` SUCCESS (tier5/httpd advisory may fail — fix or document N/A before claiming perf).
3. **Prefer** `merge-approved` label + `pr-merge-gate.py`; admin merge only when queue is blocked and CI is green.
4. **Before close:** `git log main..branch --oneline` — if unique commits exist, cherry-pick or comment the SHA for a follow-up issue.

---

## Tier P0 — `lic` compiler / proof (Wave A)

North star: [master plan PH-2e/2f/7e](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md).

| PR | Branch | CI | Action |
|----|--------|-----|--------|
| **#321** | `cursor/fix-wave-a-and-swarm-9031` | CONFLICTING | **Rebase on `main`**, resolve AutoVC/tier1 conflicts; supersedes scattered gap PRs when green |
| **#280** | `feat/proof-db-rebuild` | **GREEN** (linux+macos) | Rebase → review → **merge** (lemma rebuild pipeline) |
| **#286** | `feat/gap2-gitems` | Red | After #321 or rebase; G-par parallel-for |
| **#294** | `feat/gap2-proof` | Red | P-float corpus; coordinate with #321 |
| **#266** | `feat/gap-close-proofability` | Red | P-refine guard; depends on 2f hygiene |

**Blocked:** Do not land syntax/perf that bypasses Lean gate. Escalate new `trusted.lean` axioms.

---

## Tier P1 — Benchmark harness (PH-5b / PH-7e)

| PR | Focus | CI | Action |
|----|-------|-----|--------|
| **#308** | Registry family fill + tier-7 aliases | Red build | Rebase; likely conflicts with merged vertical CHANGELOG |
| **#306–#307** | WP1 num / WP2 md | Red | Merge **after** #308 or fold into one harness PR |
| **#305** | WP3 pde/robo/drug/bio/am/fluid | Red | Partially superseded by vertical packages — **diff vs main** before merge |
| **#304** | WP4 qm/auto/ml/viz smokes | Red | Keep if catalog rows still missing on dashboard |
| **#309** | tier-2 Li builds (WP-T2) | Red | Pair with benchmarks ingest |
| **#329** | Adaptive timing micro-benches | build green, **tier5 FAIL** | Fix tier5 regression or document advisory skip; do not merge on bench-only green |

**Evidence gate:** Update [benchmarks catalog](https://github.com/li-langverse/benchmarks/blob/main/catalog.toml) + run `./scripts/run-full-benchmark-suite.sh` after harness merges.

---

## Tier P2 — Studio / sim verticals (post-#341)

**Merged to `main`:** robotics #335, automotive #337, game #338, scientific #340, sim-rl #339, additive #334, foundation #341.

| PR | Action |
|----|--------|
| **#336** | Merge after CI (drug LITL deepen) |
| **#297** | **Close** — superseded by #334 (AM export) |
| **#289** | **Closed** — superseded by #339 (SIM-3 EnvPool) |
| **#285** | **Closed** — superseded by #337 |
| **#284** | **Close** — superseded by #340 |
| **#269** | Review — SIM-2 replay vs game #338; close if checkpoint on `main` covers it |
| **#292** | Keep open only if UX plan-loop doc deltas are not on `main` |
| **#283** | MCP lis stub — independent; rebase when Wave A stable |
| **#288–#298** | wgpu readback chain — merge **#288** before #298 |

---

## Tier P3 — PH-DB / Wave0 docs

| PR | Action |
|----|--------|
| **#323–#325** | Planning/docs only — merge one tracker PR, close duplicates |
| **#326–#327** | Wave0 verticals TOML / stdlib ADT — rebase after #321; CI stale |

---

## Tier P4 — CI / ecosystem

| PR | Action |
|----|--------|
| **#301** | lic-ci image cache — merge when build green |
| **#299** | `check` resource_options_invalid — rebase (may be on `main` already) |
| **#272** | package-release dispatch — merge after CI |
| **#319** | numerics MD survey (docs) — low risk when green |

---

## Other org repos

| Repo | PR | Mergeable | Action |
|------|-----|-----------|--------|
| **benchmarks** | #113, #114, #121 | Yes | Merge cloud-env + adaptive ingest (no li-demo) |
| **roadmap** | #25, #26 | Yes | Merge vision snapshot + agent-kit policy |
| **roadmap** | #19–#21 | CONFLICTING | Rebase agent-kit/docs after roadmap #25 |
| **lip / lit / lis / li-net / li-httpd** | agent-kit sync ~#12 | Yes | Batch merge after roadmap agent-kit lands |
| **lis** | #12 | Yes | tier5 CSV — merge for dashboard honesty |
| **li-std-math** | #7 | Yes | Dependabot checkout v6 — trivial |

**Order:** roadmap agent-kit → mirror sync PRs → benchmarks → `lic` product PRs.

---

## Superseded hygiene (runbook)

```bash
# From lic checkout — verify nothing unique on branch
git fetch origin main
git log --oneline origin/main..origin/<branch>

# Close with comment (example)
gh pr close 284 --repo li-langverse/lic --comment "Superseded by #340 (merged). ..."
```

**Template comment:** Superseded by merged `cursor/vertical-*-5599` / #33x. Progress is on `main`; reopen only if `git log main..branch` shows commits not cherry-picked.

---

## Agent continuation

1. **Read:** This file, `lic` `CHANGELOG.md` `[Unreleased]`, [SHIP-STATUS](https://github.com/li-langverse/benchmarks/blob/main/docs/dashboard/SHIP-STATUS.md).
2. **Run:** `gh pr checks 336 -R li-langverse/lic` → if green: `gh pr merge 336 --merge`. Then close #284, #297.
3. **Run:** Rebase #321 on `main`; merge #280 when review OK.
4. **Run:** `python3 ../benchmarks/scripts/ecosystem-audit.py` after bench PR merges.
5. **Blocked:** `GH_TOKEN` invalid in cloud agent — human must refresh `.env.github` or merge via UI.

---

## Not changed

- Branch protection / `merge-approved` ruleset (roadmap `apply-org-branch-protection.sh`).
- `li-demo` automation sandbox (no merge sweeps).
- Master plan phase ordering or coverage tiers.
