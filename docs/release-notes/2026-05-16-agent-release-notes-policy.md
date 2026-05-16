# Release notes: 2026-05-16 — agent-release-notes-policy

**Status:** Released  
**Repo:** li-langverse/roadmap  
**PH / REQ:** meta-governance  
**Author:** agent

---

## Summary

Org-wide mandatory agent-oriented release notes: policy, template, `li-release-notes.mdc`, `write-li-release-notes` skill, and `remind-release-notes` stop hook in agent-kit 1.1.0.

## Agent continuation

1. Read: `docs/ecosystem/release-notes.md`, `docs/release-notes/TEMPLATE.md`
2. Run: `./scripts/install-agent-kit.sh lic` (and lip/lit/lis) from sibling code repos
3. Then: on every merge-worthy PR in any org repo, add dated `docs/release-notes/` + CHANGELOG before `gh pr create`
4. Blocked on: none

## Changed

| Area | What | Evidence |
|------|------|----------|
| Policy | `docs/ecosystem/release-notes.md` | linked from engineering-standards checklist |
| Template | `docs/release-notes/TEMPLATE.md` | Agent continuation + Not changed sections |
| Agent-kit | `li-release-notes.mdc`, skill, hook | `agent-kit/manifest.toml` → 1.1.0 |
| Gates / discipline | read order + checklist | `li-ecosystem-gates.mdc`, `li-ecosystem-discipline/SKILL.md` |

## Not changed

- `lic` compiler, `lis` httpd, benchmarks dashboard ingest logic — **not** in this PR
- GitHub branch protection / required reviewers — human setup unchanged
- PR-only workflow rules — unchanged

## Breaking changes

None.

## Security

N/A — documentation and agent-kit only.

## Performance

N/A.

## Downstream

| Repo | Action |
|------|--------|
| lic, lip, lit, lis, benchmarks | Run `./scripts/sync-agent-kit.sh` (or install script); adopt `docs/release-notes/` per repo |

## CHANGELOG entry

```markdown
### Added
- Mandatory agent-oriented release notes (policy, template, rule, skill, hook); agent-kit 1.1.0
```
