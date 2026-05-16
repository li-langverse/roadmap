# Automation prompt: Benchmark improvement

**Prefer the full prompt:** [failed-benchmarks-maintainer.md](./failed-benchmarks-maintainer.md) (dashboard reds, triage table, ingest path).

Goal: Li ≤1.2× cpp on tier-1/2 catalog rows; beat HPC SOTAs where shared kernels allow. Pure-Li gaps need **lic** codegen (PH-7e).

**Dashboard:** https://li-langverse.github.io/benchmarks/

## Read

- `benchmarks/data/latest/summary.json` and `data/history/index.json` (`latest_deltas`)
- `./scripts/benchmark-failures-report.sh`
- `benchmarks/catalog.toml`
- `lic/docs/benchmarks.md`, `lic/benchmarks/harness/`

## Run (lic repo)

```bash
# If toolchain available:
./scripts/ci-bench.sh   # or harness subset
python3 benchmarks/harness/bench.py --tier 1 --runs 3
```

## Focus

1. **Red** rows first (`horner_pure_li` = pure-Li loop — interpreter/codegen, not C kernel).
2. **Near threshold** greens with ratio >1.0 (matmul_blocked, nbody_gravity, etc.) — micro-opts in Li or shared kernel only if provably correct.
3. Do **not** weaken `threshold_ratio_cpp` in benchmarks without human approval.

## Then

- Open **lic** PR with bench evidence; update CSV via normal lic CI artifact path.
- In **benchmarks**, run ingest only after lic publishes `latest.csv` (repository_dispatch — do not add Actions cron).

## Stop if

Merge queue has failing P0 CI or no lic build available — report blocked items instead.
