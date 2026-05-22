# GitHub setup

<!-- DOC-roadmap-setup-github -->

Most protection is **automated**. Human steps are only where noted below.

## Branch protection (automated)

From a roadmap checkout with `GH_TOKEN` (org admin or custom role with rulesets):

```bash
cd ../roadmap
../li/scripts/with-github-env.sh ./scripts/apply-org-branch-protection.sh
../li/scripts/with-github-env.sh ./scripts/verify-org-branch-protection.sh
```

This upserts ruleset **Li: protected branches** on every `li-langverse` repo:

| Rule | Effect |
|------|--------|
| `update` | No direct push to `main` / `dev` / `master` |
| `pull_request` | Merge only via PR + **1 approval** |
| `required_status_checks` | Per-repo CI jobs (see `scripts/org-branch-protection.json`) |
| `non_fast_forward` | No force-push |

**Org-owner bypass (solo maintainer):** When `bypass_org_owners` is `true` in `scripts/org-branch-protection.json`, **organization owners** may bypass **pull-request review** rules only (`bypass_org_owners_mode`: `pull_request`). They still merge via PR; CI required checks still apply. Owners use **Merge without waiting for requirements** on the PR — self-approval does not count. Set `bypass_org_owners` to `false` to remove bypass on the next apply run.

**Human intervention (by design):**

- **PR approval / merge** — maintainers (agents open PRs only; see `li-pr-only.mdc`); org owners may bypass review when configured above
- **Roadmap governance paths** — `CODEOWNERS` on `docs/`, `proposals/`, `agent-kit/` (`require_code_owner_review` on roadmap)
- **Org secrets, new repos, bypass flags** — maintainers only

Per-repo CI contexts: edit `scripts/org-branch-protection.json`, re-run apply script.

## Create repositories (human)

```bash
gh repo create li-langverse/roadmap --public --description "Li ecosystem governance + agent-kit"
gh repo create li-langverse/benchmarks --public --description "Li benchmark aggregation + dashboard"
```

Then run `apply-org-branch-protection.sh` on the new repo name.

## GitHub Pages (no Actions)

| Site | Local deploy |
|------|----------------|
| [Benchmarks dashboard](https://li-langverse.github.io/benchmarks/) | `benchmarks/scripts/deploy-pages-local.sh --build` |
| [Development overview](https://li-langverse.github.io/roadmap/development-overview/) | `roadmap/scripts/deploy-pages-local.sh --build` |

Both push an orphan **`gh-pages`** branch and set Pages source to **branch deploy** (not `pages.yml`). Use `--workflow` only if you intentionally want Actions.

Live PR queue on the overview site refreshes in the **browser** — redeploy only when `docs/development-overview.md` snapshot HTML changes.

## CI dispatch token (benchmarks ingest)

1. Repo secret `BENCHMARKS_INGEST_TOKEN` on **benchmarks**
2. `LI_BENCHMARKS_DISPATCH_TOKEN` on **lic** for `repository_dispatch` after bench CI

See `benchmarks/SETUP_GITHUB.md` for ingest wiring.

## Agent-kit sync

After changing `agent-kit/`:

```bash
./scripts/apply-org-agent-kit.sh   # all sibling repos
```
