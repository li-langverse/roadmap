#!/usr/bin/env bash
# Install shared agent-kit from roadmap into a sibling code repo.
# Usage: install-agent-kit.sh <repo-id|path> [--check]
set -euo pipefail

ROADMAP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KIT="$ROADMAP_ROOT/agent-kit"
MANIFEST="$KIT/manifest.toml"
CHECK_ONLY=0

usage() {
  echo "Usage: $0 <lic|lip|lit|/path/to/repo> [--check]" >&2
  exit 1
}

[[ $# -ge 1 ]] || usage
TARGET_ARG="$1"
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK_ONLY=1 ;;
    *) usage ;;
  esac
  shift
done

resolve_target() {
  local arg="$1"
  case "$arg" in
    lic|lip|lit|lis|roadmap|benchmarks)
      local sibling="$ROADMAP_ROOT/../$arg"
      if [[ "$arg" == "lic" && -d "$ROADMAP_ROOT/../li" ]]; then
        sibling="$ROADMAP_ROOT/../li"
      fi
      if [[ -d "$sibling" ]]; then
        echo "$(cd "$sibling" && pwd)"
        return
      fi
      ;;
  esac
  if [[ -d "$arg" ]]; then
    echo "$(cd "$arg" && pwd)"
    return
  fi
  echo "error: target repo not found: $arg" >&2
  exit 1
}

TARGET="$(resolve_target "$TARGET_ARG")"
REPO_ID="$TARGET_ARG"
if [[ "$TARGET" == *"/li" ]]; then
  REPO_ID="lic"
fi

CURSOR_DST="$TARGET/.cursor"
mkdir -p "$CURSOR_DST"

hash_tree() {
  python3 - "$KIT/.cursor" <<'PY'
import hashlib, os, sys
root = sys.argv[1]
h = hashlib.sha256()
for dirpath, _, files in os.walk(root):
    for f in sorted(files):
        p = os.path.join(dirpath, f)
        rel = os.path.relpath(p, root)
        h.update(rel.encode())
        with open(p, "rb") as fp:
            h.update(fp.read())
print(h.hexdigest()[:16])
PY
}

KIT_HASH="$(hash_tree)"
VERSION="$(python3 -c "import tomllib; print(tomllib.load(open('$MANIFEST','rb'))['version'])" 2>/dev/null || echo unknown)"
STAMP="${VERSION}+${KIT_HASH}"

if [[ -f "$CURSOR_DST/agent-kit-version" ]] && [[ "$(cat "$CURSOR_DST/agent-kit-version")" == "$STAMP" ]]; then
  echo "agent-kit already up to date: $STAMP"
  exit 0
fi

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  if [[ -f "$CURSOR_DST/agent-kit-version" ]] && [[ "$(cat "$CURSOR_DST/agent-kit-version")" == "$STAMP" ]]; then
    exit 0
  fi
  echo "agent-kit drift: expected $STAMP, got $(cat "$CURSOR_DST/agent-kit-version" 2>/dev/null || echo missing)" >&2
  exit 1
fi

MERGE_FILE="$TARGET/.cursor/hooks.json.lic-merge"
MERGE_BACKUP=""
if [[ -f "$MERGE_FILE" ]]; then
  MERGE_BACKUP="$(mktemp)"
  cp "$MERGE_FILE" "$MERGE_BACKUP"
fi

echo "Installing agent-kit $STAMP -> $CURSOR_DST"
rsync -a "$KIT/.cursor/" "$CURSOR_DST/"

OVERLAY="$KIT/overlays/$REPO_ID/.cursor"
if [[ -d "$OVERLAY" ]]; then
  rsync -a "$OVERLAY/" "$CURSOR_DST/"
fi

if [[ -n "$MERGE_BACKUP" && -f "$MERGE_BACKUP" ]]; then
  cp "$MERGE_BACKUP" "$CURSOR_DST/hooks.json.lic-merge"
  python3 - "$CURSOR_DST/hooks.json" "$MERGE_BACKUP" <<'PY'
import json, sys
base = json.load(open(sys.argv[1]))
extra = json.load(open(sys.argv[2]))
for phase, entries in extra.get("hooks", {}).items():
    base.setdefault("hooks", {}).setdefault(phase, []).extend(entries)
with open(sys.argv[1], "w") as f:
    json.dump(base, f, indent=2)
    f.write("\n")
print("merged lic hook overlay")
PY
  rm -f "$MERGE_BACKUP"
fi

echo "$STAMP" > "$CURSOR_DST/agent-kit-version"
if [[ "$REPO_ID" == "lic" || "$TARGET" == *"/li" ]]; then
  echo "$STAMP" > "$TARGET/scripts/expected-agent-kit-version" 2>/dev/null || true
fi
echo "Done."
