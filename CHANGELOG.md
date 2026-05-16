# Changelog

## [Unreleased]

### Added

- [Development overview](https://li-langverse.github.io/roadmap/development-overview/) — org snapshot + live PR queue (browser GitHub API via `development-overview-live.js`).
- Cursor Automation prompts (`.cursor/automations/`) and `scripts/ecosystem-health-check.sh` for maintainer agents.

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
