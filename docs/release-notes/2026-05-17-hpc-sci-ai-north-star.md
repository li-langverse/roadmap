# Release notes: 2026-05-17 — hpc-sci-ai-north-star

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PH / REQ:** meta-governance (vision)  
**Author:** agent

---

## Summary (one sentence)

Encodes Li’s **go-to ecosystem** ambition for **HPC, scientific computing, and AI** in canonical vision docs and agent-kit session hooks so every agent session reads the north star before coding.

## Agent continuation (required)

1. Read: `docs/ecosystem/vision-and-roadmap.md` § North star; `docs/roadmap/milestones.md` strategic themes line
2. Run: after merge, `./scripts/install-agent-kit.sh lic` (and lip/lit/lis/benchmarks as needed) from sibling code repos
3. Then: align new proposals/PH rows to HPC / scientific / AI outcomes; reject generic-only scope unless master plan requires it
4. Blocked on: **human merge** for `docs/**` governance paths

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Vision | § North star — go-to ecosystem table + agent deferral rules | `docs/ecosystem/vision-and-roadmap.md` |
| Milestones | Strategic themes link to north star | `docs/roadmap/milestones.md` |
| Overview | One-line ambition at top | `docs/ecosystem/overview.md` |
| Agent-kit | session hook + gates read order + plan-feature skill | `agent-kit/.cursor/hooks/session-context.sh`, `li-ecosystem-gates.mdc`, `plan-feature-from-issue/SKILL.md` |
| Agent-kit version | manifest bump | `agent-kit/manifest.toml` → **1.3.1** |

## Not changed (scope fence)

- `lic` compiler, LLVM codegen, Lean pipeline — **not** in this PR
- `lis` httpd, tier5 exploits, benchmarks ingest — **not** in this PR
- Master plan **PH-** order or phase gates — **not** modified
- Org branch protection scripts — **not** in this PR

## Breaking changes

None.

## Security

N/A — documentation and agent-kit reminders only.

## Performance

N/A — no benchmark or threshold changes.

## Downstream

| Repo | Action |
|------|--------|
| lic | Merge companion PR `feat/docs-hpc-ai-north-star` (AGENTS + rules stub); then `./scripts/sync-agent-kit.sh` |
| lip / lit / lis / benchmarks | `./scripts/install-agent-kit.sh <repo>` after roadmap merge |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Changed
- Vision north star: go-to ecosystem for HPC, scientific computing, and AI (`docs/ecosystem/vision-and-roadmap.md`); agent-kit 1.3.1 session hooks
```
