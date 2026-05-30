#!/usr/bin/env bash
# Reclaim disk and prune stale local artifacts in li-langverse workspace.
set -euo pipefail

ORG="$(cd "$(dirname "$0")/../.." && pwd)"
echo "Org cleanup: $ORG"

# 1. Remove nested lic worktree inside benchmarks (before deleting dir)
if git -C "$ORG/lic" worktree list 2>/dev/null | grep -q 'benchmarks/data/workspaces'; then
  WT_PATH="$ORG/benchmarks/data/workspaces/li-langverse/lic/bug-fixer-439/repo"
  if [[ -d "$WT_PATH" ]]; then
    git -C "$ORG/lic" worktree remove --force "$WT_PATH" 2>/dev/null || true
  fi
fi

# 2. Ephemeral agent workspaces (gitignored)
for ws in "$ORG/li-cursor-agents/data/workspaces" "$ORG/benchmarks/data/workspaces"; do
  if [[ -d "$ws" ]]; then
    echo "Removing $ws"
    rm -rf "$ws"
  fi
done

# 3. Prune stale /tmp lic worktrees
git -C "$ORG/lic" worktree prune 2>/dev/null || true

# 4. Regenerable node_modules (optional — comment out if you need offline builds)
for nm in \
  "$ORG/benchmarks/dashboard-next/node_modules" \
  "$ORG/proof-library/web/node_modules" \
  "$ORG/proof-library/web/.next" \
  "$ORG/proof-library/web/out" \
  "$ORG/li-cursor-agents/node_modules" \
  "$ORG/li-cursor-agents/dashboard-ui/node_modules"; do
  if [[ -e "$nm" ]]; then
    echo "Removing $nm"
    rm -rf "$nm"
  fi
done

# 5. Stale lic-worktrees (May 25 plan loops — branches remain on remote)
STALE=(
  compiler-studio
  security-research
  sim-chem-research
  sim-md-research
)
for name in "${STALE[@]}"; do
  p="$ORG/lic-worktrees/$name"
  if [[ -d "$p" ]] && git -C "$ORG/lic" worktree list | grep -q "$p"; then
    dirty=$(git -C "$p" status --porcelain 2>/dev/null | wc -l)
    if [[ "$dirty" -eq 0 ]]; then
      echo "Removing stale worktree: $p"
      git -C "$ORG/lic" worktree remove "$p" 2>/dev/null || git -C "$ORG/lic" worktree remove --force "$p" 2>/dev/null || true
    else
      echo "SKIP $p ($dirty dirty files)"
    fi
  fi
done

echo "Done. Run: ./roadmap/scripts/install-repo-boundaries.sh"
