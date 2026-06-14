# Li development overview

**li-langverse org** · scanned **2026-06-14T08:22Z** · gitlab snapshot · live queue via status.json

| Metric | Value |
|--------|------:|
| Open issues (GitLab) | 64 |
| Ready to merge (CI green) | 9 |
| Open MRs / PRs | 40 |
| Blocked / needs work | 0 |
| Repos with live docs | 2 / 14 |

## Recommended merge order

1. [li-os #5](https://gitlab.lilangverse.xyz/li-langverse/li-os/-/merge_requests/5) — feat: merge master-22 gates (li-os)
2. [li-research-ingest #1](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) — fix(research): R1b ingest state blocker diagnostics + S2 key gate verifi
3. [lit #7](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/7) — fix(pages): apply org Li brand tokens to site landing (lit#8)
4. [lit #9](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/9) — feat(lit): add li-tests shell_ok smoke for documented CLI flows
5. [lit #11](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/11) — feat(li-tests): shell_ok manifest and GitLab CI for lit CLI (lit#6)
6. [lit #12](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/12) — feat(lit): add li-tests shell_ok CLI smoke and GitLab CI (lit#6)
7. [lit #13](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/13) — feat(lit): add li-tests CLI smoke and GitLab CI (lit#6)
8. [lit #15](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/15) — chore(agent-kit): sync org-ga-enforcement.mdc from roadmap v1.3.6
9. [lit #16](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/16) — chore(agent-kit): sync org-ga-enforcement.mdc from roadmap v1.3.6

## Merge when reviewed

| Priority | MR/PR | CI | Action | Notes |
|----------|-------|-----|--------|-------|
| P0 | [li-os#5](https://gitlab.lilangverse.xyz/li-langverse/li-os/-/merge_requests/5) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [li-research-ingest#1](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#7](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/7) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#9](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/9) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#11](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/11) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#12](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/12) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#13](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/13) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#15](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/15) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |
| P0 | [lit#16](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/16) | pass | Merge when approved | snapshot 2026-06-14T08:22Z |

## Do not merge yet

| MR/PR | CI | Action | Notes |
|-------|-----|--------|-------|
| — | — | — | No failing open MRs |

## All open MRs / PRs

| Repo | # | Title | Base | CI | Ready |
|------|---|-------|------|-----|-------|
| benchmarks | 3 | [fix(catalog): PH-5b audit honesty — repo field + vertical stubs (#266)](https://gitlab.lilangverse.xyz/li-langverse/benchmarks/-/merge_requests/3) | main | none | no |
| li-browser | 1 | [feat(ph-br-2): renderer, chrome UI & parity harness complete (BR2-1..7…](https://gitlab.lilangverse.xyz/li-langverse/li-browser/-/merge_requests/1) | main | none | no |
| li-cursor-agents | 12 | [chore(k8s): production sprint configmap](https://gitlab.lilangverse.xyz/li-langverse/li-cursor-agents/-/merge_requests/12) | main | none | no |
| li-os | 5 | [feat: merge master-22 gates (li-os)](https://gitlab.lilangverse.xyz/li-langverse/li-os/-/merge_requests/5) | main | pass | yes |
| li-research-ingest | 1 | [fix(research): R1b ingest state blocker diagnostics + S2 key gate veri…](https://gitlab.lilangverse.xyz/li-langverse/li-research-ingest/-/merge_requests/1) | main | pass | yes |
| lic | 257 | [feat(physics): expand hep/aero/chem domain APIs (lic#7)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/257) | main | none | no |
| lic | 263 | [feat(physics): domain API Wave A+C for lic#7 — core units + hep toy MC](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/263) | main | none | no |
| lic | 264 | [feat(physics): domain APIs for chem Arrhenius + aero orbit (lic#7)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/264) | main | none | no |
| lic | 265 | [feat(physics): domain API Wave A+C for lic#7 — core, hep, aero, chem](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/265) | main | none | no |
| lic | 266 | [feat(physics): domain APIs for hep/aero/quantum packages (lic#7)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/266) | main | none | no |
| lic | 267 | [feat(physics): domain APIs for hep/chem/aero/particles (lic#7)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/267) | main | none | no |
| lic | 272 | [feat(execution): Kokkos-class @parallel(space=host) portable lowering …](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/272) | main | none | no |
| lic | 273 | [feat(7e): @cpu host memory-space + portable parallel decorator lowerin…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/273) | main | none | no |
| lic | 304 | [proof-explorer(phase15): honest catalog prove — Erdős terminal sweep](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/304) | main | none | no |
| lic | 309 | [feat(aimd): wire GPU DFT queue through chem layer in batch loop](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/309) | main | none | no |
| lic | 310 | [feat(crypto): lip-installable crypto stack (M1–M4 gates green)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/310) | main | none | no |
| lic | 320 | [proof(proof-explorer): phase16 — prove target catalog rows](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/320) | main | none | no |
| lic | 321 | [feat(libernetes): Wave 5 distributed_queue stub (LB-P15)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/321) | main | none | no |
| lic | 324 | [docs(changelog): add missing June 2026 release-note bullets (lic#126)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/324) | main | none | no |
| lic | 327 | [docs(changelog): add missing June 2026 Unreleased release notes (lic#1…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/327) | main | none | no |
| lic | 328 | [docs(changelog): add 13 missing June 2026 Unreleased bullets (lic#126)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/328) | main | none | no |
| lic | 330 | [docs(guide): extend getting-started CLI table for agent commands](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/330) | main | none | no |
| lic | 331 | [docs(guide): extend getting-started CLI table with verify/diagnose/smo…](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/331) | main | none | no |
| lic | 332 | [docs(guide): extend getting-started CLI table for agent commands](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/332) | main | none | no |
| lic | 333 | [fix(ci): homelab-k8s dind for lishare-container-e2e](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/333) | main | none | no |
| lic | 334 | [feat(libernetes): Wave 7 container restart policy (LB-C16–C17)](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/334) | main | none | no |
| lic | 335 | [feat(libernetes/livm): Wave 7 VM restart policy](https://gitlab.lilangverse.xyz/li-langverse/lic/-/merge_requests/335) | main | none | no |
| lis | 1 | [feat(registry): homelab lip-registry - agent-first auth, blobs, edge](https://gitlab.lilangverse.xyz/li-langverse/lis/-/merge_requests/1) | main | none | no |
| lit | 7 | [fix(pages): apply org Li brand tokens to site landing (lit#8)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/7) | main | pass | yes |
| lit | 8 | [feat(lit): add li-tests CLI smoke and GitLab CI (lit#6)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/8) | main | none | no |
| lit | 9 | [feat(lit): add li-tests shell_ok smoke for documented CLI flows](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/9) | main | pass | yes |
| lit | 10 | [feat(lit): add li-tests CLI smoke and GitLab CI (lit#6)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/10) | main | none | no |
| lit | 11 | [feat(li-tests): shell_ok manifest and GitLab CI for lit CLI (lit#6)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/11) | main | pass | yes |
| lit | 12 | [feat(lit): add li-tests shell_ok CLI smoke and GitLab CI (lit#6)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/12) | main | pass | yes |
| lit | 13 | [feat(lit): add li-tests CLI smoke and GitLab CI (lit#6)](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/13) | main | pass | yes |
| lit | 14 | [chore(agent-kit): sync org-ga-enforcement.mdc from roadmap v1.3.6](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/14) | main | none | no |
| lit | 15 | [chore(agent-kit): sync org-ga-enforcement.mdc from roadmap v1.3.6](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/15) | main | pass | yes |
| lit | 16 | [chore(agent-kit): sync org-ga-enforcement.mdc from roadmap v1.3.6](https://gitlab.lilangverse.xyz/li-langverse/lit/-/merge_requests/16) | main | pass | yes |
| studio | 6 | [feat(aimd): W9 GPU production — engine default GPU + 5000-DFT launch b…](https://gitlab.lilangverse.xyz/li-langverse/studio/-/merge_requests/6) | main | none | no |
| studio | 9 | [docs(aimd): GPU DFT routing and functional env](https://gitlab.lilangverse.xyz/li-langverse/studio/-/merge_requests/9) | main | none | no |

---

*Agents do not merge governance MRs without owner sign-off. Never push directly to protected `main`.*

*Snapshot regenerated from `data/development-overview/status.json`. Live queue polls the same file in the browser.*
