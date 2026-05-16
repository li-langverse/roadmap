# Ecosystem governance

<!-- DOC-ecosystem-governance -->

Li standard and first-party software lives under the **[`li-langverse`](https://github.com/li-langverse)** GitHub organization. This page summarizes rules; the normative plan is [2026-05-16-li-ecosystem-governance.md](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-ecosystem-governance.md).

## GitHub organization

| What | Where |
|------|--------|
| Language + compiler | [`li-langverse/li-language`](https://github.com/li-langverse/li-language) |
| Standard libraries | `li-langverse/li-std-*` (as they split from the monorepo) |
| Infrastructure libs | `li-langverse/li-net`, `li-http`, … (see [li-httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md)) |
| Third-party packages | Author accounts; `lip` registry when phase 8d ships |

Create an org repo when a package is listed in [official-packages.md](official-packages.md), has multiple consumers, or will be published to the registry.

**CI is mandatory** before the repo is used: `.github/workflows/ci.yml` on `main` (job `check` for packages). Audit:

```bash
# from benchmarks checkout
python3 scripts/ensure-org-repo-ci.py
```

Use `./scripts/li-new-package my-pkg --official` for the correct tree (`PKG-*`, **ci.yml**, Dependabot). Then:

```bash
./scripts/push-official-package-repo.sh my-pkg --create
cd roadmap && ./scripts/apply-org-branch-protection.sh my-pkg
```

Do **not** run bare `gh repo create` without the package tree and CI workflow.

## Documentation standards

We follow common international practice (not formal ISO certification):

- **[Semantic Versioning](https://semver.org/)** — `version` in `li.toml`, git tags `vX.Y.Z`
- **[Keep a Changelog](https://keepachangelog.com/)** — every official package
- **[SPDX](https://spdx.dev/)** — `license` in `li.toml` and `LICENSE` file
- **Task-oriented English docs** — see [Documentation style](https://github.com/li-langverse/lic/blob/main/docs/contributing/documentation.md)

## Traceability IDs

| Prefix | Example | Use |
|--------|---------|-----|
| `REQ-` | `REQ-PROOF-01` | Language design spec |
| `PH-` | `PH-Pkg`, `PH-8b` | Master plan phases |
| `T-` | `T-modules-import-ok` | `li-tests/manifest.toml` notes |
| `PKG-` | `PKG-li-language` | [official-packages.md](official-packages.md) |
| `DOC-` | `DOC-ecosystem-lip` | HTML comment in doc source |

Each official package includes `PUBLISH.md`, `docs/traceability.md`, and `CHANGELOG.md`.

Run `./scripts/check-traceability.sh` in CI to catch missing `PKG-*` metadata in `packages/`.

## Agent workflow

| Task | Document / tool |
|------|-----------------|
| **Strict gates (P/S/F)** | [engineering-standards.md](engineering-standards.md) |
| Vision placement | [vision-and-roadmap.md](vision-and-roadmap.md) |
| Multi-agent / who owns what path | [agent-coordination.md](agent-coordination.md) |
| Cursor enforcement | `.cursor/hooks.json`, `li-ecosystem-gates.mdc`, skill **li-ecosystem-discipline** |
| Language change → bump downstream | [language-evolution.md](language-evolution.md) |
| New package tree | **create-li-package** skill — never hand-roll |
| GitHub org / secrets / new repo | **Action needed from you** — [master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) |
