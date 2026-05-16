# GitHub setup (human-only)

<!-- DOC-roadmap-setup-github -->

Complete once per org. Agents: post **“Action needed from you”** and wait.

## Create repositories

```bash
gh repo create li-langverse/roadmap --public --description "Li ecosystem governance + agent-kit"
gh repo create li-langverse/benchmarks --public --description "Li benchmark aggregation + dashboard"
```

Push sibling checkouts:

```bash
cd ../roadmap && git init && git add -A && git commit -m "chore: initial roadmap + agent-kit"
git branch -M main
git remote add origin https://github.com/li-langverse/roadmap.git
git push -u origin main

cd ../benchmarks && git init && git add -A && git commit -m "chore: initial benchmarks hub + dashboard"
git branch -M main
git remote add origin https://github.com/li-langverse/benchmarks.git
git push -u origin main
```

## Branch protection (both repos)

On `main`:

- Require pull request before merging
- Require approvals: **1**
- Require status checks to pass
- Do not allow bypassing

### Roadmap path rulesets (optional second ruleset)

- **Governance:** `docs/**`, `proposals/**`, `README.md`, `CHANGELOG.md` — require code owner review
- **Agent-kit:** `agent-kit/**` — require CI + 1 approval

## Benchmarks: GitHub Pages

Repo **Settings → Pages → Build from GitHub Actions** (`pages.yml` workflow).

Dashboard URL: https://li-langverse.github.io/benchmarks/

## CI dispatch token (benchmarks ingest)

1. Create fine-grained PAT or repo secret `BENCHMARKS_INGEST_TOKEN` on **benchmarks** repo.
2. Add `LI_BENCHMARKS_DISPATCH_TOKEN` secret on **lic** for `repository_dispatch` after bench CI.

See `benchmarks/SETUP_GITHUB.md` for ingest workflow wiring.
