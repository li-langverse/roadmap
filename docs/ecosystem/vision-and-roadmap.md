# Vision & roadmap governance

<!-- DOC-ecosystem-vision-roadmap -->

**Where visions live** so agents and humans do not fork the story per repo.

## Layers

| Scope | Canonical home | Updates when |
|-------|----------------|--------------|
| **Language + compiler + org** | [Master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) | Pillars, phases **PH-***, new repo policy, cross-cutting gates |
| **Ecosystem governance + agent-kit** | **This repo** | Engineering standards, coordination, PR-only agent-kit |
| **Milestones & themes** | [docs/roadmap/](../../roadmap/) | PH-linked status, quarterly themes |
| **Benchmarks dashboard** | [`li-langverse/benchmarks`](https://github.com/li-langverse/benchmarks) | Ingested CSV, regression overview |
| **Product / package** | Each package `README.md`, `PUBLISH.md`, `docs/traceability.md` | Package scope only — not language syntax |
| **Server (li-httpd)** | [li-httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md) + **`lis`** repo | Agent gateway features |
| **Living gaps** | [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) | What is **not** proved yet |

**Rule:** If a change affects **more than one package** or **Li pillars**, update the **master plan** and open a **proposal** here (human merge). Do not hide ecosystem vision only in a package README.

### This repo

- **Governance** — `docs/ecosystem/` (canonical; `lic` has stubs)
- **Milestones** — `docs/roadmap/`; master plan stays normative for **PH-** order
- **Agent-kit** — `agent-kit/`; install into code repos via `scripts/install-agent-kit.sh`
- Agents: read **engineering-standards** + **master plan PH tracker** each session

---

## Li vision (non-negotiable)

All ecosystem work must reinforce:

1. **Easy** — Nim-like surface; low ceremony; TOML/config desugar
2. **AI-first** — agents, streaming, observability, safe defaults at the edge
3. **Secure** — proofs + typed config + CVE-informed tests + minimal trusted base
4. **Provable** — `lic build` = Lean; no `sorry` in user code
5. **Blazingly fast** — LLVM, SIMD, OpenMP; measured regressions; no perf claims without benches

See [engineering-standards.md](engineering-standards.md) for how agents enforce this daily.
