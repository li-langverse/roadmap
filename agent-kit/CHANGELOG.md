# Agent-kit changelog

## 1.3.0 — 2026-05-16

- Skills: `plan-feature-from-issue`, `audit-plan-completion`
- Automations: issue-feature-planner, plan-completion-audit
- Commands: `plan-feature`, `audit-plans`
- Overlay `benchmarks`; workflow template for issue planning

## 1.1.0 — 2026-05-16

- `li-release-notes.mdc` — mandatory agent-oriented release notes
- Skill `write-li-release-notes`
- Hook `remind-release-notes.sh` on stop
- Policy: `docs/ecosystem/release-notes.md`, template `docs/release-notes/TEMPLATE.md`

## 1.0.0 — 2026-05-16

- `li-pr-only.mdc`, `li-ecosystem-gates.mdc`
- Hooks: session-context, guard-destructive-git, guard-secrets, guard-direct-push, remind-governance-docs
- Skill: li-ecosystem-discipline
