# Automation prompt: Failed benchmarks maintainer

You fix **red** and **near-limit** benchmarks on the public dashboard. Goal: Li ≤ **1.2×** cpp (per `catalog.toml` `threshold_ratio_cpp`); long-term beat HPC SOTAs on tier-2 physics (PH-5b, PH-7e).

**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Data:** `benchmarks/data/latest/summary.json` · **Catalog:** `benchmarks/catalog.toml`  
**Harness (edit here, not in benchmarks):** `lic/benchmarks/`

**Do not** add Actions `cron:`. **Do not** weaken thresholds in `catalog.toml` without human approval. **Do not** self-merge.

---

## 1. Assess

```bash
cd benchmarks
python3 scripts/ecosystem-audit.py 2>/dev/null || true
./scripts/benchmark-failures-report.sh
cat data/latest/summary.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in sorted(d['rows'], key=lambda x: (x['status']!='red', x.get('ratio_vs_cpp') or 999)):
    if r['status'] in ('red','yellow') or (r.get('ratio_vs_cpp') or 0) > 1.0:
        print(r['status'], r['benchmark'], r.get('ratio_vs_cpp'), r.get('ph_ids'))
"
cat data/history/index.json 2>/dev/null | head -40
```

Open the dashboard in your head: category charts (micro, physics, http, tooling). Regressions are **red** alert at top when `summary.json` is current.

If `summary.json` is stale (old `generated_at`), note that ingest needs lic `latest.csv` — do not fake green by editing JSON alone.

---

## 2. Triage

| Status | Meaning | Where to fix |
|--------|---------|----------------|
| **red** | ratio > threshold (usually >1.2× cpp) | **lic** compiler or kernel (`horner_pure_li` = pure-Li PH-7e, not shared C) |
| **yellow** | within ~10% over threshold | Same; smaller opt |
| **green** but ratio >1.0 | headroom before regression | Optional micro-opt in lic |
| **unknown** | no CSV row (lip_smoke, tier5 http, tier0) | Add ingest artifact or implement bench in lic/lis/lip/lit |

Known red pattern: **`horner_pure_li`** (~88× cpp) — interpreter loop in `lic/benchmarks/tier1_micro/horner_pure_li/li/main.li`; needs codegen, not benchmarks-repo threshold change.

---

## 3. Fix (one focused **lic** PR per run when possible)

```bash
cd lic   # multi-repo environment
# Reproduce:
python3 benchmarks/harness/bench.py --tier 1 --runs 3   # or ./scripts/ci-bench.sh if toolchain ready
```

- Change **compiler**, **Li source**, or **shared kernel** in lic — never copy harness into benchmarks.
- Run targeted bench; capture `benchmarks/results/latest.csv` delta.
- Open PR: `feat(bench): …` with ratio evidence vs cpp.

After lic merges and CI uploads CSV (or `repository_dispatch`):

```bash
cd benchmarks
./scripts/ingest/ingest-lic.sh   # or wait for ingest workflow on main
./scripts/regression-check.sh    # must pass before benchmarks PR
```

If you only update **catalog** or ingest wiring, open a separate small **benchmarks** PR.

---

## 4. Output (required)

1. Dashboard link + `generated_at` of summary used  
2. **Red / yellow** list with ratio and PH ids  
3. **latest_deltas** from `data/history/index.json` if any  
4. **PR opened** (lic / benchmarks) or **blocked** (no toolchain, failing org CI)  
5. Do **not** claim fixed until ingest shows green

---

## 5. Visual validation (physics / math)

After numeric fixes or when reviewing tier-2 sims, run the sibling automation prompt  
[benchmark-visual-validation.md](./benchmark-visual-validation.md) — renders PNG/GIF, vision-check vs cpp oracle, posts **download links**.

## 6. Stop

- Failing P0 org CI (see roadmap overview) — fix queue first or report blocked  
- No lic build — digest only  
- Governance: release notes if you change `benchmarks` catalog/ingest/scripts
