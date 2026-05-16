#!/usr/bin/env bash
# Apply GitHub rulesets (PR-only + CI) for li-langverse org repos.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/apply_org_branch_protection.py" "$@"
