# Cursor Automations — development overview maintainer

Create these at **[cursor.com/automations](https://cursor.com/automations)** (not GitHub Actions `schedule:` — saves Actions budget).

## Recommended automation

| Field | Value |
|-------|--------|
| **Name** | Li development overview maintainer |
| **Repository** | `li-langverse/roadmap` |
| **Multi-repo** (optional) | `li-langverse/benchmarks`, `li-langverse/lic`, `li-langverse/li-net`, `li-langverse/li-httpd`, `li-std-core`, `li-std-math`, `li-demo` as needed for fixes |
| **Trigger** | Schedule: **every 12 hours** (or daily) |
| **Tools** | Open pull request, Comment on pull request (optional) |
| **Prompt** | Copy entire contents of [development-overview-maintainer.md](./development-overview-maintainer.md) |

**Live dashboard:** https://li-langverse.github.io/roadmap/development-overview/

## Optional second automation

| Name | Trigger | Prompt |
|------|---------|--------|
| Benchmark improvement | Weekly | Use `benchmarks` repo: `.cursor/automations/benchmark-improvement.md` from [benchmarks](https://github.com/li-langverse/benchmarks) |

## Policy

- **Do not** add `cron:` workflows for audits or queue refresh on `roadmap` / `benchmarks`.
- **Do not** embed GitHub tokens in `development-overview-live.js` (browser uses public API only).
- **Do not** self-merge PRs on protected branches.
