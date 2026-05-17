# Cursor Automations (not GitHub Actions cron)

Heavy recurring ops run as **[Cursor Automations](https://cursor.com/automations)** (cloud agents) so we stay inside the GitHub Actions free budget. Create each automation in the Cursor UI and paste the prompt from the matching file below.

| Automation | Trigger (suggested) | Prompt file | Primary repo |
|------------|---------------------|-------------|--------------|
| **Development overview maintainer** | Every 12h or daily | [development-overview-maintainer.md](./development-overview-maintainer.md) | `roadmap` (+ fixes in org repos) |
| **Issue feature planner** | 2×/week per repo (or org sweep) | [issue-feature-planner.md](./issue-feature-planner.md) + [repos/](./repos/) | all · skills: `plan-feature-from-issue` |
| **Plan completion audit** | Weekly | [plan-completion-audit.md](./plan-completion-audit.md) | `benchmarks` + `lic` · skill: `audit-plan-completion` |
| **Benchmark visuals** | Weekly or after lic bench / manual | [benchmark-visual-validation.md](./benchmark-visual-validation.md) | `lic` + `benchmarks` |
| **Failed benchmarks** | Schedule: weekly, or webhook after lic bench | [failed-benchmarks-maintainer.md](./failed-benchmarks-maintainer.md) | `lic` (+ `benchmarks` ingest) |
| Ecosystem health | Schedule: daily or every 12h | [ecosystem-health.md](./ecosystem-health.md) | `benchmarks` (+ `roadmap` read) |
| Benchmark improvement | Same as failed benchmarks (alias) | [benchmark-improvement.md](./benchmark-improvement.md) | `lic` |
| Merge queue digest | Schedule: daily | [merge-queue-digest.md](./merge-queue-digest.md) | `roadmap` |

**Live development overview:** https://li-langverse.github.io/roadmap/development-overview/ (browser GitHub API — no Actions cron for queue refresh).

**Benchmarks dashboard:** https://li-langverse.github.io/benchmarks/ — local report: `./scripts/benchmark-failures-report.sh`

**Setup guide:** [docs/ecosystem/agent-automations.md](../docs/ecosystem/agent-automations.md) (in **benchmarks** repo on `main`)

## Development overview maintainer (detail)

| Field | Value |
|-------|--------|
| **Name** | Li development overview maintainer |
| **Repository** | `li-langverse/roadmap` |
| **Multi-repo** (optional) | `benchmarks`, `lic`, package mirrors for CI fixes |
| **Trigger** | Schedule: **every 12 hours** (or daily) |
| **Tools** | Open pull request, Comment on pull request (optional) |
| **Prompt** | Copy entire contents of [development-overview-maintainer.md](./development-overview-maintainer.md) |

## Policy

- **Do not** add `cron:` workflows for audits or queue refresh on `roadmap` / `benchmarks` (Actions budget).
- **Do not** embed GitHub tokens in `development-overview-live.js` (browser uses public API only).
- **Do not** self-merge PRs on protected branches.
- **Conflicts:** skill `resolve-merge-conflicts` — preserve both `main` and branch progress.

## GitHub Actions we keep (critical path)

See [docs/ecosystem/actions-budget.md](../docs/ecosystem/actions-budget.md) for minute estimates.
