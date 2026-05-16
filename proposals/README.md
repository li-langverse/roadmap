# Proposals (ADRs)

Required when a change affects **Li pillars**, **PH order**, **org policy**, or **more than one repo**.

## Learned from (design discipline)

Survey **2–4** mature systems before writing a proposal — e.g. Rust RFC process, Kubernetes enhancements, Cargo workspaces, nginx/httpd operational patterns. Document what you adopt and reject; do not copy verbatim.

## Process

1. Copy `0000-template.md` → `NNNN-short-title.md`
2. Open PR to `proposals/` — **human merges**
3. Update `docs/roadmap/milestones.md` in the same PR when applicable
4. Link **REQ-** / **PH-** ids; land matching tests in `lic` separately

Agents: draft only; do not merge governance PRs.
