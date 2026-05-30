#!/usr/bin/env bash
# Quick org health report for agents (no Actions). Used by Cursor Automations.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPOS_FILE="${ROOT}/.github/li-org-repos.txt"

echo "=== Li ecosystem health check ==="
echo "Dashboard: https://li-langverse.github.io/roadmap/development-overview/"
echo

if command -v gh >/dev/null 2>&1; then
  chmod +x "${ROOT}/scripts/refresh-development-overview.sh"
  "${ROOT}/scripts/refresh-development-overview.sh"
  echo
  python3 -c "
import json
from pathlib import Path
p = Path('${ROOT}/data/development-overview/status.json')
d = json.loads(p.read_text())
m = d['metrics']
print(f\"Open PRs: {m['open_prs']}  Ready: {m['ready_to_merge']}  Blocked: {m['blocked']}\")
eco = d.get('ecosystem') or {}
if eco:
    loc = eco.get('lines_of_code')
    loc_s = f\"{loc:,}\" if isinstance(loc, int) else '?'
    nrepos = eco.get('org_repositories', eco.get('packages'))
    print(f\"LoC: {loc_s}  Org repos: {nrepos}  Issues: {eco.get('issues_open', '?')}  Closed PRs: {eco.get('prs_closed', '?')}\")
failed = [x for x in d['pull_requests'] if x['ci']=='fail']
if failed:
    print('Failed CI:')
    for x in failed:
        print(f\"  {x['repo']}#{x['number']} {x['title'][:60]}\")
" 2>/dev/null || true
  echo
  echo "=== Missing .github/workflows on main ==="
  while read -r repo; do
    [[ -z "$repo" || "$repo" =~ ^# ]] && continue
    if ! gh api "repos/li-langverse/${repo}/contents/.github/workflows" -q '.[].name' 2>/dev/null | grep -qE '\.(yml|yaml)$'; then
      echo "  li-langverse/${repo}"
    fi
  done < "$REPOS_FILE"
else
  echo "gh not installed — install GitHub CLI" >&2
  exit 1
fi

if [[ -d "${ROOT}/../benchmarks" ]]; then
  echo
  echo "=== Benchmarks audit (sibling benchmarks/) ==="
  python3 "${ROOT}/../benchmarks/scripts/ecosystem-audit.py" 2>/dev/null || true
fi

echo
echo "Done."
