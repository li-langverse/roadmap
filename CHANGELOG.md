# Changelog

## [Unreleased]

### Added

<<<<<<< HEAD
- **lidb matrices appendix:** token efficiency cross-link to benchmarks/lidb audit — [2026-05-25-liq-token-efficiency-xlink.md](docs/release-notes/2026-05-25-liq-token-efficiency-xlink.md).
=======
- **PH-DB status checklist:** `docs/ecosystem/ph-db-status.md` — merged vs open `feat/ph-db*` / `feat/lidb*` / `feat/tier-db*` PRs, WP-N1…N9 %, human actions, production registry blockers — [2026-05-25-ph-db-status.md](docs/release-notes/2026-05-25-ph-db-status.md)
>>>>>>> ec904d5 (chore: CHANGELOG [Unreleased] for ph-db-status checklist)

- **lidb native Li research:** `proposals/lidb-native-li-matrices.md` — 8 vertical competitor tables, WP-N1…N9, benchmark spectrum, PH-DB-3.1 ([2026-05-25-lidb-native-li-research.md](docs/release-notes/2026-05-25-lidb-native-li-research.md))

- PH-DB native engine ADR (`proposals/lidb-native-engine.md`): deprecate sqlite smoke; parallel N1/N2/N3/N5; sequential N4 (after N2+N3), N6 (after N5); realtime in `lis` bundle
- PH-DB roadmap gaps: `PKG-lidb` in `official-packages.md`; PH-DB-0..10 table + **PH-8d-v2 → PH-DB-4** in `vision-and-roadmap.md`; `benchmark-tier-index.md`; proposal cross-links (`lidb-li-data-platform` ↔ `lidb-multi-model-gpu-research`)
- PH-DB-0 ADR: Li data platform (`proposals/lidb-li-data-platform.md`) — `lidb`+`lis` bundle, `liorm`+`liq`, Supabase vertical map, PH-DB-0..10 phases, registry-min path (PH-DB-0)

### Changed

- `proposals/lidb-li-data-platform.md` — PH-DB-3.1 row, WP-N1…N9 scheduling, links to matrices + lidb architecture ADR
- Vision **north star**: go-to ecosystem for HPC, scientific computing, and AI (`docs/ecosystem/vision-and-roadmap.md`); agent-kit **1.3.1** session hooks

### Added

- [Development overview](https://li-langverse.github.io/roadmap/development-overview/) — org snapshot (PR queue, branch CI, docs/bench); source `docs/development-overview.md`, built via `scripts/gen-development-overview.sh` and GitHub Pages.
- Live PR merge queue: `data/development-overview/status.json` refreshed every 15 minutes on `main` (`scripts/refresh-development-overview.sh`); Pages UI polls every 60s (`scripts/development-overview-live.js`).

### Changed

- Org-owner PR-review bypass on **Li: protected branches** (`bypass_org_owners` in `org-branch-protection.json`; `OrganizationAdmin` + `pull_request` mode).

### Added

- Agent-oriented release notes policy, template, skill, rule, and stop hook (agent-kit 1.1.0).
- `scripts/apply-org-agent-kit.sh`; root `.cursor/` sync; org-wide rollout to sibling repos.
- `scripts/apply-org-branch-protection.sh` — GitHub rulesets (PR-only + CI) for all org repos; agent-kit 1.2.0.

## [1.1.0] - 2026-05-16

### Added

- `docs/ecosystem/release-notes.md`, `docs/release-notes/TEMPLATE.md`
- Agent-kit: `li-release-notes.mdc`, `write-li-release-notes` skill, `remind-release-notes.sh`

## [1.0.0] - 2026-05-16

### Added

- Initial roadmap repo: ecosystem docs, agent-kit v1.0.0, PR-only workflow.
- Milestones index and proposal template.
