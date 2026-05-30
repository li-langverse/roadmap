# Changelog

## [Unreleased]

### Added

- Org activity history charts on development overview (open/closed PRs and issues; history.json + live API).

### Added

- PH-DB-0 ADR: Li data platform (`proposals/lidb-li-data-platform.md`) — `lidb`+`lis` bundle, `liorm`+`liq`, Supabase vertical map, PH-DB-0..10 phases, registry-min path (PH-DB-0)

### Changed

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
