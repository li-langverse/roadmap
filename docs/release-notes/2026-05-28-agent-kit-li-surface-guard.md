# Release notes: 2026-05-28 — agent-kit-li-surface-guard

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** branch `cursor/org-wide-li-only-5b3a`  
**PH / REQ:** Agent-kit 1.3.4, Li surface policy  
**Author:** agent

---

## Summary (one sentence)

Agent-kit 1.3.4 adds org-wide Cursor rules and hooks that keep Li code on `def` syntax and block new non-Li helper-code drift outside compiler/runtime/tooling boundaries.

## Agent continuation (required)

1. Read: `agent-kit/.cursor/rules/li-def-not-proc.mdc`, `agent-kit/.cursor/rules/li-native-li-only.mdc`, `agent-kit/.cursor/hooks/guard-li-surface.sh`, and `agent-kit/.cursor/hooks.json`.
2. Run: `chmod +x agent-kit/.cursor/hooks/guard-li-surface.sh && ./scripts/install-agent-kit.sh lic --check` after syncing a target repo.
3. Then: after this roadmap PR merges, run `./scripts/install-agent-kit.sh <repo>` or each repo's `./scripts/sync-agent-kit.sh` so `lic`, `lip`, `lit`, `lis`, `benchmarks`, and `li-cursor-agents` inherit the guard.
4. Blocked on: target repos need follow-up sync PRs; existing legacy `proc` and helper-code occurrences are not removed by this PR.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Agent-kit rules | Added `li-def-not-proc.mdc` and `li-native-li-only.mdc`. | Files under `agent-kit/.cursor/rules/`. |
| Agent-kit hooks | Added `guard-li-surface.sh`; wired it into `afterFileEdit` with `failClosed` and `stop` in `agent-kit/.cursor/hooks.json`. | `bash -n agent-kit/.cursor/hooks/guard-li-surface.sh`; manual negative fixture blocks new `proc` token. |
| Agent-kit version | Bumped `agent-kit/manifest.toml` to `1.3.4`; updated `agent-kit/CHANGELOG.md`. | `agent-kit/manifest.toml`, `agent-kit/CHANGELOG.md`. |
| Roadmap release notes | Added this dated note and `CHANGELOG.md` Unreleased entry. | `docs/release-notes/2026-05-28-agent-kit-li-surface-guard.md`. |

## Not changed (scope fence)

- Existing legacy compiler/runtime names containing the banned token are not renamed in this PR.
- The Li compiler grammar is not changed; this PR is agent-kit guidance and hook enforcement.
- Target repos are not all synced in this roadmap PR; each repo still needs an install/sync commit.
- Compiler/runtime bootstrap code remains allowed in the narrow boundaries named by `li-native-li-only.mdc`.

## Breaking changes

N/A — this changes Cursor agent guard behavior, not shipped Li language/runtime APIs.

## Security

The hook reduces trusted-surface drift by blocking new sidecar helper implementations outside compiler/runtime/scripts/hooks boundaries. It adds no runtime code and no secrets.

## Performance

N/A — Cursor hook/rule policy only; no benchmark or runtime path changed.

## Downstream

| Repo | Action |
|------|--------|
| `lic`, `lip`, `lit`, `lis`, `benchmarks`, `li-cursor-agents` | Run agent-kit sync after roadmap merge; expect `.cursor/hooks/guard-li-surface.sh`, new rules, and updated `hooks.json`. |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- **Agent-kit 1.3.4 Li surface guard:** org-wide Cursor rule/hook set blocks new `proc` tokens and non-Li helper-code drift outside compiler/runtime/scripts/hooks boundaries — [2026-05-28-agent-kit-li-surface-guard.md](docs/release-notes/2026-05-28-agent-kit-li-surface-guard.md).
```
