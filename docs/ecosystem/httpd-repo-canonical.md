# HTTP package mirrors — canonical repo vs legacy `net.httpd`

<!-- DOC-ecosystem-httpd-canonical -->

**Status:** Recommendation only (WP-B4). **No repo deletes or renames** until human executes WP-D3 in the [org hygiene multi-agent plan](https://github.com/li-langverse/li-cursor-agents/blob/main/docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md) after review.

## Problem

The org hosts **two GitHub mirrors** for the same Li library (`import net.httpd`):

| GitHub repo | `li.toml` `name` | `pkg_id` | `github_repo` metadata |
|-------------|------------------|----------|------------------------|
| [`li-httpd`](https://github.com/li-langverse/li-httpd) | `li-net-httpd` | `PKG-li-net-httpd` | `li-net-httpd` (target name; repo not renamed yet) |
| [`net.httpd`](https://github.com/li-langverse/net.httpd) | `net.httpd` | `PKG-net-httpd` | `net.httpd` |

Both READMEs describe the same Phase H gateway. Source differs slightly; **`net.httpd`** carries path deps to sibling dot repos (`../http`, `../net`) from an older layout. The monorepo source of truth is **`lic` → `packages/li-net-httpd/`** ([repo naming in lic](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/repo-naming.md)).

## Decision table (recommendation)

| Layer | Canonical | Legacy / interim | Notes |
|-------|-----------|------------------|-------|
| **Li import** (source) | `import net.httpd` | `import li_httpd` | Documented in [lic import-style](https://github.com/li-langverse/lic/blob/main/docs/language/import-style.md); do not introduce new `li_httpd` uses. |
| **Monorepo folder** | `lic/packages/li-net-httpd/` | — | Listed in `packages/li.toml`; push via `push-official-package-repo.sh`. |
| **GitHub org mirror (today)** | **`li-httpd`** | **`net.httpd`** | `li-httpd` already matches org lists (`li-org-repos.txt`, branch protection, development-overview). |
| **GitHub org mirror (target, WP-D3)** | **`li-net-httpd`** | Archive **`net.httpd`**; redirect **`li-httpd` → `li-net-httpd`** | Aligns import `net.httpd` → repo `li-net-httpd` per [repo-naming.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/repo-naming.md). Human `gh repo rename` only. |
| **`lip` / registry publish** | Single index entry pointing at canonical mirror URL | No second publish path for `PKG-net-httpd` | Grep registry + ingest before D3: `rg 'net\.httpd|PKG-net-httpd' lip benchmarks`. |
| **Server binary / tier-5** | `lic` / `lis` binary **`li-httpd`** (build artifact) | — | Binary name ≠ package repo name; [lis](https://github.com/li-langverse/lis) infra + [httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md). |
| **Compiler prerequisites** | Unchanged — [httpd-prerequisites.md](httpd-prerequisites.md) | — | M1 `.li` still blocked on lic P0 gates. |

## Recommended actions (human-gated)

1. **Now:** Treat **`li-httpd`** as the only mirror agents should sync, CI-fix, and open package PRs against.
2. **Read-only on `net.httpd`:** No new features; add repo README banner “superseded by `li-httpd` (rename to `li-net-httpd` planned)” in a small follow-up if needed.
3. **WP-D3:** Human renames `li-httpd` → `li-net-httpd`, archives `net.httpd`, updates `roadmap/.github/li-org-repos.txt`, benchmarks ingest, and `official-packages.md` row.
4. **Do not delete** either mirror or change `import_name` without ADR + `lip` lockfile migration.

## Verification (agents)

```bash
# No duplicate publish ids in lip (when registry tree present)
rg -n 'PKG-net-httpd|net\.httpd' ../lip ../benchmarks --glob '*.{json,toml,md}' || true

# Org mirrors
gh repo view li-langverse/li-httpd --json name,description
gh repo view li-langverse/net.httpd --json name,description

# Monorepo metadata
rg -n 'import_name|github_repo' ../lic/packages/li-net-httpd/li.toml
```

## Related

| Doc | Role |
|-----|------|
| [httpd-prerequisites.md](httpd-prerequisites.md) | lic P0 gates before M1 `.li` |
| [lic repo-naming.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/repo-naming.md) | `net.httpd` → `li-net-httpd` naming rule |
| [official-packages.md](official-packages.md) | PKG-* table (add `PKG-li-net-httpd` row when mirror rename lands) |
| Org hygiene plan WP-B4 / WP-D3 | `li-cursor-agents/docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md` |
