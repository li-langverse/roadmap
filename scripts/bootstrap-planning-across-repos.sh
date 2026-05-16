#!/usr/bin/env bash
# Deploy issue-feature-planning workflow to org repos (uses benchmarks script via sparse checkout).
set -euo pipefail

ROADMAP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WF_SRC="$ROADMAP_ROOT/agent-kit/templates/github-workflows/issue-feature-planning.yml"
ORG=li-langverse
REPOS=(lic lip lit lis roadmap)

for repo in "${REPOS[@]}"; do
  dir="$ROADMAP_ROOT/../$repo"
  [[ -d "$dir" ]] || { echo "skip $repo (no checkout at $dir)"; continue; }
  mkdir -p "$dir/.github/workflows"
  cp "$WF_SRC" "$dir/.github/workflows/issue-feature-planning.yml"
  echo "installed workflow -> $repo"
done

echo "Run scripts/setup-org-labels.sh from benchmarks for labels."
