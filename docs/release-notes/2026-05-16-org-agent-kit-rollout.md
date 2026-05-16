# Release notes: 2026-05-16 — org-agent-kit-rollout

**Status:** Released  
**Repo:** li-langverse/roadmap  
**PH / REQ:** meta-governance  
**Author:** agent

---

## Summary

Batch-applied agent-kit v1.1.0 to all org sibling repos via `scripts/apply-org-agent-kit.sh`; installed kit on roadmap root `.cursor/`; `install-agent-kit.sh` writes `expected-agent-kit-version` for every repo id.

## Agent continuation

1. Edit `agent-kit/` → bump `agent-kit/manifest.toml` → run `./scripts/apply-org-agent-kit.sh` or per-repo `./scripts/sync-agent-kit.sh` from each checkout
2. Policy unchanged: `docs/ecosystem/release-notes.md`
3. Blocked on: none

## Changed

| Area | What | Evidence |
|------|------|----------|
| Scripts | `apply-org-agent-kit.sh` | lic, lip, lit, lis, benchmarks, roadmap |
| Install | `install-agent-kit.sh` | all repo ids get `scripts/expected-agent-kit-version` |
| This repo | `.cursor/` from agent-kit | v1.1.0 |

## Not changed

- Governance doc content in `docs/ecosystem/` — **not** rewritten in this rollout
- Branch protection / CODEOWNERS — human setup unchanged

## Breaking changes

None.

## Security

N/A.

## Performance

N/A.

## Downstream

| Repo | Action |
|------|--------|
| lic, lip, lit, lis, benchmarks | Committed rollout on respective default branches |

## CHANGELOG entry

```markdown
### Added
- `apply-org-agent-kit.sh`; root `.cursor/` sync; org-wide rollout release note
```
