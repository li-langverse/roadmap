# Agent-kit changelog

## 1.2.1 — 2026-05-17

- Overlay `overlays/li-cursor-agents` — commit-when-done + agent-kit sync for Cursor SDK runner
- `install-agent-kit.sh` resolves `li-cursor-agents` sibling repo

## 1.1.0 — 2026-05-16

- `li-release-notes.mdc` — mandatory agent-oriented release notes
- Skill `write-li-release-notes`
- Hook `remind-release-notes.sh` on stop
- Policy: `docs/ecosystem/release-notes.md`, template `docs/release-notes/TEMPLATE.md`

## 1.0.0 — 2026-05-16

- `li-pr-only.mdc`, `li-ecosystem-gates.mdc`
- Hooks: session-context, guard-destructive-git, guard-secrets, guard-direct-push, remind-governance-docs
- Skill: li-ecosystem-discipline
