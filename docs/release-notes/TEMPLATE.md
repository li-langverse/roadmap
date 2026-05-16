# Release notes: YYYY-MM-DD — short-slug

**Status:** WIP | Ready for review | Released  
**Repo:** li-langverse/REPO  
**PR:** #NNN (or branch `feat/...`)  
**PH / REQ:** PH-…, REQ-…  
**Author:** human | agent (session id optional)

---

## Summary (one sentence)

Exact outcome in plain language — what merged and why it matters for the next worker.

## Agent continuation (required)

What the **next agent** should do, in order:

1. Read: (paths or docs)
2. Run: (exact commands)
3. Then: (next task or stop condition)
4. Blocked on: (human / PH- / other repo) or **none**

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| e.g. parser | Describe behavior with file paths | `li-tests/...` green |
| e.g. security | CVE class + mitigation | `security/cve-catalog.json` row |

Use bullets if the table is too narrow:

- `path/to/file` — concrete change (input → output, flag, error text)

## Not changed (scope fence)

Explicit list so agents do not assume work happened elsewhere:

- e.g. LLVM backend / OpenMP / lis tier5 RPS — **not** in this PR

## Breaking changes

None — or **BREAKING:** with migration steps and repos affected.

## Security

N/A — or CVE/CWE ids, new tests (`T-…`), exploit TOML paths.

## Performance

N/A — or bench ids, dashboard link, ratio vs cpp, command to reproduce.

## Downstream

| Repo | Action |
|------|--------|
| lip / lit / lis / packages | bump `li-toolchain.toml` / regenerate lock / N/A |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added|Changed|Fixed
- Specific user-facing line with PH-/REQ- ref ([#NNN](URL))
```
