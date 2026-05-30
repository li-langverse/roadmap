# Li development overview

**li-langverse org** — live metrics on [progress.lilangverse.xyz](https://progress.lilangverse.xyz/).

The published site loads **`status.json`**, refreshed by GitHub Actions from the org API (repos, open issues, open PRs with CI rollup, workflow presence, doc sites). New public repos in the org are picked up automatically.

## What the dashboard shows

| Section | Source |
|---------|--------|
| Org metrics | GitHub Search + org repos API |
| Repository table | All public org repos (not a fixed list) |
| Open PR queue | Org-wide PR search + per-repo check rollup |
| Issue counts | Search API (`is:issue`) per repo; org total in metrics |

## Maintainer notes

- **Refresh locally:** `./scripts/refresh-development-overview.sh` (requires `gh auth login`)
- **Regenerate HTML:** `./scripts/gen-development-overview.sh`
- **`li-org-repos.txt`** — optional hints / policy list; org API is the source of truth for the dashboard
- **Known doc URLs** — extend `KNOWN_DOC_URLS` in `scripts/refresh_development_overview.py` when new custom domains ship

## Policy

*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main` branches.*

*CI policy: every repo should have `.github/workflows/ci.yml` — see benchmarks `docs/ecosystem/repo-ci-required.md`.*
