# Release notes: 2026-05-25 — httpd-repo-canonical-wp-b4

**Status:** Ready for review  
**Repo:** li-langverse/roadmap  
**PR:** (branch `docs/httpd-canonical-wp-b4`)  
**PH / REQ:** WP-B4 (org hygiene plan)  
**Author:** agent

---

## Summary (one sentence)

Adds an ecosystem decision table recommending **`li-httpd`** as the canonical GitHub mirror for `import net.httpd`, with **`net.httpd`** legacy and **`li-net-httpd`** as the human-gated rename target (no deletes).

## Agent continuation (required)

1. Read: `docs/ecosystem/httpd-repo-canonical.md`, `lic/docs/ecosystem/repo-naming.md`, org hygiene plan WP-D3.
2. Run: `rg -n 'net\.httpd|li-httpd' roadmap benchmarks .github/li-org-repos.txt`
3. Then: Human executes WP-D3 (`gh repo rename`, archive `net.httpd`); update `official-packages.md` PKG row; mirror README banner on `net.httpd` if desired.
4. Blocked on: human merge of this PR + WP-D3 rename/archive approval.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ecosystem docs | New `docs/ecosystem/httpd-repo-canonical.md` decision table | WP-B4 deliverable |
| httpd-prerequisites | Cross-link to canonical doc | Same PR |
| CHANGELOG | Unreleased entry | This file |

## Not changed (scope fence)

- **`li-httpd` / `net.httpd` repo contents** — no mirror code or CI edits in this PR.
- **`lic` `packages/li-net-httpd/`** — monorepo source unchanged.
- **`lip` registry** — no publish-path migration until WP-D3.
- **Agent-kit manifest** — no version bump.
- **Binary `build/li-httpd`** — naming unchanged.

## Breaking changes

None — documentation only.

## Security

N/A — no code or CVE surface.

## Performance

N/A — no benchmarks.

## Downstream

| Repo | Action |
|------|--------|
| `li-httpd`, `net.httpd` | After human WP-D3: archive/redirect per decision table |
| `benchmarks` | Update ingest paths when repo rename lands |
| `lic` | `github_repo` in `li.toml` already targets `li-net-httpd` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- HTTP mirror decision table (`docs/ecosystem/httpd-repo-canonical.md`) — canonical `li-httpd` vs legacy `net.httpd` (WP-B4).
```
