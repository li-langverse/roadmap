# li-langverse/roadmap

Canonical **ecosystem governance**, **milestones**, **proposals (ADRs)**, and **agent-kit** (shared Cursor rules, hooks, skills) for the Li org.

## Read order (agents)

1. [engineering-standards.md](docs/ecosystem/engineering-standards.md)
2. [vision-and-roadmap.md](docs/ecosystem/vision-and-roadmap.md)
3. [agent-coordination.md](docs/ecosystem/agent-coordination.md)
4. [milestones.md](docs/roadmap/milestones.md)
5. [lic master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) — **PH-** tracker
6. [Benchmarks dashboard](https://li-langverse.github.io/benchmarks/)

## Normative split

| Topic | Home |
|-------|------|
| Compiler phases, REQ-*, `li-tests` | [`lic`](https://github.com/li-langverse/lic) |
| Ecosystem gates, vision, agent coordination | **this repo** |
| Perf snapshots & regression overview | [`benchmarks`](https://github.com/li-langverse/benchmarks) |

## Agent-kit install

Sibling layout: `coding-projects/{roadmap,li,lip,lit}`.

```bash
./scripts/install-agent-kit.sh lic    # installs into ../li
./scripts/install-agent-kit.sh lic --check
```

## Edit policy

| Paths | Merge |
|-------|-------|
| `docs/**`, `proposals/**`, root policy | **Human** after PR review |
| `agent-kit/**` | **Reviewer** after CI (agents do not self-merge) |

All work: **feature branch + PR** — no direct push to `main`.

## GitHub setup (human once)

See [SETUP_GITHUB.md](SETUP_GITHUB.md) for repo creation, branch protection, rulesets, and Pages (benchmarks repo).
