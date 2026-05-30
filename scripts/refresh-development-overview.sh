#!/usr/bin/env bash
# Refresh status.json from GitHub (requires authenticated gh).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "${ROOT}/scripts/refresh_development_overview.py"
