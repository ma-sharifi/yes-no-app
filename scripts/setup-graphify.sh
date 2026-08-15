#!/usr/bin/env bash
#
# One-time setup for the Graphify knowledge graph in this project.
#   1. Points git at the tracked hooks directory (.githooks).
#   2. Builds the graphify image.
#   3. Generates the graph for the first time.
#
# After this, every `git commit` refreshes graphify-out/ automatically, and you
# can serve the graph with: docker compose up -d graphify
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "[graphify] Enabling tracked git hooks (.githooks)..."
git config core.hooksPath .githooks
chmod +x .githooks/post-commit scripts/*.sh 2>/dev/null || true

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  echo "[graphify] Docker / docker compose not found." >&2
  echo "[graphify] Install Docker Desktop, then re-run this script." >&2
  exit 1
fi

echo "[graphify] Building the graphify image..."
docker compose build graphify

echo "[graphify] Building the knowledge graph for the first time..."
docker compose run --rm graphify-build

cat <<'EOF'

[graphify] Setup complete.
  • Graph artifacts:  graphify-out/graph.json, graph.html, GRAPH_REPORT.md
  • Auto-rebuild:     runs after every `git commit`
  • Serve the graph:  docker compose up -d graphify
  • MCP endpoint:     http://localhost:8080/mcp  (already wired in .mcp.json)
EOF
