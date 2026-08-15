#!/usr/bin/env bash
#
# One-time setup for the Graphify knowledge graph in this project.
#   1. Points git at the tracked hooks directory (.githooks).
#   2. Builds the graph for the first time (local CLI or Docker).
#
# After this, every `git commit` refreshes graphify-out/ automatically, and both
# you and the Copilot agent can search it with:
#   ./scripts/graph-query.sh "your question"
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "[graphify] Enabling tracked git hooks (.githooks)..."
git config core.hooksPath .githooks
chmod +x .githooks/post-commit scripts/*.sh 2>/dev/null || true

echo "[graphify] Building the knowledge graph for the first time..."
"$ROOT/scripts/rebuild-graph.sh"

cat <<'EOF'

[graphify] Setup complete.
  • Graph artifacts:  graphify-out/graph.json, graph.html, GRAPH_REPORT.md
  • Auto-rebuild:     runs after every `git commit`
  • Search the graph: ./scripts/graph-query.sh "what plays the tap sounds?"
  • Visualize:        open graphify-out/graph.html in a browser

Tip: install the CLI locally for faster queries with
     `pipx install graphifyy` (otherwise Docker is used automatically).
EOF
