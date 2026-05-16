# Agent instructions (roadmap)

1. Read `docs/ecosystem/engineering-standards.md` — **functionality, security, performance**.
2. Read `docs/ecosystem/vision-and-roadmap.md` and `docs/roadmap/milestones.md`.
3. Read [lic master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) for current **PH-**.
4. **PR-only:** branch → PR → CI green → **stop** (do not merge your own PR).
5. **READ** governance docs; **EDIT** `agent-kit/**` via PR only; **DRAFT** `docs/**` and `proposals/**` for human merge.
6. After agent-kit changes: bump `agent-kit/manifest.toml`, run `./scripts/install-agent-kit.sh lic` in a **lic** PR.
7. Perf status: https://li-langverse.github.io/benchmarks/

**Never:** push to `main`, `gh pr merge` on your PR, `--no-verify`, weaken `guard-*.sh` without human approval.
