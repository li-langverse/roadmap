# Li development overview

**li-langverse org** · scanned **2026-06-10T10:13Z** · gitlab snapshot · live queue via status.json

| Metric | Value |
|--------|------:|
| Open issues (GitLab) | 17 |
| Ready to merge (CI green) | 34 |
| Open MRs / PRs | 161 |
| Blocked / needs work | 0 |

## Recommended merge order

1. [li-httpd #1](https://gitlab.lilangverse.xyz/li-langverse/li-httpd/-/merge_requests/1) — chore(li-httpd): Code implementer automated update
2. [li-research-ingest #1](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) — fix(research): R1b ingest state blocker diagnostics + S2 key gate verifi
3. [lic #125](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/125) — feat(ph-sci): WP-SCI-03 tier-2 registry   WP-PLAT-05 MD oracle stub
4. [lic #126](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/126) — feat(ph-sci): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD oracle stub
5. [lic #129](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/129) — feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dispa
6. [lic #132](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/132) — feat(ph-sci): WP-SCI-GPU-VENDOR-02 MD grid device-buffer bind
7. [lic #133](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/133) — feat(ph-sci): WP-SCI-GPU-VENDOR-02 MD grid device-buffer bind
8. [lic #134](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/134) — feat(PH-7e): scalar FMA HornerConstLoopF64 + trip-edge li-tests (lic#11)
9. [lic #135](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/135) — docs(plan): link G-* gaps in phase 03/07 exit gates (lic#9)
10. [lic #136](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/136) — feat(container): extern-def container seam — P0–P3 (seam, li-oci, li-con
11. [lic #137](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/137) — fix(httpd): post-#677 TLS/httpd follow-ups (dual listen, config validati
12. [lic #138](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/138) — chore(std): PH-IO-4 std.io/csv regression gate

## Merge when reviewed

| Priority | MR/PR | CI | Action | Notes |
|----------|-------|-----|--------|-------|
| P0 | [li-httpd#1](https://gitlab.lilangverse.xyz/li-langverse/li-httpd/-/merge_requests/1) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [li-research-ingest#1](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#125](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/125) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#126](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/126) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#129](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/129) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#132](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/132) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#133](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/133) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#134](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/134) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#135](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/135) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#136](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/136) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#137](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/137) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#138](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/138) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#139](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/139) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#140](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/140) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#141](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/141) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#142](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/142) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#143](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/143) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#144](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/144) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#145](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/145) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |
| P0 | [lic#146](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/146) | pass | Merge when approved | snapshot 2026-06-10T10:13Z |

## Do not merge yet

| MR/PR | CI | Action | Notes |
|-------|-----|--------|-------|
| — | — | — | No failing open MRs |

## All open MRs / PRs

| Repo | # | Title | Base | CI | Ready |
|------|---|-------|------|-----|-------|
| li-httpd | 1 | [chore(li-httpd): Code implementer automated update](https://gitlab.lilangverse.xyz/li-langverse/li-httpd/-/merge_requests/1) | main | pass | yes |
| li-os | 1 | [feat(kernel): LiOS M2 — QEMU dev-vm, virtio, physmap bump alloc](https://gitlab.lilangverse.xyz/li-langverse/li-os/-/merge_requests/1) | main | none | no |
| li-os | 2 | [feat(kernel): LiOS M2 — QEMU dev-vm, virtio-mmio, physmap bump alloc](https://gitlab.lilangverse.xyz/li-langverse/li-os/-/merge_requests/2) | cursor/lios-kernel-m1 | none | no |
| li-research-ingest | 1 | [fix(research): R1b ingest state blocker diagnostics + S2 key gate veri…](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) | main | pass | yes |
| lic | 1 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch (s…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/1) | main | none | no |
| lic | 2 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry oracles](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/2) | main | none | no |
| lic | 3 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/3) | main | none | no |
| lic | 4 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/4) | main | none | no |
| lic | 5 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/5) | main | none | no |
| lic | 6 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/6) | main | none | no |
| lic | 7 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/7) | main | none | no |
| lic | 8 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/8) | main | none | no |
| lic | 9 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/9) | main | none | no |
| lic | 10 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/10) | main | none | no |
| lic | 11 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/11) | main | none | no |
| lic | 12 | [feat(sim-scientific): WP-SCI-03 QM tier-2 run_algo_registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/12) | main | none | no |
| lic | 13 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/13) | main | none | no |
| lic | 14 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/14) | main | none | no |
| lic | 15 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/15) | main | none | no |
| lic | 16 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch (P…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/16) | main | none | no |
| lic | 17 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/17) | main | none | no |
| lic | 18 | [docs(li-parallel): post-merge GOAL_COMPLETE audit trail (pass 9)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/18) | main | none | no |
| lic | 19 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/19) | main | none | no |
| lic | 20 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/20) | main | none | no |
| lic | 21 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/21) | main | none | no |
| lic | 22 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/22) | main | none | no |
| lic | 23 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/23) | main | none | no |
| lic | 24 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/24) | main | none | no |
| lic | 25 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/25) | main | none | no |
| lic | 26 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/26) | main | none | no |
| lic | 27 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/27) | main | none | no |
| lic | 28 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/28) | main | none | no |
| lic | 29 | [feat(sim-scientific): WP-SCI-03 QM/CFD/FEA tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/29) | main | none | no |
| lic | 30 | [feat(sim-scientific): WP-SCI-03 Phase 2 QM/CFD/FEA tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/30) | main | none | no |
| lic | 31 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/31) | main | none | no |
| lic | 32 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/32) | main | none | no |
| lic | 33 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/33) | main | none | no |
| lic | 34 | [feat(ph-sci): Phase 2 WP-PLAT-05 MD oracle + WP-SCI-03 CFD/FEA/QM regi…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/34) | main | none | no |
| lic | 35 | [feat(sim-scientific): WP-SCI-03 Phase 2 QM/CFD/FEA tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/35) | main | none | no |
| lic | 36 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/36) | main | none | no |
| lic | 37 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/37) | main | none | no |
| lic | 38 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/38) | main | none | no |
| lic | 39 | [feat(sim-scientific): WP-SCI-03   WP-PLAT-05 Phase 2 tier-2 oracles](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/39) | main | none | no |
| lic | 40 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/40) | main | none | no |
| lic | 41 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/41) | main | none | no |
| lic | 42 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/42) | main | none | no |
| lic | 43 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/43) | main | none | no |
| lic | 45 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/45) | main | none | no |
| lic | 46 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/46) | main | none | no |
| lic | 47 | [feat(sim-scientific): WP-SCI-03 QM tier-2 run_algo_registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/47) | main | none | no |
| lic | 48 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/48) | main | none | no |
| lic | 49 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/49) | main | none | no |
| lic | 50 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/50) | main | none | no |
| lic | 51 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/51) | main | none | no |
| lic | 52 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/52) | main | none | no |
| lic | 53 | [feat(sim-scientific): WP-SCI-03 tier-2 QM/CFD/FEA registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/53) | main | none | no |
| lic | 54 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/54) | main | none | no |
| lic | 55 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/55) | main | none | no |
| lic | 56 | [feat(sim-scientific): WP-SCI-03 Phase 2 QM/CFD/FEA tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/56) | main | none | no |
| lic | 58 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/58) | main | none | no |
| lic | 59 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry ker…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/59) | main | none | no |
| lic | 60 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/60) | main | none | no |
| lic | 61 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM + WP-PLAT-05 MD oracle stub](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/61) | main | none | no |
| lic | 62 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/62) | main | none | no |
| lic | 63 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/63) | main | none | no |
| lic | 64 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/64) | main | none | no |
| lic | 65 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry (clean)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/65) | main | none | no |
| lic | 66 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/66) | main | none | no |
| lic | 67 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/67) | main | none | no |
| lic | 68 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/68) | main | none | no |
| lic | 69 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/69) | main | none | no |
| lic | 70 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/70) | main | none | no |
| lic | 71 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/71) | main | none | no |
| lic | 72 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/72) | main | none | no |
| lic | 73 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/73) | main | none | no |
| lic | 74 | [feat(sim-scientific): WP-SCI-03 Phase 2 QM/CFD/FEA tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/74) | main | none | no |
| lic | 75 | [feat(sim-scientific): WP-SCI-03 QM tier-2 run_algo_registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/75) | main | none | no |
| lic | 76 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/76) | main | none | no |
| lic | 77 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/77) | main | none | no |
| lic | 78 | [feat(sim-scientific): WP-SCI-03 QM tier-2 registry dispatch (401–432)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/78) | main | none | no |
| lic | 79 | [feat(sim-scientific): WP-SCI-03   WP-PLAT-05 Phase 2 tier-2 registry  …](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/79) | main | none | no |
| lic | 80 | [feat(sim-scientific): WP-SCI-03 QM tier-2 registry dispatch (401–432)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/80) | main | none | no |
| lic | 81 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/81) | main | none | no |
| lic | 82 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/82) | main | none | no |
| lic | 83 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/83) | main | none | no |
| lic | 84 | [feat(sim-scientific): WP-SCI-03 Phase 2 QM/CFD/FEA tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/84) | main | none | no |
| lic | 85 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry + WP-PLAT-0…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/85) | main | none | no |
| lic | 86 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/86) | main | none | no |
| lic | 87 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry ker…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/87) | main | none | no |
| lic | 88 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/88) | main | none | no |
| lic | 89 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/89) | main | none | no |
| lic | 90 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/90) | main | none | no |
| lic | 91 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/91) | main | none | no |
| lic | 92 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/92) | main | none | no |
| lic | 93 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/93) | main | none | no |
| lic | 94 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/94) | main | none | no |
| lic | 95 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/95) | main | none | no |
| lic | 96 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/96) | main | none | no |
| lic | 97 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/97) | main | none | no |
| lic | 98 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/98) | main | none | no |
| lic | 99 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/99) | main | none | no |
| lic | 100 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/100) | main | none | no |
| lic | 101 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/101) | main | none | no |
| lic | 102 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2   WP-PLAT-05 MD orac…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/102) | main | none | no |
| lic | 103 | [feat(sim-scientific): WP-SCI-03 QM/CFD/FEA tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/103) | main | none | no |
| lic | 104 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry ker…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/104) | main | none | no |
| lic | 105 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry + WP-PLAT-0…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/105) | main | none | no |
| lic | 106 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry dispatch](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/106) | main | none | no |
| lic | 107 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 registry + WP-PLAT-0…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/107) | main | none | no |
| lic | 108 | [feat(ph-sci): WP-PLAT-05 LAMMPS/GROMACS MD oracle column + algo 104 di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/108) | main | none | no |
| lic | 109 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/109) | main | none | no |
| lic | 110 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/110) | main | none | no |
| lic | 111 | [feat(ph-sci): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD oracle colum…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/111) | main | none | no |
| lic | 112 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD orac…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/112) | main | none | no |
| lic | 113 | [feat(sim-scientific): WP-SCI-03 Phase 2 CFD/FEA/QM tier-2 registry dis…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/113) | main | none | no |
| lic | 114 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 run_algo_registry di…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/114) | main | none | no |
| lic | 115 | [feat(sim-scientific): WP-SCI-03 Phase 2 + WP-PLAT-05 MD oracle stub](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/115) | main | none | no |
| lic | 116 | [feat(ph-sci): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD oracle stub](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/116) | main | none | no |
| lic | 117 | [feat(ph-sci): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD oracle stub](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/117) | main | none | no |
| lic | 118 | [feat(sim-scientific): WP-SCI-03 CFD/FEA/QM tier-2 + WP-PLAT-05 MD orac…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/118) | main | none | no |
| … | … | _41 more in status.json_ | … | … | … |

---

*Agents do not merge governance MRs without owner sign-off. Never push directly to protected `main`.*

*Snapshot regenerated from `data/development-overview/status.json`. Live queue polls the same file in the browser.*
