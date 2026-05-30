# Li development overview

**li-langverse org** · scanned **2026-05-16T18:10Z** · `gh pr list` / checks · `gh api` workflows per branch · `curl -sI` Pages

| Metric | Value |
|--------|------:|
| Ready to merge (CI green) | 10 |
| Open PRs | 14 |
| Blocked / needs work | 2 |
| Repos with live docs | 2 / 12 |

## Ecosystem statistics

Org-wide snapshot · refresh with `./scripts/compute-ecosystem-stats.py` · **Org repositories** counts every repo under `li-langverse` on GitHub (LoC still sums `.github/li-org-repos.txt` only). Open issues / closed PRs also update live in the browser.

| Metric | Value |
|--------|------:|
| Lines of code (tracked repos) | 67,208 |
| Org repositories (GitHub) | 14 |
| Open issues | 57 |
| Closed pull requests | 103 |

## Recommended merge order

1. **Package CI (P0, all green):** [li-net #2](https://github.com/li-langverse/li-net/pull/2), [li-httpd #2](https://github.com/li-langverse/li-httpd/pull/2), [li-std-core #2](https://github.com/li-langverse/li-std-core/pull/2), [li-std-math #2](https://github.com/li-langverse/li-std-math/pull/2), [li-demo #1](https://github.com/li-langverse/li-demo/pull/1).
2. [benchmarks #1](https://github.com/li-langverse/benchmarks/pull/1) · then sync [lic dev → main](https://github.com/li-langverse/lic/compare/main...dev) (unpin `lic@main` in package CI).
3. **Dependabot (after package CI on main):** lit #1, then li-net / li-httpd / li-std-core / li-std-math #1.

## Downstream repo CI (main branch)

Org repos from `.github/li-downstream-repos.txt` — workflow presence on GitHub `main`.

| Repo | CI on main | Notes |
|------|-----------|-------|
| lic | full | `.github/workflows/ci.yml` (linux/macos/windows) |
| li-language | full | docs site + build-and-test |
| lip | full | bootstrap via lic |
| lit | full | lit test + coverage |
| benchmarks | full | ci + ingest + pages |
| roadmap | full | governance ci.yml |
| li-net | none | only ecosystem-upstream on main; CI in PR #2 |
| li-httpd | none | only ecosystem-upstream on main; CI in PR #2 |
| li-std-core | none | only ecosystem-upstream on main; CI in PR #2 |
| li-std-math | none | only ecosystem-upstream on main; CI in PR #2 |
| li-demo | none | no `.github` on main; CI + dependabot in PR #1 |

## Branch CI coverage

Workflows at branch tip via GitHub contents API · last run conclusion where available · PR heads from open PRs.

| Metric | Value |
|--------|------:|
| Repos needing branch CI work | 8 |
| Package mirrors: main dispatch-only | 5 |
| Core repos: dev ≠ main workflows | 2 |

| Repo | main | dev | PR heads | Gap |
|------|------|-----|----------|-----|
| lic | full CI (11 wf: ci, memory, lean, fuzz, …) · last skipped | full CI (10 wf, −fuzz −hpc-competitive) · last failure | PR#1 fix/ci-dev-pr3-sync: full (11) · pass | dev workflow set behind main; fix dev CI before dev→main PR |
| li-language | lite (4 wf: ci, docs, benchmarks, release) · pass | full (10 wf) · pass | PR#5 fix/ci: full (11) pass · PR#3 → dev (10 wf) | main has 4 workflows; dev/PR heads run full compiler suite |
| benchmarks | package (ci, ingest, pages) · pass | — (no dev branch) | PR#1 feat/tier3: same 3 wf · pass | — |
| roadmap | package (ci.yml) · pass | — (no dev branch) | — | — |
| lip | package (ci + ecosystem-upstream) · pass | — (no dev branch) | — | — |
| lit | full (ci + notify-downstream + upstream) · pass | — (no dev branch) | PR#1 dependabot: same 3 wf · pass | — |
| lis | package (ci + branch-sync) · pass | package (ci + branch-sync) · pass | — | — |
| li-net | dispatch-only (ecosystem-upstream) · fail | — (no dev branch) | PR#2 ci/add-…: ci+upstream · pass · PR#1 dependabot: upstream only | Merge PR#2 — main has no ci.yml until then |
| li-httpd | dispatch-only (ecosystem-upstream) · fail | — (no dev branch) | PR#2: ci+upstream · pass · PR#1: upstream only | Merge PR#2 — same as li-net |
| li-std-core | dispatch-only (ecosystem-upstream) · fail | — (no dev branch) | PR#2: ci+upstream · pass · PR#1: upstream only | Merge PR#2 — Dependabot PRs get no checks until main has ci.yml |
| li-std-math | dispatch-only (ecosystem-upstream) · success | — (no dev branch) | PR#2: ci+upstream · pass · PR#1: upstream only | Merge PR#2 — main still dispatch-only |
| li-demo | none (no .github/workflows) | — (no dev branch) | PR#1 ci/add-…: ci+upstream · pass | Merge PR#1 — first CI on repo |

### Biggest branch CI gaps

- **Package mirrors** (`li-net`, `li-httpd`, `li-std-*`, `li-demo`): `main` has dispatch-only or no workflows; full `ci.yml` exists only on CI-setup PR heads until merge.
- **`lic` / `li-language`:** `dev` runs a different (larger) workflow set than `main`; `lic` dev last run failed, `main` has 4 vs dev 10 on li-language.
- **No `dev` branch** in downstream packages — CI improvements land via PR → `main` only.

## Ecosystem: docs and benchmarks

Catalog source: `li-langverse/benchmarks` `catalog.toml` (main) · tier-3 planned in lic `docs/ecosystem/benchmarks-catalog-additions.toml` · harness `benchmarks/harness/bench_ecosystem.py`.

| Metric | Value |
|--------|------:|
| Live docs (HTTP 200) | 2 |
| In benchmark catalog | 3 |
| CI-setup PRs (all pass) | 5 |

| Repo | Open PR | CI (PR) | Branch CI | Live docs | Benchmarks |
|------|---------|---------|-----------|-----------|------------|
| benchmarks | [#1 catalog tier-3](https://github.com/li-langverse/benchmarks/pull/1) | on main | main package · pass | [live](https://li-langverse.github.io/benchmarks/) | yes — Dashboard host + catalog.toml |
| li-language | [#3](https://github.com/li-langverse/li-language/pull/3) + [#5 fix-ci](https://github.com/li-langverse/li-language/pull/5) | on main | main lite / dev full · needs work | [live](https://li-langverse.github.io/li-language/) | partial — Harness in-repo; catalog rows under lic |
| lic | [#1 fix-ci](https://github.com/li-langverse/lic/pull/1) | on main | dev≠main workflows · needs work | none — No /lic/ Pages; handbook on li-language | partial — T0–2 + tier5 lis; tier-3 harness pending |
| lip | — | on main | pass | none — README only | yes — lip_smoke tier 3 |
| lit | [#1 dependabot](https://github.com/li-langverse/lit/pull/1) | pass | pass | none — README only | yes — lit_smoke tier 3 |
| lis | — | on main | pass | none — No Pages; docs in-repo | yes — tier5_http static_small, keepalive_pipelining |
| roadmap | — | on main | pass | none — docs on main; Pages after merge | no — Governance repo |
| li-net | [#1 dependabot](https://github.com/li-langverse/li-net/pull/1) | [#2 pass](https://github.com/li-langverse/li-net/pull/2) | dispatch-only · needs work | none — Package mirror | no |
| li-httpd | [#1 dependabot](https://github.com/li-langverse/li-httpd/pull/1) | [#2 pass](https://github.com/li-langverse/li-httpd/pull/2) | dispatch-only · needs work | none — Package mirror | no |
| li-std-core | [#1 dependabot](https://github.com/li-langverse/li-std-core/pull/1) | [#2 pass](https://github.com/li-langverse/li-std-core/pull/2) | dispatch-only · needs work | none — Package mirror | no |
| li-std-math | [#1 dependabot](https://github.com/li-langverse/li-std-math/pull/1) | [#2 pass](https://github.com/li-langverse/li-std-math/pull/2) | dispatch-only · needs work | none — Package mirror | no |
| li-demo | — | [#1 pass](https://github.com/li-langverse/li-demo/pull/1) | none · needs work | none — Scaffold example | no |

### CI setup PRs (package mirrors)

| Repo | PR | CI | Action |
|------|-----|-----|--------|
| li-net | [#2](https://github.com/li-langverse/li-net/pull/2) | pass | Merge when reviewed |
| li-httpd | [#2](https://github.com/li-langverse/li-httpd/pull/2) | pass | Merge when reviewed |
| li-std-core | [#2](https://github.com/li-langverse/li-std-core/pull/2) | pass | Merge when reviewed |
| li-std-math | [#2](https://github.com/li-langverse/li-std-math/pull/2) | pass | Merge when reviewed |
| li-demo | [#1](https://github.com/li-langverse/li-demo/pull/1) | pass | Merge when reviewed |

**Recently merged:** [roadmap #1](https://github.com/li-langverse/roadmap/pull/1) — branch protection automation.

## Merge when reviewed

| Priority | PR | CI | Action | Notes |
|----------|-----|-----|--------|-------|
| P0 | [li-net#2](https://github.com/li-langverse/li-net/pull/2) | pass | Merge when approved | Merge before Dependabot #1 — adds ci.yml. Pins lic@24f851cc until main builds. |
| P0 | [li-httpd#2](https://github.com/li-langverse/li-httpd/pull/2) | pass | Merge when approved | Merge before Dependabot #1. Same workflow as li-net #2. |
| P0 | [li-std-core#2](https://github.com/li-langverse/li-std-core/pull/2) | pass | Merge when approved | Merge before Dependabot #1. |
| P0 | [li-std-math#2](https://github.com/li-langverse/li-std-math/pull/2) | pass | Merge when approved | No open Dependabot PR; merge to enable future PR checks. |
| P0 | [li-demo#1](https://github.com/li-langverse/li-demo/pull/1) | pass | Merge when approved | Adds ci.yml + dependabot + ecosystem-upstream. |
| P0 | [benchmarks#1](https://github.com/li-langverse/benchmarks/pull/1) | pass | Merge when approved | Soft-dep: lic dev has bench_ecosystem CSV. |
| P2 | [lit#1](https://github.com/li-langverse/lit/pull/1) | pass | Merge when approved | Routine Dependabot. |
| P0 | [lic#1](https://github.com/li-langverse/lic/pull/1) | pass | Merge when approved | Linux/macOS/memory/registry green; Windows re-run. |
| P0 | [li-language#5](https://github.com/li-langverse/li-language/pull/5) | pass | Merge when approved | Supersedes #3. |

## Do not merge yet

| PR | CI | Action | Notes |
|-----|-----|--------|-------|
| [li-language#3](https://github.com/li-langverse/li-language/pull/3) | fail | Fix CI first | Superseded by #5 — close after #5 merges. |
| [lic compare](https://github.com/li-langverse/lic/compare/main...dev) | — | Open PR | Merge main into dev, push dev, then open PR. Local dev may be ahead of origin/dev. |

## All open PRs

| Repo | # | Title | Base | CI | Review |
|------|---|-------|------|-----|--------|
| li-net | 2 | ci: add lic check workflow on push and PR | main | pass | required |
| li-httpd | 2 | ci: add lic check workflow on push and PR | main | pass | required |
| li-std-core | 2 | ci: add lic check workflow on push and PR | main | pass | required |
| li-std-math | 2 | ci: add lic check workflow on push and PR | main | pass | required |
| li-demo | 1 | ci: add lic check workflow on push and PR | main | pass | required |
| benchmarks | 1 | feat(catalog): tier-3 lic ecosystem + security dashboard | main | pass | required |
| lit | 1 | build(deps): bump actions/checkout 4 → 6 | main | pass | required |
| li-net | 1 | chore(deps): bump actions/checkout 4 → 6 | main | none | required |
| li-httpd | 1 | chore(deps): bump actions/checkout 4 → 6 | main | none | required |
| li-std-core | 1 | chore(deps): bump actions/checkout 4 → 6 | main | none | required |
| li-std-math | 1 | chore(deps): bump actions/checkout 4 → 6 | main | none | required |
| lic | 1 | fix(ci): sync dev CI fixes (lip/lit checkout, Windows LLVM) | main | pass | required |
| li-language | 3 | Enhance li-httpd plan + expand physics benchmarks | main | fail | required |
| li-language | 5 | fix(ci): sync dev CI fixes (lip/lit checkout, Windows LLVM) | main | pass | required |

---

*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main` branches.*

*Snapshot: edit this file, then `./scripts/gen-development-overview.sh`. Live queue: browser JavaScript on the [development overview](https://li-langverse.github.io/roadmap/development-overview/) page (GitHub Search API — no Actions cron). Optional offline refresh: `./scripts/refresh-development-overview.sh`. Canvas: `lic` `canvases/pr-merge-queue.canvas.tsx` — link to the Pages URL.*
