#!/usr/bin/env bash
#
# Search the Graphify knowledge graph in natural language.
#
#   ./scripts/graph-query.sh "what connects the buttons to the sounds?"
#
# This is what the Copilot agent (and you) should run FIRST to locate the
# relevant files before reading or editing code — see
# .github/copilot-instructions.md.
#
# Prefers a locally installed `graphify`; otherwise runs it via Docker.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: $0 <natural-language question>" >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [ ! -f graphify-out/graph.json ]; then
  echo "[graphify] graphify-out/graph.json not found — building the graph first..." >&2
  "$ROOT/scripts/rebuild-graph.sh"
fi

if command -v graphify >/dev/null 2>&1; then
  exec graphify query "$*"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  exec docker compose run --rm graphify query "$*"
else
  echo "[graphify] Neither the graphify CLI nor docker compose is available." >&2
  exit 1
fi
