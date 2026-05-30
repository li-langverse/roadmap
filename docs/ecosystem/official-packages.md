# Official Li packages

<!-- DOC-ecosystem-official-packages -->

Packages maintained under **[`li-langverse`](https://github.com/li-langverse)**. Each has a **`PKG-*`** traceability id.

| PKG id | Repository | Role | Phase | Notifies on upstream (`depends_on`) |
|--------|------------|------|-------|-------------------------------------|
| `PKG-lic` | [`li-langverse/lic`](https://github.com/li-langverse/lic) | Compiler, runtime, `li-tests`, docs | 0–7 | — (source of `lic` releases) |
| `PKG-lip` | [`li-langverse/lip`](https://github.com/li-langverse/lip) | Package manager + registry | 8b–8d | `lic`, `lit` |
| `PKG-lit` | [`li-langverse/lit`](https://github.com/li-langverse/lit) | Tests + ≥80% coverage | 8e | `lic` |
| `PKG-roadmap` | [`li-langverse/roadmap`](https://github.com/li-langverse/roadmap) | Governance docs + agent-kit | meta | — |
| `PKG-benchmarks` | [`li-langverse/benchmarks`](https://github.com/li-langverse/benchmarks) | Benchmark ingest + dashboard | meta | `lic`, `lis` |
| `PKG-lidb` | *proposed* [`li-langverse/lidb`](https://github.com/li-langverse/lidb) | Postgres-shaped engine, `liorm`, `liq`, registry migrations | **PH-DB-0..10** | `lis`, `lip`, `benchmarks` |
| `PKG-li-std-core` | `packages/li-std-core` → *planned* [`li-std-core`](https://github.com/li-langverse/li-std-core) | Standard library core | **4s**, **8a** | `lic` |
| `PKG-li-std-math` | `packages/li-std-math` → *planned* `li-std-math` | Math / linalg (2i/7e) | **2i** | `lic`, `li-std-core` |
| `PKG-li-http` | *planned* `li-langverse/li-http` | HTTP stack | H | `lic`, registry deps TBD |

## Monorepo paths (pre-split)

Until a package moves to its own repo, it may live under `packages/<name>/` in **`lic`**. Promotion checklist:

1. `./scripts/li-new-package <name> --official` or migrate with history
2. `gh repo create li-langverse/<name>`
3. Update this table; add repo to **`lic`** `.github/li-downstream-repos.txt`; copy Dependabot + `ecosystem-upstream.yml` templates (**8-sync**)
4. Tag `v0.1.0` with `CHANGELOG.md`

## Adding a row

1. Assign `PKG-<kebab-name>` (hyphens allowed in id after `PKG-`).
2. Create repo under `li-langverse`.
3. Ensure `PUBLISH.md` lists the same `PKG-*` id.
4. Link `PH-*` and `T-*` in `docs/traceability.md`.

Third-party packages are **not** listed here; they appear in the public `lip` index (phase 8d).


**Upstream notifications:** [Master plan § Cross-repo notifications](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md#cross-repo-dependency-notifications-every-official-package) — every row must receive GitHub dispatch / Dependabot when a `depends_on` repo releases.
