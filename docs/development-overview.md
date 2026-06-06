# Li development overview

**li-langverse org** · scanned **2026-06-06T09:12Z** · org-issue-zero queue + `gh` · live docs HEAD

| Metric | Value |
|--------|------:|
| Open issues (org queue) | 143 |
| Needs triage | 48 |
| Org swarm issue closes (audit) | 8 |
| Ready to merge (CI green) | — |
| Open PRs | — |
| Repos with live docs | 3 / 15 |

> **Issues:** Open count refreshes from committed `ecosystem-stats.json` and live Search API in the browser. The homelab **org-issue-triage** lane (`li-swarm`) has been closing duplicates/already-implemented issues via `close_github_issue` since 2026-06-06; net open issues down from **152 → 143** (2026-06-03 → 2026-06-06).


## Recommended merge order

_No PRs with green CI and non-draft status._

## Merge when reviewed

| Priority | PR | CI | Action | Notes |
|----------|-----|-----|--------|-------|
| — | — | — | — | No green PRs |

## Do not merge yet

| PR | CI | Action | Notes |
|-----|-----|--------|-------|
| — | — | — | No failing open PRs |

## All open PRs

| Repo | # | Title | Base | CI | Ready |
|------|---|-------|------|-----|-------|
| lic | 623 | [Li World Studio: Windows runnable + Inno Setup installer](https://github.com/li-langverse/lic/pull/623) | main | pending | no |

---

*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main`.*

*Snapshot: `./scripts/regenerate-development-overview-md.py` then `./scripts/deploy-pages-local.sh --build`. Live queue: browser on [development overview](https://li-langverse.github.io/roadmap/development-overview/) — no redeploy for queue-only changes.*
