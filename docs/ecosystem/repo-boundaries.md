# li-langverse repo boundaries

Each GitHub repo owns **one domain**. Agents must not copy artifacts across repos — link externally instead.

## Canonical map

| Repo | Owns | Never add |
|------|------|-----------|
| **lic** | Compiler, runtime, `proof-db/`, semantics, `li-tests/` | Proof-library UI, benchmark dashboard |
| **benchmarks** | Perf catalog, ingest, `dashboard-next/`, `summary.json` | Proof UI/scripts, lic sources |
| **proof-library** | Proof corpus UI, `library.json`, votes | `proof-db` sources, perf matrix |
| **lip** / **lit** / **lis** | Package manager, test CLI, server | Compiler, benchmarks |
| **li-cursor-agents** | SDK agent runner, automations | Product source code from other repos |
| **roadmap** | Master plan, agent-kit, ecosystem docs | Implementation code |
| **research-findings** | Research memos, cycle reports | Compiler or benchmark code |
| **lidb** | Database ORM/contracts | Compiler core |
| **li-httpd**, **li-net**, **li-std-*** | Focused std packages | Unrelated domains |
| **sim.***, **studio.***, **physics.***, **ui**, **world**, etc. | One vertical Li package | Compiler, benchmarks, proof UI |

## Worktrees

`lic-studio-ui/`, `lic-gpu-bench-5b3a/`, `lic-vulkan-spirv-5b3a/`, `lic-worktrees/*` are **lic branch checkouts**, not separate repos. Merge to `lic` via PR; do not treat as canonical homes for proof-db or benchmarks.

## Local workspace layout

```
li-langverse/
  lic/              ← canonical compiler (main or feature branch)
  benchmarks/       ← perf dashboard
  proof-library/    ← proof corpus UI
  lip/ lit/ lis/    ← tooling packages
  li-cursor-agents/ ← agent runner (ephemeral clones in data/workspaces/)
  roadmap/          ← plans + agent-kit
  …vertical stubs…  ← one package per repo
```

Ephemeral agent clones live under `data/workspaces/` (gitignored). Delete freely to reclaim disk.

## Enforcement

- `.cursor/rules/repo-boundaries.mdc` in each repo (installed via `roadmap/scripts/install-repo-boundaries.sh`)
- Cross-repo reads at **build/CI time** via env vars (`LIC_ROOT`, `LIS_ROOT`) — never vendor sibling repos
