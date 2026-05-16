# Release notes: 2026-05-16 — org-owner-ruleset-bypass

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** #1 (branch `chore/org-branch-protection-automation`)  
**PH / REQ:** meta-governance  
**Author:** agent

---

## Summary

Org owners can bypass **pull-request review** rules only (`OrganizationAdmin` + `pull_request` mode) on ruleset **Li: protected branches**; config-driven via `org-branch-protection.json` and already applied to all 12 org repos.

## Agent continuation

1. Read: `SETUP_GITHUB.md` (org-owner bypass section), `scripts/org-branch-protection.json`
2. Run: after CI job renames, `../li/scripts/with-github-env.sh ./scripts/apply-org-branch-protection.sh`
3. Then: solo maintainer merges own PRs via **Merge without waiting for requirements** (not self-approval); agents still must not `gh pr merge`
4. Blocked on: none

## Changed

| Area | What | Evidence |
|------|------|----------|
| Config | `bypass_org_owners`, `bypass_org_owners_mode` | `scripts/org-branch-protection.json` |
| Script | `bypass_actors_from_config`, `build_ruleset(..., bypass_actors)` | `scripts/apply_org_branch_protection.py` |
| Docs | Solo-maintainer bypass workflow | `SETUP_GITHUB.md` |
| GitHub | Rulesets updated on 12 repos | apply script run 2026-05-16 |

## Not changed

- Required CI status checks still enforced on merge (unless owner uses broader bypass modes — `always` not enabled)
- Agent `guard-pr-merge` / PR-only rules in agent-kit
- `lic` compiler, CVE harnesses, benchmark ingest
- CODEOWNERS / `require_code_owner_review` on `roadmap` governance paths

## Breaking changes

None — adds optional bypass for org owners only; direct push to default branches remains blocked.

## Security

Org owners can merge without a second reviewer when bypassing PR rules; audit log records bypass. Set `bypass_org_owners: false` and re-apply to revoke. CVE/compiler posture unchanged.

## Performance

N/A — GitHub ruleset metadata only.

## Downstream

| Repo | Action |
|------|--------|
| All `li-langverse` repos | No action — rulesets already updated via apply script |

## CHANGELOG entry

```markdown
### Changed
- Org-owner PR-review bypass (`bypass_org_owners`) on **Li: protected branches** rulesets; applied to all org repos
```
