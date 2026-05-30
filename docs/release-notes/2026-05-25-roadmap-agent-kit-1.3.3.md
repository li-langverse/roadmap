# Release notes: 2026-05-25 — roadmap-agent-kit-1.3.3

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (opened by agent)  
**PH / REQ:** WP-A1 (org hygiene plan)  
**Author:** agent (WP-A1)

---

## Summary (one sentence)

Completes **agent-kit 1.3.3** adoption in `roadmap` by syncing installed `.cursor/` files and version stamps to match `agent-kit/manifest.toml` (manifest was already 1.3.3 on `main`; stamps were stuck at 1.3.2).

## Agent continuation (required)

1. **Read:** `agent-kit/CHANGELOG.md` (1.3.3 section); `docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md` WP-B2.
2. **Run:** `cd ../benchmarks && python3 scripts/ensure-org-agent-kit.py --local-only` — expect `roadmap` in `repos_ok` after merge + local `install-agent-kit.sh .` on sibling clone.
3. **Then:** dispatch **WP-B2** (`agent_kit_maintainer`) — org rollout PRs for drifted repos (`lidb`, `sim.scientific`, …).
4. **Blocked on:** human merge of this governance PR (roadmap policy).

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Version stamps | `.cursor/agent-kit-version`, `scripts/expected-agent-kit-version` → `1.3.3+12f1f4d190a4dd06` | `./scripts/install-agent-kit.sh .` |
| Skills | Added `.cursor/skills/run-local-ci-gha-quota/`; `li-ecosystem-discipline` links local-ci skill | `agent-kit/.cursor/skills/` rsync |
| Manifest | Already `version = "1.3.3"` on `main` | `agent-kit/manifest.toml` |

## Not changed (scope fence)

- **Org-wide rollout** to `lic`, `lip`, `benchmarks`, etc. — **not** in this PR (WP-B2 after merge).
- **agent-kit/manifest.toml** version number — already 1.3.3; no bump to 1.3.4.
- **Branch protection / org rulesets** — unchanged.
- **li-cursor-agents** overlay sync — separate PR when roadmap merges.

## Breaking changes

None — stamp-only + skill sync; downstream repos should run `install-agent-kit.sh` when convenient (WP-B2).

## Security

N/A — no trusted surface or CVE catalog changes.

## Performance

N/A — no benchmark or compiler paths.

## Downstream

| Repo | Action |
|------|--------|
| All `CORE_AGENT_KIT_REPOS` | After human merge: `../roadmap/scripts/install-agent-kit.sh <repo>` → PR per WP-B2 |
| **li-cursor-agents** | `./scripts/sync-agent-kit.sh` after roadmap merge (overlay) |
| **benchmarks** | Re-run `ensure-org-agent-kit.py` to refresh `org-agent-kit-audit.json` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Changed
- Agent-kit **1.3.3** adoption in `roadmap`: sync `.cursor/` stamps and `run-local-ci-gha-quota` skill.
```
