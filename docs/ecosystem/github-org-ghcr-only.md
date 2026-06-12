# GitHub org `li-langverse` — GHCR only

**GitLab** is where Li source code lives. **GitHub** exists for:

1. **GHCR** — `ghcr.io/li-langverse/*` container images  
2. **Org profile** — repository [`.github`](https://github.com/li-langverse/.github) (this README on github.com/li-langverse)  
3. **Legacy Pages** (retiring) — some `*.github.io` URLs until DNS moves to `*.lilangverse.xyz`

Do **not** clone, branch, or merge on `github.com/li-langverse/*` except `.github` maintenance.

## Canonical URLs

| Need | URL |
|------|-----|
| Browse / clone source | https://gitlab.lilangverse.xyz/li-langverse |
| Issues / MRs | GitLab group |
| Container images | `docker pull ghcr.io/li-langverse/<image>:<tag>` |
| Development overview | https://progress.lilangverse.xyz/roadmap/development-overview/ |

## Cleanup tooling

From `roadmap/`:

```bash
# Preview org description + repo archive plan
python3 scripts/github-org-ghcr-setup.py

# Apply org description + archive mirror repos (keeps .github only)
python3 scripts/github-org-ghcr-setup.py --apply

# Only update org description and repo banners (no archive)
python3 scripts/github-org-ghcr-setup.py --apply --stamp-only
```

Requires `gh auth login` with org owner permissions.

## Retired automation

| Was | Now |
|-----|-----|
| `gitlab-github-mirror` CronJob (15m git push) | **Suspended** — see `gitlab-github-mirror/deploy/k8s/cronjob.yaml` |
| `GH_MIRROR_TOKEN` / `GITHUB_OFFICIAL_TOKEN` | Revoke or scope to GHCR only |
| `benchmarks` GitLab CI → GitHub Pages git push | Removed — use GitLab Pages / homelab edge |
| `github` git remote on dev clones | Removed by `configure-gitlab-remotes.ps1` |

## Tokens (after cleanup)

| Token | Use |
|-------|-----|
| `GITLAB_TOKEN` | Git, GitLab API, CI |
| `GH_PACKAGES` / `GHCR_TOKEN` | `docker login ghcr.io`, image push/pull |
| `GH_TOKEN` | GHCR, legacy Pages workflow dispatch only |

## Related

- [GitLab-primary runbook](https://gitlab.lilangverse.xyz/li-langverse/homelab-k3s/-/blob/main/docs/gitlab-primary-github-mirror.md) (in `homelab-k3s` repo on GitLab)
- Org profile source: `li-langverse-dotgithub` / `.github`
