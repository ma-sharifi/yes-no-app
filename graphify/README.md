# Graphify knowledge graph (CLI mode)

This folder packages [Graphify](https://github.com/Graphify-Labs/graphify) as a
project-local **code knowledge graph** you drive from the command line — no MCP
server. Graphify parses the source locally with tree-sitter (Swift included) —
nothing leaves your machine — and turns files, types, and functions into nodes
with explained edges between them. The graph is meant to be **searched first**
by the Copilot agent (and by you) before diving into the code.

## What's here

| File | Purpose |
|------|---------|
| `Dockerfile` | Image with the `graphifyy` package; entrypoint is the `graphify` CLI. |
| `../docker-compose.yml` | One `graphify` service used for both `extract` and `query`. |
| `../.graphifyignore` | What to exclude from the graph. |
| `../.githooks/post-commit` | Rebuilds the graph after every commit. |
| `../scripts/setup-graphify.sh` | One-time setup (hook + first build). |
| `../scripts/rebuild-graph.sh` | Rebuild the graph on demand. |
| `../scripts/graph-query.sh` | **Search the graph** in natural language. |
| `../.github/copilot-instructions.md` | Tells Copilot to query the graph first. |
| `../.github/workflows/copilot-setup-steps.yml` | Preinstalls graphify for the hosted Copilot coding agent. |

## First-time setup

```bash
./scripts/setup-graphify.sh
```

Enables the tracked git hook and builds the graph. Optionally
`pipx install graphifyy` for a faster local CLI (otherwise Docker is used).

## Everyday use

- **Search first** (this is the point):
  ```bash
  ./scripts/graph-query.sh "how does localization get wired into the UI?"
  ```
- **Rebuild** on demand (also runs automatically after each commit):
  ```bash
  ./scripts/rebuild-graph.sh
  ```
- **Visualize**: open `graphify-out/graph.html` in a browser.

## Outputs (in `graphify-out/`, git-ignored)

- `graph.json` — the queryable knowledge graph
- `graph.html` — interactive browser visualization
- `GRAPH_REPORT.md` — highlights and suggested questions

## How Copilot uses it

`.github/copilot-instructions.md` instructs the Copilot agent to run
`./scripts/graph-query.sh "…"` **before** exploring code, so it locates the
right files via the graph instead of a blind text search. Because it's plain
CLI, this works both in local editors and in the GitHub-hosted Copilot coding
agent (which gets graphify preinstalled by `copilot-setup-steps.yml`).

## Shipping to another project

Copy `graphify/`, `docker-compose.yml`, `.graphifyignore`, `.githooks/`,
`scripts/`, `.github/copilot-instructions.md`, and
`.github/workflows/copilot-setup-steps.yml` into the other repo, then run
`./scripts/setup-graphify.sh`. Nothing here is specific to the Yes/No app.

## Notes

- The graph is regenerated from source, so it's intentionally **not committed**
  (`graphify-out/` is git-ignored). What ships is the *setup*, not the data.
- The post-commit rebuild is best-effort: if neither the CLI nor Docker is
  available, your commit still succeeds.
- To exclude more paths from the graph, edit `.graphifyignore`.
