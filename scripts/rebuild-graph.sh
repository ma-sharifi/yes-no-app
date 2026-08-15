#!/usr/bin/env bash
#
# Rebuild the Graphify knowledge graph from the current working tree.
# Safe to run standalone; also invoked by .githooks/post-commit.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Prefer a locally installed graphify; fall back to the Docker image.
if command -v graphify >/dev/null 2>&1; then
  echo "[graphify] Rebuilding knowledge graph (local CLI)..."
  graphify extract . --force
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "[graphify] Rebuilding knowledge graph (Docker)..."
  docker compose run --rm graphify
else
  echo "[graphify] Neither the graphify CLI nor docker compose is available — skipping." >&2
  exit 0
fi
echo "[graphify] Done. See graphify-out/GRAPH_REPORT.md"
