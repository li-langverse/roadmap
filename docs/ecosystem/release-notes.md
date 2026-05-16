# Release notes (mandatory — agent-oriented)

<!-- DOC-ecosystem-release-notes -->

Every **merge-worthy PR** and every **release tag** MUST update release notes so the **next agent** can continue without re-deriving context from the diff alone.

**Canonical template:** [docs/release-notes/TEMPLATE.md](../release-notes/TEMPLATE.md)

## Where notes live

| Repo type | File(s) | Also |
|-----------|---------|------|
| **All org repos** | `CHANGELOG.md` (Keep a Changelog) | Unreleased section before merge |
| **Ship slice / agent handoff** | `docs/release-notes/YYYY-MM-DD-short-slug.md` | Link from CHANGELOG Unreleased |
| **GitHub Release** | Paste same content on tag `v*` | Required for `lic`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap` |

## Rules (no ambiguity)

1. **Specific** — name files, commands, flags, PH-/REQ-/T- ids, and observable outcomes (not “improved parser”).
2. **Scoped** — state what this PR **does not** change (prevents wrong assumptions).
3. **Agent continuation** — required section: what to read next, what is blocked, what CI to run, sibling repos to bump.
4. **Verifiable** — every claim points to evidence: test id, bench row, CVE row, or file path.
5. **No marketing** — no vague “better”, “enhanced”, “various fixes”.
6. **Breaking** — if any downstream must change `li-toolchain.toml`, edition, or API, lead with **BREAKING** and exact migration steps.

## When required

| Change | Release notes |
|--------|----------------|
| User-visible language, compiler, std, lip/lit/lis | **Required** |
| Agent-kit, governance, benchmarks catalog | **Required** |
| CI-only, typo in comment | One-line CHANGELOG entry OK |
| WIP / draft PR | `docs/release-notes/WIP-<branch>.md` allowed; mark **Status: WIP** |

## Agents

- Use skill **write-li-release-notes** before opening PR.
- Rule **li-release-notes.mdc** is always on after agent-kit sync.
- `stop` hook reminds if code changed but `CHANGELOG.md` / `docs/release-notes/` untouched.

Humans merge governance paths; release-note **content** is still required in the PR body and CHANGELOG.
