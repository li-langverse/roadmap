# Li development overview

**li-langverse org** · scanned **2026-05-23T00:50Z** · `gh pr list` / checks · live docs HEAD

| Metric | Value |
|--------|------:|
| Ready to merge (CI green) | 0 |
| Open PRs | 2 |
| Blocked / needs work | 1 |
| Repos with live docs | 3 / 12 |

## Recommended merge order

_No PRs with green CI and non-draft status._

## Merge when reviewed

| Priority | PR | CI | Action | Notes |
|----------|-----|-----|--------|-------|
| — | — | — | — | No green PRs |

## Do not merge yet

| PR | CI | Action | Notes |
|-----|-----|--------|-------|
| [lic#176](https://github.com/li-langverse/lic/pull/176) | fail | Fix CI first | feat(wave-a): 2i explicit math, 7e verify, 7d @vectorized on |

## All open PRs

| Repo | # | Title | Base | CI | Ready |
|------|---|-------|------|-----|-------|
| lic | 175 | [feat(httpd): httpd plan loop — M1.5–M3 optional gateway hooks](https://github.com/li-langverse/lic/pull/175) | main | none | no |
| lic | 176 | [feat(wave-a): 2i explicit math, 7e verify, 7d @vectorized on def](https://github.com/li-langverse/lic/pull/176) | main | fail | no |

---

*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main`.*

*Snapshot: `./scripts/regenerate-development-overview-md.py` then `./scripts/deploy-pages-local.sh --build`. Live queue: browser on [development overview](https://li-langverse.github.io/roadmap/development-overview/) — no redeploy for queue-only changes.*
