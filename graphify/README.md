# Graphify knowledge graph

This folder packages [Graphify](https://github.com/Graphify-Labs/graphify) as a
Docker Compose service so the project ships with its own **queryable code
knowledge graph**. Graphify parses the source locally with tree-sitter (Swift
included) — nothing leaves your machine — and turns files, types, and functions
into nodes with explained edges between them.

## What's here

| File | Purpose |
|------|---------|
| `Dockerfile` | Image with the `graphifyy` package installed. |
| `../docker-compose.yml` | `graphify` (MCP server) + `graphify-build` (extractor). |
| `../.graphifyignore` | What to exclude from the graph. |
| `../.githooks/post-commit` | Rebuilds the graph after every commit. |
| `../scripts/setup-graphify.sh` | One-time setup (hooks + first build). |
| `../scripts/rebuild-graph.sh` | Rebuild the graph on demand. |
| `../.mcp.json` | Points AI assistants at the served graph. |

## First-time setup

```bash
./scripts/setup-graphify.sh
```

This enables the tracked git hook, builds the image, and generates the graph.

## Everyday use

- **After each commit** the graph rebuilds automatically into `graphify-out/`.
- **Serve it** for your IDE / AI assistant:
  ```bash
  docker compose up -d graphify
  # MCP Streamable HTTP endpoint: http://localhost:8080/mcp
  ```
- **Rebuild manually** any time:
  ```bash
  ./scripts/rebuild-graph.sh
  ```

## Outputs (in `graphify-out/`, git-ignored)

- `graph.json` — the queryable knowledge graph
- `graph.html` — interactive browser visualization
- `GRAPH_REPORT.md` — highlights and suggested questions

## Shipping to another project

Copy `graphify/`, `docker-compose.yml`, `.graphifyignore`, `.githooks/`,
`scripts/`, and `.mcp.json` into the other repo, then run
`./scripts/setup-graphify.sh` there. Nothing in this setup is specific to the
Yes/No app — the extractor reads whatever source lives at the repo root.

## Notes

- The graph is regenerated from source, so it's intentionally **not committed**
  (`graphify-out/` is git-ignored). What ships is the *setup*, not the data.
- The post-commit rebuild is best-effort: if Docker isn't running or extraction
  fails, your commit still succeeds.
- To exclude more paths from the graph, edit `.graphifyignore`.
