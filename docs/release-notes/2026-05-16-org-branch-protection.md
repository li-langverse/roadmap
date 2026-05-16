# Release notes: 2026-05-16 — org-branch-protection

**Status:** Released  
**Repo:** li-langverse/roadmap  
**PH / REQ:** meta-governance  
**Author:** agent

---

## Summary

Automated GitHub ruleset **Li: protected branches** across all org repos; agent-kit 1.2.0 adds `guard-pr-merge` and stronger push guards.

## Agent continuation

1. Run `./scripts/apply-org-branch-protection.sh` after adding org repos or changing CI job names in `org-branch-protection.json`
2. Run `./scripts/verify-org-branch-protection.sh` in roadmap CI / locally
3. All merges: feature branch → PR → human approval (never `gh pr merge` as agent)
4. Blocked on: none

## Changed

| Area | What | Evidence |
|------|------|----------|
| GitHub | Rulesets on 12 org repos | `scripts/apply_org_branch_protection.py` |
| Config | Per-repo required checks | `scripts/org-branch-protection.json` |
| Agent-kit | 1.2.0 guards + gates text | `guard-pr-merge.sh`, `manifest.toml` |
| Docs | SETUP_GITHUB.md automated | human only for secrets/new repos |

## Not changed

- Compiler, httpd, benchmark ingest logic
- Org secrets / PAT creation

## Breaking changes

Direct push to `main`/`dev`/`master` is **blocked** on GitHub for all org repos.

## Security

CVE posture unchanged; reduces risk of unreviewed merges to default branches.

## Performance

N/A.

## Downstream

| Repo | Action |
|------|--------|
| All siblings | `./scripts/sync-agent-kit.sh` (done in rollout) |

## CHANGELOG entry

```markdown
### Added
- Automated org branch protection (rulesets) and verify script; agent-kit 1.2.0 merge/push guards
```
