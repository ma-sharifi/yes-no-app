#!/usr/bin/env bash
#
# Rebuild the Graphify knowledge graph from the current working tree.
# Safe to run standalone; also invoked by .githooks/post-commit.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  echo "[graphify] docker compose not available — skipping graph rebuild." >&2
  exit 0
fi

echo "[graphify] Rebuilding knowledge graph..."
if docker compose run --rm graphify-build; then
  echo "[graphify] Done. See graphify-out/GRAPH_REPORT.md"
else
  echo "[graphify] Graph rebuild failed (non-fatal)." >&2
fi
