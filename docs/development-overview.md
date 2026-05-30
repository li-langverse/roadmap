# Li development overview

**li-langverse org** · scanned **2026-05-25T19:01Z** · `gh pr list` / checks · live docs HEAD

| Metric | Value |
|--------|------:|
| Ready to merge (CI green) | 17 |
| Open PRs | 61 |
| Blocked / needs work | 39 |
| Repos with live docs | 3 / 12 |

## Recommended merge order

1. [benchmarks #97](https://github.com/li-langverse/benchmarks/pull/97) — ci(benchmarks): WP-E1 skip duplicate dashboard build on main
2. [benchmarks #99](https://github.com/li-langverse/benchmarks/pull/99) — feat(catalog): sync paths from lic benchmarks tree (WP5)
3. [benchmarks #100](https://github.com/li-langverse/benchmarks/pull/100) — fix(dashboard): 79% measured catalog rows via lic ingest
4. [benchmarks #102](https://github.com/li-langverse/benchmarks/pull/102) — fix(dashboard): SOTA relative perf charts on bench drill-down
5. [benchmarks #103](https://github.com/li-langverse/benchmarks/pull/103) — fix(ingest): clear tier0_stability unknown from stability.csv
6. [benchmarks #104](https://github.com/li-langverse/benchmarks/pull/104) — fix(ingest): tier-5 HTTP unknown rows → yellow oracle-only (WP-T5)
7. [benchmarks #106](https://github.com/li-langverse/benchmarks/pull/106) — feat(dashboard): pillar and drilldown SOTA-relative charts
8. [benchmarks #107](https://github.com/li-langverse/benchmarks/pull/107) — fix(dashboard): overview tier cards measured vs pending (WP-O)
9. [li-demo #14](https://github.com/li-langverse/li-demo/pull/14) — chore(docs): GitHub description SEO (WP-A4)
10. [li-httpd #12](https://github.com/li-langverse/li-httpd/pull/12) — chore(docs): GitHub description SEO (WP-A4)
11. [li-net #10](https://github.com/li-langverse/li-net/pull/10) — chore(docs): GitHub description SEO (WP-A4)
12. [li-std-core #7](https://github.com/li-langverse/li-std-core/pull/7) — chore(docs): GitHub description SEO (WP-A4)

## Merge when reviewed

| Priority | PR | CI | Action | Notes |
|----------|-----|-----|--------|-------|
| P0 | [benchmarks#97](https://github.com/li-langverse/benchmarks/pull/97) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#99](https://github.com/li-langverse/benchmarks/pull/99) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#100](https://github.com/li-langverse/benchmarks/pull/100) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#102](https://github.com/li-langverse/benchmarks/pull/102) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#103](https://github.com/li-langverse/benchmarks/pull/103) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#104](https://github.com/li-langverse/benchmarks/pull/104) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#106](https://github.com/li-langverse/benchmarks/pull/106) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [benchmarks#107](https://github.com/li-langverse/benchmarks/pull/107) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [li-demo#14](https://github.com/li-langverse/li-demo/pull/14) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [li-httpd#12](https://github.com/li-langverse/li-httpd/pull/12) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [li-net#10](https://github.com/li-langverse/li-net/pull/10) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [li-std-core#7](https://github.com/li-langverse/li-std-core/pull/7) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [li-std-math#8](https://github.com/li-langverse/li-std-math/pull/8) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [lic#280](https://github.com/li-langverse/lic/pull/280) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [roadmap#19](https://github.com/li-langverse/roadmap/pull/19) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [roadmap#20](https://github.com/li-langverse/roadmap/pull/20) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |
| P0 | [roadmap#21](https://github.com/li-langverse/roadmap/pull/21) | pass | Merge when approved | Auto snapshot 2026-05-25T19:01Z |

## Do not merge yet

| PR | CI | Action | Notes |
|-----|-----|--------|-------|
| [li-demo#10](https://github.com/li-langverse/li-demo/pull/10) | fail | Fix CI first | chore(deps): bump actions/checkout from 4 to 6 |
| [li-httpd#7](https://github.com/li-langverse/li-httpd/pull/7) | fail | Fix CI first | chore(deps): bump actions/checkout from 4 to 6 |
| [li-httpd#10](https://github.com/li-langverse/li-httpd/pull/10) | fail | Fix CI first | feat(li-net-httpd): plan-loop split from lic/cursor/httpd-pl |
| [li-net#6](https://github.com/li-langverse/li-net/pull/6) | fail | Fix CI first | chore(deps): bump actions/checkout from 4 to 6 |
| [li-std-core#6](https://github.com/li-langverse/li-std-core/pull/6) | fail | Fix CI first | chore(deps): bump actions/checkout from 4 to 6 |
| [li-std-math#7](https://github.com/li-langverse/li-std-math/pull/7) | fail | Fix CI first | chore(deps): bump actions/checkout from 4 to 6 |
| [lic#183](https://github.com/li-langverse/lic/pull/183) | fail | Fix CI first | feat(compiler): VC witness + policy module (compiler-only) |
| [lic#194](https://github.com/li-langverse/lic/pull/194) | fail | Fix CI first | feat(compiler-studio): wave-d-gui-scaffold — AL-9 import gui |
| [lic#254](https://github.com/li-langverse/lic/pull/254) | fail | Fix CI first | chore(verification): Phase 2a gap closure queue |
| [lic#262](https://github.com/li-langverse/lic/pull/262) | fail | Fix CI first | feat(2i): plan tracker — norm reduction shape compile_fail |
| [lic#263](https://github.com/li-langverse/lic/pull/263) | fail | Fix CI first | feat(proof-db): Phase 2b catalog lemmas + rebuild report |
| [lic#264](https://github.com/li-langverse/lic/pull/264) | fail | Fix CI first | fix(ci): resolve verify.py merge conflict on main |
| [lic#266](https://github.com/li-langverse/lic/pull/266) | fail | Fix CI first | feat(2f): P-refine guard discharge + prove_lean_ok specimens |
| [lic#268](https://github.com/li-langverse/lic/pull/268) | fail | Fix CI first | feat(plans): close tier-0 correctness plot checkbox (Phase 2 |
| [lic#269](https://github.com/li-langverse/lic/pull/269) | fail | Fix CI first | feat(sim): PH-SIM SIM-2 replay tick stub |
| [lic#271](https://github.com/li-langverse/lic/pull/271) | fail | Fix CI first | feat(demo): publish studio-verticals MP4 via GitHub Release |
| [lic#272](https://github.com/li-langverse/lic/pull/272) | fail | Fix CI first | feat(ci): package-release dispatch on v* tags |
| [lic#281](https://github.com/li-langverse/lic/pull/281) | fail | Fix CI first | feat(8p-b): parallel lic-workspace-build (gap2 plan tracker) |
| [lic#282](https://github.com/li-langverse/lic/pull/282) | fail | Fix CI first | feat(proof-db): gap2 catalog slice — three L-MATH entries +  |
| [lic#283](https://github.com/li-langverse/lic/pull/283) | fail | Fix CI first | feat(PH-AGENT-1): lis MCP stdio stub for Studio tools |
| [lic#284](https://github.com/li-langverse/lic/pull/284) | fail | Fix CI first | feat(studio): tier-2 MD oracle in scientific viewport |
| [lic#285](https://github.com/li-langverse/lic/pull/285) | fail | Fix CI first | feat(sim): li-sim-automotive drive smoke stub |
| [lic#286](https://github.com/li-langverse/lic/pull/286) | fail | Fix CI first | feat(gap2): G-par parallel-for disjoint MIR tag + P-par lemm |
| [lic#288](https://github.com/li-langverse/lic/pull/288) | fail | Fix CI first | feat(vertical-gap): wgpu readback phase A — present_blit_rgb |
| [lic#289](https://github.com/li-langverse/lic/pull/289) | fail | Fix CI first | feat(PH-SIM): SIM-3 partial — ml.rl EnvPoolStub and sim_rl s |
| [lic#291](https://github.com/li-langverse/lic/pull/291) | fail | Fix CI first | feat(PH-HW WP2): LKIR matmul CPU oracle + md_force_short pla |
| [lic#292](https://github.com/li-langverse/lic/pull/292) | fail | Fix CI first | chore(studio-ux): Wave 2 plan loop state + UX assessment |
| [lic#294](https://github.com/li-langverse/lic/pull/294) | fail | Fix CI first | feat(2f): P-float corpus gate + dedupe #185 (gap2-proof) |
| [lic#295](https://github.com/li-langverse/lic/pull/295) | fail | Fix CI first | chore(gates): align master-plan verticals with honest CI evi |
| [lic#297](https://github.com/li-langverse/lic/pull/297) | fail | Fix CI first | feat(PH-AM): sim.export.print temp G-code/3MF pipeline |
| [lic#298](https://github.com/li-langverse/lic/pull/298) | fail | Fix CI first | feat(wgpu): phase B readback scaffold (after #288) |
| [lic#299](https://github.com/li-langverse/lic/pull/299) | fail | Fix CI first | fix(check): wire resource_options_invalid exit (main CI) |
| [lic#304](https://github.com/li-langverse/lic/pull/304) | fail | Fix CI first | feat(bench): WP4 compile smokes for qm, auto, ml, viz |
| [lic#305](https://github.com/li-langverse/lic/pull/305) | fail | Fix CI first | feat(bench): WP3 tier-2 harnesses (pde, robo, drug, bio, am, |
| [lic#306](https://github.com/li-langverse/lic/pull/306) | fail | Fix CI first | feat(bench): tier1 num_* + fft_1d_fixed harnesses (WP1) |
| [lic#307](https://github.com/li-langverse/lic/pull/307) | fail | Fix CI first | feat(bench): WP2 tier2 md_* catalog harness fill (PH-5b) |
| [lic#308](https://github.com/li-langverse/lic/pull/308) | fail | Fix CI first | feat(bench): registry family harness fill + tier-7 CSV alias |
| [lic#309](https://github.com/li-langverse/lic/pull/309) | fail | Fix CI first | fix(bench): tier-2 physics Li builds (WP-T2) |
| [lis#12](https://github.com/li-langverse/lis/pull/12) | fail | Fix CI first | feat(tier5): real HTTP bench CSV (WP6 fill-all) |

## All open PRs

| Repo | # | Title | Base | CI | Ready |
|------|---|-------|------|-----|-------|
| benchmarks | 97 | [ci(benchmarks): WP-E1 skip duplicate dashboard build on main](https://github.com/li-langverse/benchmarks/pull/97) | main | pass | yes |
| benchmarks | 99 | [feat(catalog): sync paths from lic benchmarks tree (WP5)](https://github.com/li-langverse/benchmarks/pull/99) | main | pass | yes |
| benchmarks | 100 | [fix(dashboard): 79% measured catalog rows via lic ingest](https://github.com/li-langverse/benchmarks/pull/100) | main | pass | yes |
| benchmarks | 102 | [fix(dashboard): SOTA relative perf charts on bench drill-down](https://github.com/li-langverse/benchmarks/pull/102) | main | pass | yes |
| benchmarks | 103 | [fix(ingest): clear tier0_stability unknown from stability.csv](https://github.com/li-langverse/benchmarks/pull/103) | main | pass | yes |
| benchmarks | 104 | [fix(ingest): tier-5 HTTP unknown rows → yellow oracle-only (WP-T5)](https://github.com/li-langverse/benchmarks/pull/104) | main | pass | yes |
| benchmarks | 106 | [feat(dashboard): pillar and drilldown SOTA-relative charts](https://github.com/li-langverse/benchmarks/pull/106) | main | pass | yes |
| benchmarks | 107 | [fix(dashboard): overview tier cards measured vs pending (WP-O)](https://github.com/li-langverse/benchmarks/pull/107) | main | pass | yes |
| li-demo | 10 | [chore(deps): bump actions/checkout from 4 to 6](https://github.com/li-langverse/li-demo/pull/10) | main | fail | no |
| li-demo | 14 | [chore(docs): GitHub description SEO (WP-A4)](https://github.com/li-langverse/li-demo/pull/14) | main | pass | yes |
| li-httpd | 7 | [chore(deps): bump actions/checkout from 4 to 6](https://github.com/li-langverse/li-httpd/pull/7) | main | fail | no |
| li-httpd | 10 | [feat(li-net-httpd): plan-loop split from lic/cursor/httpd-plan-continu…](https://github.com/li-langverse/li-httpd/pull/10) | main | fail | no |
| li-httpd | 12 | [chore(docs): GitHub description SEO (WP-A4)](https://github.com/li-langverse/li-httpd/pull/12) | main | pass | yes |
| li-net | 6 | [chore(deps): bump actions/checkout from 4 to 6](https://github.com/li-langverse/li-net/pull/6) | main | fail | no |
| li-net | 10 | [chore(docs): GitHub description SEO (WP-A4)](https://github.com/li-langverse/li-net/pull/10) | main | pass | yes |
| li-std-core | 6 | [chore(deps): bump actions/checkout from 4 to 6](https://github.com/li-langverse/li-std-core/pull/6) | main | fail | no |
| li-std-core | 7 | [chore(docs): GitHub description SEO (WP-A4)](https://github.com/li-langverse/li-std-core/pull/7) | main | pass | yes |
| li-std-math | 7 | [chore(deps): bump actions/checkout from 4 to 6](https://github.com/li-langverse/li-std-math/pull/7) | main | fail | no |
| li-std-math | 8 | [chore(docs): GitHub description SEO (WP-A4)](https://github.com/li-langverse/li-std-math/pull/8) | main | pass | yes |
| lic | 183 | [feat(compiler): VC witness + policy module (compiler-only)](https://github.com/li-langverse/lic/pull/183) | main | fail | no |
| lic | 188 | [feat(sim): num_dot_axpy (algo_id=1) — li-math-numerics smoke](https://github.com/li-langverse/lic/pull/188) | main | none | no |
| lic | 194 | [feat(compiler-studio): wave-d-gui-scaffold — AL-9 import gui](https://github.com/li-langverse/lic/pull/194) | main | fail | no |
| lic | 254 | [chore(verification): Phase 2a gap closure queue](https://github.com/li-langverse/lic/pull/254) | main | fail | no |
| lic | 262 | [feat(2i): plan tracker — norm reduction shape compile_fail](https://github.com/li-langverse/lic/pull/262) | main | fail | no |
| lic | 263 | [feat(proof-db): Phase 2b catalog lemmas + rebuild report](https://github.com/li-langverse/lic/pull/263) | main | fail | no |
| lic | 264 | [fix(ci): resolve verify.py merge conflict on main](https://github.com/li-langverse/lic/pull/264) | main | fail | no |
| lic | 266 | [feat(2f): P-refine guard discharge + prove_lean_ok specimens](https://github.com/li-langverse/lic/pull/266) | main | fail | no |
| lic | 268 | [feat(plans): close tier-0 correctness plot checkbox (Phase 2b)](https://github.com/li-langverse/lic/pull/268) | main | fail | no |
| lic | 269 | [feat(sim): PH-SIM SIM-2 replay tick stub](https://github.com/li-langverse/lic/pull/269) | main | fail | no |
| lic | 271 | [feat(demo): publish studio-verticals MP4 via GitHub Release](https://github.com/li-langverse/lic/pull/271) | main | fail | no |
| lic | 272 | [feat(ci): package-release dispatch on v* tags](https://github.com/li-langverse/lic/pull/272) | main | fail | no |
| lic | 280 | [feat(proof-db): lemma rebuild pipeline and math seed](https://github.com/li-langverse/lic/pull/280) | main | pass | yes |
| lic | 281 | [feat(8p-b): parallel lic-workspace-build (gap2 plan tracker)](https://github.com/li-langverse/lic/pull/281) | main | fail | no |
| lic | 282 | [feat(proof-db): gap2 catalog slice — three L-MATH entries + report](https://github.com/li-langverse/lic/pull/282) | main | fail | no |
| lic | 283 | [feat(PH-AGENT-1): lis MCP stdio stub for Studio tools](https://github.com/li-langverse/lic/pull/283) | main | fail | no |
| lic | 284 | [feat(studio): tier-2 MD oracle in scientific viewport](https://github.com/li-langverse/lic/pull/284) | main | fail | no |
| lic | 285 | [feat(sim): li-sim-automotive drive smoke stub](https://github.com/li-langverse/lic/pull/285) | main | fail | no |
| lic | 286 | [feat(gap2): G-par parallel-for disjoint MIR tag + P-par lemma](https://github.com/li-langverse/lic/pull/286) | main | fail | no |
| lic | 288 | [feat(vertical-gap): wgpu readback phase A — present_blit_rgba8](https://github.com/li-langverse/lic/pull/288) | main | fail | no |
| lic | 289 | [feat(PH-SIM): SIM-3 partial — ml.rl EnvPoolStub and sim_rl studio rout…](https://github.com/li-langverse/lic/pull/289) | main | fail | no |
| lic | 291 | [feat(PH-HW WP2): LKIR matmul CPU oracle + md_force_short placeholder](https://github.com/li-langverse/lic/pull/291) | main | fail | no |
| lic | 292 | [chore(studio-ux): Wave 2 plan loop state + UX assessment](https://github.com/li-langverse/lic/pull/292) | main | fail | no |
| lic | 294 | [feat(2f): P-float corpus gate + dedupe #185 (gap2-proof)](https://github.com/li-langverse/lic/pull/294) | main | fail | no |
| lic | 295 | [chore(gates): align master-plan verticals with honest CI evidence](https://github.com/li-langverse/lic/pull/295) | main | fail | no |
| lic | 297 | [feat(PH-AM): sim.export.print temp G-code/3MF pipeline](https://github.com/li-langverse/lic/pull/297) | main | fail | no |
| lic | 298 | [feat(wgpu): phase B readback scaffold (after #288)](https://github.com/li-langverse/lic/pull/298) | main | fail | no |
| lic | 299 | [fix(check): wire resource_options_invalid exit (main CI)](https://github.com/li-langverse/lic/pull/299) | main | fail | no |
| lic | 301 | [ci(lic): WP-C1–C5 lic-ci image, build cache, package-ci](https://github.com/li-langverse/lic/pull/301) | main | none | no |
| lic | 304 | [feat(bench): WP4 compile smokes for qm, auto, ml, viz](https://github.com/li-langverse/lic/pull/304) | main | fail | no |
| lic | 305 | [feat(bench): WP3 tier-2 harnesses (pde, robo, drug, bio, am, fluid)](https://github.com/li-langverse/lic/pull/305) | main | fail | no |
| lic | 306 | [feat(bench): tier1 num_* + fft_1d_fixed harnesses (WP1)](https://github.com/li-langverse/lic/pull/306) | main | fail | no |
| lic | 307 | [feat(bench): WP2 tier2 md_* catalog harness fill (PH-5b)](https://github.com/li-langverse/lic/pull/307) | main | fail | no |
| lic | 308 | [feat(bench): registry family harness fill + tier-7 CSV aliases](https://github.com/li-langverse/lic/pull/308) | main | fail | no |
| lic | 309 | [fix(bench): tier-2 physics Li builds (WP-T2)](https://github.com/li-langverse/lic/pull/309) | main | fail | no |
| lic | 310 | [docs(research/md): md-r0-sota-survey — MD algorithm SOTA map](https://github.com/li-langverse/lic/pull/310) | main | none | no |
| lic | 311 | [docs(numerics): chem-r0 QM SOTA survey (401-432)](https://github.com/li-langverse/lic/pull/311) | main | none | no |
| lic | 312 | [feat(httpd): close gap-phase2-mitigation-exploits (tier5 nginx mitigat…](https://github.com/li-langverse/lic/pull/312) | main | none | no |
| lis | 12 | [feat(tier5): real HTTP bench CSV (WP6 fill-all)](https://github.com/li-langverse/lis/pull/12) | main | fail | no |
| roadmap | 19 | [docs(ecosystem): point compiler to lic (WP-A5)](https://github.com/li-langverse/roadmap/pull/19) | main | pass | yes |
| roadmap | 20 | [chore(agent-kit): adopt 1.3.3 in roadmap (WP-A1)](https://github.com/li-langverse/roadmap/pull/20) | main | pass | yes |
| roadmap | 21 | [docs(ecosystem): httpd mirror canonical decision (WP-B4)](https://github.com/li-langverse/roadmap/pull/21) | main | pass | yes |

---

*Agents do not merge governance PRs without owner sign-off. Never push directly to protected `main`.*

*Snapshot: `./scripts/regenerate-development-overview-md.py` then `./scripts/deploy-pages-local.sh --build`. Live queue: browser on [development overview](https://li-langverse.github.io/roadmap/development-overview/) — no redeploy for queue-only changes.*
