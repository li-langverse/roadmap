# Automation prompt: Merge queue digest

Repo: **roadmap** (or multi-repo with roadmap + benchmarks read-only).

## Run

Live queue is **browser JavaScript** on the Pages site (GitHub API) — no cron needed.

Update snapshot when branch CI / ecosystem tables change:

```bash
cd roadmap
# edit docs/development-overview.md
./scripts/gen-development-overview.sh
```

Optional offline: `./scripts/refresh-development-overview.sh` (agents only).

## Output

Digest for human review:

- Ready to merge (CI green, not draft) in vision order: package CI PRs → benchmarks#1 → lic dev→main
- Failed PRs — which check failed (Windows, memory-linux, etc.)
- Repos still missing `ci.yml` on `main` or live docs

## Do not

- Self-merge PRs
- Add GitHub Actions `schedule:` cron (use this Cursor automation instead)
- Push directly to protected branches

Update `docs/development-overview.md` snapshot only when branch CI / ecosystem tables materially changed.
