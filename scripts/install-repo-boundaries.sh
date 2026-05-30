#!/usr/bin/env bash
# Install repo-boundaries.mdc into sibling li-langverse repos.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORG="$(cd "$ROOT/.." && pwd)"
KIT="$ROOT/agent-kit"
TEMPLATE_PKG="$KIT/templates/repo-boundaries-package.mdc"

install_overlay() {
  local repo_id="$1"
  local dst="$ORG/$repo_id/.cursor/rules/repo-boundaries.mdc"
  local src="$KIT/overlays/$repo_id/.cursor/rules/repo-boundaries.mdc"
  if [[ -f "$src" ]]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "  overlay -> $repo_id"
  fi
}

install_package() {
  local repo_id="$1"
  local dst="$ORG/$repo_id/.cursor/rules/repo-boundaries.mdc"
  if [[ ! -d "$ORG/$repo_id/.git" ]]; then
    return
  fi
  if [[ -f "$KIT/overlays/$repo_id/.cursor/rules/repo-boundaries.mdc" ]]; then
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$TEMPLATE_PKG" "$dst"
  echo "  package -> $repo_id"
}

echo "Installing repo-boundaries rules under $ORG"

for id in lic benchmarks li-cursor-agents; do
  install_overlay "$id"
done

# proof-library keeps its own rule if present; install only if missing
if [[ -d "$ORG/proof-library/.git" && ! -f "$ORG/proof-library/.cursor/rules/repo-boundaries.mdc" ]]; then
  install_package proof-library
fi

for id in lip lit lis lidb li-demo li-httpd li-net li-std-core li-std-math li-language li-local-ci research-findings roadmap; do
  install_package "$id"
done

for id in mmo net.httpd physics.custom physics.runtime render sim sim.additive sim.automotive sim.drug_design sim.robotics sim.scientific store.realtime studio studio.ai ui world; do
  install_package "$id"
done

echo "Done."
