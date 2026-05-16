# Upstream release notifications (8-sync)

When **`lic`**, **`lit`**, or **`lip`** releases, dependent repos get a GitHub **issue** and/or **`repository_dispatch`**.

## Wiring

| Repo | On release | Notifies |
|------|------------|----------|
| **lic** | `notify-downstream.yml` | repos in `.github/li-downstream-repos.txt` |
| **lit** | `notify-downstream-lit.yml` | **lip** (and more via list later) |
| each package | `ecosystem-upstream.yml` | opens tracking issue in that repo |

## Action needed from you (one-time)

1. **Secret on `li-langverse/lic`:** `LI_DOWNSTREAM_DISPATCH_TOKEN` — fine-grained PAT on **lip** + **lit** with **Actions: Read and write** (for `repository_dispatch`). Re-run **notify-downstream** after updating scopes if you see HTTP 403.
2. **Secrets on `li-langverse/lip` and `li-langverse/lit`:** `LIC_CHECKOUT_TOKEN` — fine-grained PAT with **Contents: Read** on **lic** (needed while **lic** is private).
2. **Optional org app:** [Renovate](https://github.com/apps/renovate) on `li-langverse` for auto-PRs on `lic_version` in `li-toolchain.toml`.
4. **Label:** create `ecosystem-upstream` on repos (or issues will be created without label).
5. **Push** updated workflows to **lic**, **lip**, **lit** on GitHub.

## Test

After push, run **notify-downstream** workflow_dispatch on **lic** with a test version, or publish a patch release — **lip** should run **ecosystem-upstream** and open an issue.

## Local agent / CLI token

Path: `/Users/julian/Documents/coding-projects/.env.github` (sibling of `li/`, `lip/`, `lit/`).

1. Edit `GH_TOKEN=` (fine-grained PAT).
2. `chmod 600 .env.github`
3. Agent runs: `./scripts/with-github-env.sh gh auth status`
4. Push: `./scripts/push-li-langverse-repos.sh`

Cloud dispatch uses repo secret `LI_DOWNSTREAM_DISPATCH_TOKEN` on **lic** only (separate from `.env.github`).
