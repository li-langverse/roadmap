#!/usr/bin/env bash
# Install agent-kit + release-notes scaffolding on all li-langverse sibling repos.
set -euo pipefail
ROADMAP="$(cd "$(dirname "$0")/.." && pwd)"
PARENT="$(cd "$ROADMAP/.." && pwd)"
INSTALL="$ROADMAP/scripts/install-agent-kit.sh"

PR_TEMPLATE_BODY='## Summary

## Release notes (required)

Policy: https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md

Link: `docs/release-notes/YYYY-MM-DD-<slug>.md` (skill **write-li-release-notes**)

- [ ] **CHANGELOG.md** `## [Unreleased]` updated
- [ ] Dated `docs/release-notes/` with **Agent continuation** + **Not changed**

## Test plan

- [ ] CI green on PR
'

RN_README='# Release notes

Per-merge agent handoff: `docs/release-notes/YYYY-MM-DD-<slug>.md`

**Policy & template:** https://github.com/li-langverse/roadmap/tree/main/docs/release-notes
'

CHANGELOG_HEADER='# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

'

apply_repo() {
  local id="$1"
  local dir="$PARENT/$id"
  [[ "$id" == "lic" ]] && dir="$PARENT/li"
  [[ -d "$dir/.git" ]] || { echo "skip $id (no checkout)"; return 0; }

  echo "==> $id"
  mkdir -p "$dir/docs/release-notes" "$dir/scripts" "$dir/.github"
  [[ -f "$dir/docs/release-notes/README.md" ]] || printf '%s\n' "$RN_README" > "$dir/docs/release-notes/README.md"
  if [[ ! -f "$dir/CHANGELOG.md" ]]; then
    printf '%s\n- Agent-kit sync and release-notes policy (roadmap v1.1.0).\n' "$CHANGELOG_HEADER" > "$dir/CHANGELOG.md"
  fi
  [[ -f "$dir/.github/pull_request_template.md" ]] || printf '%s' "$PR_TEMPLATE_BODY" > "$dir/.github/pull_request_template.md"
  cat > "$dir/scripts/sync-agent-kit.sh" <<'SYNC'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROADMAP="${LI_ROADMAP_ROOT:-$ROOT/../roadmap}"
exec "$ROADMAP/scripts/install-agent-kit.sh" "REPO_ID_PLACEHOLDER" "$@"
SYNC
  sed -i '' "s/REPO_ID_PLACEHOLDER/$id/" "$dir/scripts/sync-agent-kit.sh" 2>/dev/null || \
    sed -i "s/REPO_ID_PLACEHOLDER/$id/" "$dir/scripts/sync-agent-kit.sh"
  chmod +x "$dir/scripts/sync-agent-kit.sh"
  "$INSTALL" "$id"
}

for id in lic lip lit lis benchmarks roadmap; do
  apply_repo "$id"
done

echo "All repos updated."
