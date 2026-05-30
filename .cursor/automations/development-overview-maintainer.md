# Automation prompt: Development overview maintainer

You maintain the **li-langverse** org using the live dashboard and snapshot:

- **Live (browser):** https://li-langverse.github.io/roadmap/development-overview/
- **Snapshot source:** `docs/development-overview.md` in **roadmap**
- **Vision:** [lic master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) — PH-5b benchmarks, PH-7e codegen, package CI before Dependabot

**Do not** add scheduled GitHub Actions (`cron:`). **Do not** put tokens in client-side JS.

---

## 1. Assess (every run)

```bash
cd roadmap   # this repo
chmod +x scripts/*.sh

# Live queue + org scan (offline; mirrors what the website shows)
./scripts/refresh-development-overview.sh
python3 scripts/compute-ecosystem-stats.py
cat data/development-overview/status.json | head -80
cat data/development-overview/history.json | tail -40

# Optional cross-check from benchmarks (if checked out)
if [ -d ../benchmarks ]; then
  python3 ../benchmarks/scripts/ecosystem-audit.py 2>/dev/null || true
  cat ../benchmarks/data/latest/ecosystem-audit.json 2>/dev/null | head -60
fi
```

Use `gh` to validate:

```bash
# Failed CI on open PRs
for r in lic li-language li-net li-httpd li-std-core li-std-math li-demo benchmarks lit roadmap; do
  gh pr list --repo "li-langverse/$r" --state open --json number,title,statusCheckRollup,isDraft \
    --jq '.[] | select(.isDraft|not) | select([.statusCheckRollup[]?.conclusion] | any(. == "FAILURE")) | "\($r):\(.number) \(.title)"' 2>/dev/null
done

# Missing ci.yml on main
for r in $(grep -v '^#' .github/li-org-repos.txt); do
  gh api "repos/li-langverse/$r/contents/.github/workflows" -q '.[].name' 2>/dev/null | grep -q '\.yml' || echo "missing CI workflows on main: $r"
done
```

Open the live site mentally against snapshot tables: branch CI gaps, missing live docs, merge order.

---

## 2. Fix (priority order)

Work only what you can finish in one run; open **focused PRs** per repo.

| P | Issue | Action |
|---|--------|--------|
| **P0** | Failing CI on lic#1, li-language#5 (often **Windows** / memory-linux) | Open or update fix PR in **lic** / **li-language**; do not merge |
| **P0** | Package mirrors: no `ci.yml` on `main` | Ensure CI setup PR (#2) is ready; **do not** merge Dependabot #1 first |
| **P1** | Missing live docs (lic, lip, lit, roadmap was none until Pages) | Add minimal GitHub Pages or link to li-language handbook where appropriate — **small PRs** |
| **P1** | Red benchmarks (`horner_pure_li`) | Fix in **lic** (PH-7e pure-Li), not threshold games in benchmarks |
| **P2** | Stale snapshot | Edit `docs/development-overview.md` (metrics, tables, merge order) when org state changed materially |

After editing the snapshot:

```bash
./scripts/gen-development-overview.sh
./scripts/deploy-pages-local.sh --build   # no Actions; or merge to main + pages.yml
```

Live PR queue (`development-overview-live.js`) does **not** need redeploy — browser polls GitHub API.
Optional offline mirror: `./scripts/refresh-development-overview.sh` → `data/development-overview/status.json` (agents only).

---

## 3. Output (required)

Post a short run summary (Slack / PR comment / automation memory):

1. **Failed PRs** — repo#n + failing check name + link
2. **Missing CI on main** — repo list
3. **Missing / down live docs** — repo list
4. **Ready to merge** — ordered list (human merges only)
5. **PRs you opened** — links or “none”
6. **Blocked** — what needs human (org settings, merge approval)

---

## 4. Stop conditions

- Do **not** `gh pr merge` your own PRs.
- Do **not** push to protected `main`.
- Do **not** weaken `agent-kit` hooks or skip release notes on merge-worthy roadmap changes.
- If only digest is possible (no safe fix), stop after §3.

---

## 5. Release notes (roadmap changes only)

If you change `docs/**`, workflows, or scripts on **roadmap**:

- `docs/release-notes/YYYY-MM-DD-<slug>.md` from template
- `CHANGELOG.md` under `[Unreleased]`
- PR body: Summary + Agent continuation
