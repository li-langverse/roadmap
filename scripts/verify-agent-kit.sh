#!/usr/bin/env bash
# Verify agent-kit manifest and optional install check against a target repo.
set -euo pipefail
ROADMAP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROADMAP_ROOT/scripts/install-agent-kit.sh" "${1:-lic}" --check
