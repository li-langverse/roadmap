# Automation prompt: Benchmark visual validation (math & physics)

Produce **visual evidence** that Li simulations track **cpp/rust/julia** (shared C kernels) and are not obviously unphysical. Deliver **download links** in your run summary and PR.

**Dashboard (numbers):** https://li-langverse.github.io/benchmarks/  
**Harness:** `lic/benchmarks/` — **do not** copy harness into `benchmarks`.

**Do not** add Actions `cron:`. **Do not** self-merge.

---

## 1. Render visuals

```bash
cd benchmarks
chmod +x scripts/render-benchmark-visuals.sh scripts/visual-manifest.py
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh
cat data/visuals/latest/manifest.json
ls -la data/visuals/latest/
```

Requires **lic** checkout + matplotlib venv (plot_shareables creates `.venv-plot` in lic).

If lic toolchain missing: run what you can (`bench.py --sample` in lic for demo CSV only) and state **blocked** — do not claim physics validated.

---

## 2. Vision review (required)

Open every file listed under `physics_priority` in `manifest.json`, then all `*.gif` and tier-2 PNGs. Use **image recognition** / multimodal analysis.

### Pass / fail heuristics

| Asset | OK | Obviously off (fail) |
|-------|----|----------------------|
| `md_lennard_jones_*.gif` | Compact fluid-like cluster; smooth motion; langs similar morphology | Explosion, flying particles, empty box, frozen frame |
| `md_lennard_jones_energy_*.png` | Energy drift bounded; Li tracks cpp overlay | Li curve diverges, NaN, vertical spike |
| `bench_speed_tier2.png` / `speedup_vs_cpp.png` | Li bar within ~1.2× cpp for physics rows | Li 10×+ slower with no known codegen excuse |
| `md_stability_by_lang.png` | Li passes like cpp | Li fail while cpp pass |
| Micro tier1 bars | horner may be slow; simd/matmul should be near cpp | — |

**SOTA framing:** cpp/rust/julia run the **same** `common/*_core.c`; they are the oracle. Li must match **physics shape**, not necessarily win on wall_time yet.

Grid benches (`heat_equation_2d`, `wave_equation_1d`): if only speed plots exist, note “grid animation not wired — speed-only check” in report.

---

## 3. Cross-check numbers

```bash
./scripts/benchmark-failures-report.sh
```

Red rows must be mentioned in the visual report (e.g. `horner_pure_li`).

---

## 4. Publish download links

1. Create branch `cursor/bench-visuals-YYYYMMDD` on **benchmarks** (or attach to an open **lic** bench PR).
2. `git add data/visuals/latest/` (PNG/GIF + manifest + zip). **Avoid** committing 50MB+ without need; prefer zip + key PNGs.
3. Push and open/update PR.

In PR description and automation output, paste **clickable raw links** (replace `BRANCH`):

```text
Bundle: https://raw.githubusercontent.com/li-langverse/benchmarks/BRANCH/data/visuals/latest/benchmark-visuals-*.zip
MD overlay: https://raw.githubusercontent.com/li-langverse/benchmarks/BRANCH/data/visuals/latest/md_lennard_jones_energy_overlay.png
Tier-2 speeds: https://raw.githubusercontent.com/li-langverse/benchmarks/BRANCH/data/visuals/latest/bench_speed_tier2.png
```

If Cursor provides **artifact URLs** from the cloud run, include those too (preferred for large GIFs).

**Optional:** attach 2–4 key images inline in the PR body so humans need not download first.

---

## 5. Required output format

Post this summary every run:

1. **Verdict:** PASS / FAIL / BLOCKED per physics benchmark reviewed  
2. **Vision notes:** 3–6 bullets (what you saw; Li vs cpp)  
3. **Download links:** zip + top 5 files  
4. **Dashboard:** link + whether `summary.json` is stale  
5. **Follow-up PR:** lic fix needed? (PH-7e / kernel / params)

---

## 6. Fix loop (if FAIL)

- Open **lic** PR with fix + re-run `render-benchmark-visuals.sh` on updated branch  
- Do not relax `threshold_ratio_cpp` in benchmarks without human approval  
- Re-run vision on new GIFs before claiming fixed

---

## 7. Stop

- No lic checkout / no plots generated → BLOCKED digest only  
- Do not merge your own PRs
