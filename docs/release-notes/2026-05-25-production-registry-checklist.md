# Release notes: 2026-05-25 — production-registry-checklist

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (feat/ph-db-status-doc)  
**PH / REQ:** PH-DB-4, REQ-registry-v2  
**Author:** agent

---

## Summary (one sentence)

Adds §5 production registry checklist to `ph-db-status.md` (DNS, TLS via li-httpd, `LIP_REGISTRY_TOKEN`, `lis db start --profile registry-min`) with human-only secrets steps.

## Agent continuation (required)

1. Read: `docs/ecosystem/ph-db-status.md` §5; `lis/docs/production-registry.md`; `lip/docs/registry.md`
2. Run: after human DNS/TLS, `lip publish --registry https://<host>/v1` with org token
3. Then: refresh §2 percentages when production smoke passes
4. Blocked on: human DNS + `LIP_REGISTRY_TOKEN` in org secrets — agents must not invent credentials

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ecosystem | `docs/ecosystem/ph-db-status.md` §5 production checklist | doc review |
| Release notes | This file | policy |

## Not changed (scope fence)

- `lidb` / `lis` / `lip` implementation code — **not** in this PR
- Benchmark thresholds — **not** changed

## Breaking changes

None.

## Security

N/A — documentation only; explicitly forbids committing production tokens.

## Performance

N/A — no bench runs.

## Downstream

| Repo | Action |
|------|--------|
| lis / lip | align OpenAPI `servers[]` FQDN when DNS cutover PR lands |

## CHANGELOG entry (paste into Unreleased)

- **PH-DB:** `ph-db-status.md` §5 production registry checklist (DNS, TLS, `registry-min`, `LIP_REGISTRY_TOKEN`).
