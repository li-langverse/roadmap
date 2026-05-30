#!/usr/bin/env bash
# Publish https://li-langverse.github.io/roadmap/development-overview/ locally (no GitHub Actions).
#
# Live PR metrics refresh in the browser (development-overview-live.js); redeploy is only
# needed when the markdown snapshot HTML changes.
#
# Usage:
#   ./scripts/deploy-pages-local.sh              # deploy existing site/
#   ./scripts/deploy-pages-local.sh --build      # gen-development-overview.sh first
#   ./scripts/deploy-pages-local.sh --workflow   # trigger pages.yml (uses Actions)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_SLUG="${PAGES_REPO:-li-langverse/roadmap}"
SITE="${ROOT}/site"
DO_BUILD=0
USE_WORKFLOW=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) DO_BUILD=1 ;;
    --workflow) USE_WORKFLOW=1 ;;
    -h|--help)
      sed -n '2,11p' "$0"
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

run_gh() {
  if [[ -n "${WITH_GITHUB_ENV:-}" && -x "$WITH_GITHUB_ENV" ]]; then
    "$WITH_GITHUB_ENV" gh "$@"
  else
    gh "$@"
  fi
}

find_with_github_env() {
  for d in "$ROOT/../lic" "$ROOT/../li"; do
    if [[ -x "$d/scripts/with-github-env.sh" ]]; then
      export WITH_GITHUB_ENV="$d/scripts/with-github-env.sh"
      return 0
    fi
  done
  return 1
}

if [[ "$USE_WORKFLOW" == "1" ]]; then
  find_with_github_env || true
  echo "==> trigger Development overview (Pages) workflow"
  run_gh workflow run pages.yml --repo "$REPO_SLUG"
  run_gh run list --repo "$REPO_SLUG" --workflow=pages.yml --limit 3
  echo "When green: https://li-langverse.github.io/roadmap/development-overview/"
  exit 0
fi

if [[ "$DO_BUILD" == "1" ]]; then
  chmod +x "$ROOT/scripts/gen-development-overview.sh"
  "$ROOT/scripts/gen-development-overview.sh"
fi

if [[ ! -f "$SITE/development-overview/index.html" ]]; then
  echo "error: $SITE/development-overview/index.html missing — re-run with --build" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI required" >&2
  exit 1
fi
find_with_github_env || true
if [[ -z "${GH_TOKEN:-}" ]]; then
  run_gh auth status >/dev/null 2>&1 || {
    echo "error: gh not authenticated" >&2
    exit 1
  }
fi

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
cp -a "$SITE"/. "$WORKDIR"/
touch "$WORKDIR/.nojekyll"

echo "==> push gh-pages branch"
(
  cd "$WORKDIR"
  git init -q
  git config user.name "roadmap-pages"
  git config user.email "roadmap-pages@users.noreply.github.com"
  git add -A
  git commit -qm "chore: local Pages deploy $(date -u +%Y-%m-%dT%H:%MZ)"
  git branch -M gh-pages
  if [[ -n "${GH_TOKEN:-}" ]]; then
    git push -f "https://x-access-token:${GH_TOKEN}@github.com/${REPO_SLUG}.git" gh-pages
  else
    git remote add origin "https://github.com/${REPO_SLUG}.git"
    run_gh auth setup-git 2>/dev/null || true
    git push -f origin gh-pages
  fi
)

echo "==> ensure Pages source = gh-pages branch"
run_gh api "repos/${REPO_SLUG}/pages" -X PUT \
  --input - <<'JSON' 2>/dev/null || echo "(Pages API: set branch gh-pages / root manually if this failed)"
{
  "build_type": "legacy",
  "source": { "branch": "gh-pages", "path": "/" }
}
JSON

echo ""
echo "Published: https://li-langverse.github.io/roadmap/development-overview/"
echo "Live PR queue updates in-browser — no redeploy needed for queue-only changes."
echo "Snapshot tables: edit docs/development-overview.md then $0 --build"
